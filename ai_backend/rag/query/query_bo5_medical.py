# ========================================
# QUERY BO5 - Analyse Visite Médicale
# HYBRID: RAG + ML Classifier
# ========================================
import os
import re
import sys
import json
import pandas as pd
import numpy as np
from langdetect import detect
from pathlib import Path
from datetime import datetime
from functools import lru_cache
import pickle
from sentence_transformers import SentenceTransformer, InputExample, losses
from sentence_transformers.evaluation import EmbeddingSimilarityEvaluator
from torch.utils.data import DataLoader
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score


# ========================================
# FIX PATHS
# ========================================
def load_products():
    path = os.path.join(
        PROJECT_ROOT, "ai_backend/data/parapharmacie_vital_final_v2.json"
    )
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# Ajouter le répertoire parent (ai_backend) au path
CURRENT_FILE = Path(__file__).resolve()
AI_BACKEND_DIR = CURRENT_FILE.parent.parent.parent  # ai_backend/
PROJECT_ROOT = AI_BACKEND_DIR.parent  # racine du projet

sys.path.insert(0, str(AI_BACKEND_DIR))
sys.path.insert(0, str(PROJECT_ROOT))

# Dossier de sauvegarde
RAPPORTS_DIR = PROJECT_ROOT / "rapports_archives"
RAPPORTS_DIR.mkdir(exist_ok=True)

# Importer les services RAG
try:
    from services.rag_service import retrieve_context, generate_response
except ImportError as e:
    print(f"⚠️ Erreur import services: {e}")
    raise

EMBED_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"

# ========================================
# FINE-TUNING CONFIGURATION
# ========================================
FINETUNED_MODEL_PATH = PROJECT_ROOT / "ai_backend" / "models" / "finetuned_sentence_transformer"
FINETUNED_MODEL_PATH.mkdir(parents=True, exist_ok=True)


# ========================================
# FINE-TUNING FUNCTIONS
# ========================================
def create_training_pairs(
    df: pd.DataFrame,
    text_column: str = "transcript",
    label_column: str = "main_objection_type",
) -> list:
    """
    Crée des paires (anchor, positive, negative) pour fine-tuning contrastif
    Anchor = texte source
    Positive = autre texte de même classe
    Negative = texte de classe différente
    """
    pairs = []

    texts = df[text_column].astype(str).tolist()
    labels = df[label_column].astype(str).tolist()

    # Grouper par classe
    label_to_indices = {}
    for idx, label in enumerate(labels):
        if label not in label_to_indices:
            label_to_indices[label] = []
        label_to_indices[label].append(idx)

    # Créer des triplets
    for anchor_idx, anchor_label in enumerate(labels):
        anchor_text = texts[anchor_idx]

        # Positif: un autre texte de même classe
        same_class_indices = label_to_indices[anchor_label]
        if len(same_class_indices) > 1:
            positive_idx = np.random.choice(
                [i for i in same_class_indices if i != anchor_idx]
            )
            positive_text = texts[positive_idx]

            # Négatif: un texte de classe différente
            different_labels = [l for l in label_to_indices.keys() if l != anchor_label]
            if different_labels:
                negative_label = np.random.choice(different_labels)
                negative_idx = np.random.choice(label_to_indices[negative_label])
                negative_text = texts[negative_idx]

                pairs.append(
                    InputExample(texts=[anchor_text, positive_text, negative_text])
                )

    return pairs


def fine_tune_sentence_transformer(
    csv_path: str = None, epochs: int = 2, batch_size: int = 16
) -> SentenceTransformer:
    """
    Fine-tune le SentenceTransformer sur les données médicales
    Utilise TripletLoss pour maximiser similarité intra-classe et minimiser inter-classe
    """
    print(f"🔧 Début du fine-tuning du SentenceTransformer...")

    # Charger dataset
    if csv_path is None:
        csv_path = os.path.join(AI_BACKEND_DIR, "data", "vital_bo6_dataset.csv")

    df = pd.read_csv(csv_path)
    df = df.dropna(subset=["transcript", "main_objection_type"]).copy()
    df["main_objection_type"] = df["main_objection_type"].apply(
        normalize_objection_label
    )

    print(f"📊 Dataset: {len(df)} samples")

    # Charger modèle pré-entraîné
    model = SentenceTransformer(EMBED_MODEL)

    # Créer paires d'entraînement
    train_examples = create_training_pairs(df)
    print(f"📚 Paires créées: {len(train_examples)}")

    # DataLoader
    train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=batch_size)

    # Loss: TripletLoss pour apprentissage métrique
    train_loss = losses.TripletLoss(model=model)

    # Entraîner
    print(f"🚀 Fine-tuning sur {epochs} epochs...")
    model.fit(
        train_objectives=[(train_dataloader, train_loss)],
        epochs=epochs,
        warmup_steps=100,
        show_progress_bar=True,
    )

    # Sauvegarder modèle fine-tuné
    model.save(str(FINETUNED_MODEL_PATH), safe_serialization=False)
    print(f"✅ Modèle fine-tuné sauvegardé: {FINETUNED_MODEL_PATH}")

    return model


@lru_cache(maxsize=1)
def get_sentence_transformer_finetuned() -> SentenceTransformer:
    """Charge le modèle fine-tuné s'il existe, sinon charge le pré-entraîné"""
    if (FINETUNED_MODEL_PATH / "pytorch_model.bin").exists():
        print(f"✅ Chargement modèle fine-tuné: {FINETUNED_MODEL_PATH}")
        return SentenceTransformer(str(FINETUNED_MODEL_PATH))
    else:
        print(f"⚠️ Pas de modèle fine-tuné trouvé. Utilisation du modèle pré-entraîné.")
        return SentenceTransformer(EMBED_MODEL)


def full_finetuning_pipeline(
    csv_path: str = None, epochs: int = 2, batch_size: int = 16
) -> dict:
    """
    Pipeline complet de fine-tuning:
    1. Fine-tune le SentenceTransformer
    2. Réentraîne le classifier ML sur les embeddings fine-tunés
    3. Retourne les métriques
    """
    print("\n" + "=" * 80)
    print("🚀 PIPELINE COMPLET DE FINE-TUNING")
    print("=" * 80)

    # Étape 1: Fine-tune SentenceTransformer
    print("\n📍 Étape 1: Fine-tuning SentenceTransformer...")
    finetuned_model = fine_tune_sentence_transformer(
        csv_path, epochs=epochs, batch_size=batch_size
    )

    # Étape 2: Invalider cache pour utiliser nouveau modèle
    print("\n📍 Étape 2: Invalidation des caches...")
    get_sentence_transformer.cache_clear()
    get_sentence_transformer_finetuned.cache_clear()

    # Étape 3: Réentraîner classifier
    print("\n📍 Étape 3: Réentraînement du classifier...")
    df = load_objection_dataset(csv_path)
    embedder = get_sentence_transformer()

    texts = df["transcript"].astype(str).tolist()
    labels = df["main_objection_type"].astype(str).tolist()

    X_train, X_valid, y_train, y_valid = train_test_split(
        texts, labels, test_size=0.2, stratify=labels, random_state=42
    )

    X_train_embeddings = embedder.encode(
        X_train, convert_to_numpy=True, show_progress_bar=True
    )
    X_valid_embeddings = embedder.encode(
        X_valid, convert_to_numpy=True, show_progress_bar=True
    )

    classifier = LogisticRegression(
        max_iter=2000, solver="lbfgs", class_weight="balanced", random_state=42
    )
    classifier.fit(X_train_embeddings, y_train)

    train_pred = classifier.predict(X_train_embeddings)
    valid_pred = classifier.predict(X_valid_embeddings)

    train_acc = accuracy_score(y_train, train_pred)
    valid_acc = accuracy_score(y_valid, valid_pred)

    print("\n" + "=" * 80)
    print("✅ FINE-TUNING TERMINÉ")
    print("=" * 80)

    return {
        "success": True,
        "finetuned_model": finetuned_model,
        "classifier": classifier,
        "train_accuracy": float(train_acc),
        "validation_accuracy": float(valid_acc),
        "message": f"Accuracy: Train={train_acc:.1%}, Validation={valid_acc:.1%}",
    }


# ========================================
# 1. PARSER CONVERSATION
# ========================================
def parse_conversation(dialogue: str) -> dict:
    """
    Parse une conversation entre délégué et médecin

    Format accepté:
    DÉLÉGUÉ: ...
    MÉDECIN: ...
    """
    lines = dialogue.split("\n")

    delegue_text = []
    medecin_text = []
    exchanges = []

    current_speaker = None
    current_text = ""

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Détecter le speaker
        if line.upper().startswith("DÉLÉGUÉ:") or line.upper().startswith("DELEGATE:"):
            if current_speaker and current_text:
                exchanges.append(
                    {"speaker": current_speaker, "text": current_text.strip()}
                )
            current_speaker = "DÉLÉGUÉ"
            current_text = line.split(":", 1)[1] if ":" in line else ""
            delegue_text.append(current_text)

        elif (
            line.upper().startswith("MÉDECIN:")
            or line.upper().startswith("MEDECIN:")
            or line.upper().startswith("DOCTOR:")
        ):
            if current_speaker and current_text:
                exchanges.append(
                    {"speaker": current_speaker, "text": current_text.strip()}
                )
            current_speaker = "MÉDECIN"
            current_text = line.split(":", 1)[1] if ":" in line else ""
            medecin_text.append(current_text)

        else:
            # Continuation de la réplique précédente
            if current_speaker:
                current_text += "\n" + line

    # Ajouter la dernière réplique
    if current_speaker and current_text:
        exchanges.append({"speaker": current_speaker, "text": current_text.strip()})

    return {
        "exchanges": exchanges,
        "delegue_text": " ".join(delegue_text),
        "medecin_text": " ".join(medecin_text),
        "full_dialogue": dialogue,
    }


# ========================================
# 2. DÉTECTEUR D'OBJECTIONS (OPTIMISÉ)
# ========================================
def detect_objections(dialogue_text: str) -> list:
    """
    Détecte les objections dans le texte (SANS DOUBLONS)
    """
    objection_patterns = {
        "price": {
            "keywords": ["prix", "cher", "coût", "cost", "expensive", "budget"],
            "type": "Price Objection",
        },
        "safety": {
            "keywords": [
                "effets secondaires",
                "safety",
                "tolérance",
                "tolerance",
                "sécurité",
                "side effects",
                "adverse",
            ],
            "type": "Safety Concern",
        },
        "efficacy": {
            "keywords": [
                "efficacité",
                "efficacy",
                "étude",
                "study",
                "evidence",
                "preuve",
                "results",
            ],
            "type": "Efficacy Question",
        },
        "stock": {
            "keywords": [
                "stock",
                "disponible",
                "availability",
                "grossiste",
                "available",
            ],
            "type": "Stock/Availability",
        },
        "reimbursement": {
            "keywords": [
                "cnam",
                "reimbursement",
                "remboursement",
                "couverture",
                "coverage",
            ],
            "type": "Reimbursement",
        },
    }

    text_lower = dialogue_text.lower()
    detected = []
    detected_types = set()  # 🔥 ÉVITER DOUBLONS

    for key, pattern in objection_patterns.items():
        for keyword in pattern["keywords"]:
            if keyword in text_lower and pattern["type"] not in detected_types:
                # Extraire le contexte (phrase contenant le keyword)
                sentences = re.split(r"[.!?]", dialogue_text)
                for sentence in sentences:
                    if keyword in sentence.lower():
                        detected.append(
                            {
                                "type": pattern["type"],
                                "text": sentence.strip(),
                                "keyword": keyword,
                            }
                        )
                        detected_types.add(pattern["type"])  # 🔥 Marquer comme trouvé
                        break
                break  # 🔥 Passer à l'objection suivante

    return detected


# ========================================
# 2B. SENTIMENT & INTÉRÊT PREDICTIONS
# ========================================


def predict_sentiment(dialogue_text: str) -> float:
    """
    Estime un score de sentiment simple basé sur un lexique.
    Retourne: -1.0 (négatif) à +1.0 (positif)
    """
    positive_words = [
        "bien",
        "excellent",
        "meilleur",
        "amélioration",
        "sûr",
        "sûreté",
        "tolérance",
        "support",
        "disponible",
    ]
    negative_words = [
        "cher",
        "inquiet",
        "risque",
        "effets secondaires",
        "indisponible",
        "problème",
        "non",
        "pas",
        "doute",
    ]

    lower = dialogue_text.lower()
    score = 0
    for word in positive_words:
        score += lower.count(word)
    for word in negative_words:
        score -= lower.count(word)

    if score > 0:
        return min(1.0, score / 5)
    if score < 0:
        return max(-1.0, score / 5)
    return 0.0


def predict_interest(dialogue_text: str) -> int:
    """
    Estime un niveau d'intérêt approximatif (0-100) pour le médecin.
    """
    interest_signals = [
        "intéressé",
        "intéressant",
        "oui",
        "ok",
        "d'accord",
        "bon",
        "très bien",
        "je vais",
    ]
    disinterest_signals = [
        "non",
        "pas intéressé",
        "je n'ai pas besoin",
        "plus tard",
        "trop cher",
        "déjà",
        "je suis pressé",
    ]

    lower = dialogue_text.lower()
    score = 50
    for word in interest_signals:
        if word in lower:
            score += 10
    for word in disinterest_signals:
        if word in lower:
            score -= 10

    return max(0, min(100, score))


def cosine_similarity(vec_a, vec_b):
    """Retourne la similarité cosinus entre deux vecteurs."""
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(vec_a, vec_b) / (norm_a * norm_b))


@lru_cache(maxsize=1)
def get_sentence_transformer() -> SentenceTransformer:
    """Charge le modèle d'embedding (fine-tuné si disponible, sinon pré-entraîné)"""
    return get_sentence_transformer_finetuned()


def normalize_objection_label(label: str) -> str:
    label = str(label).strip().upper()
    if label in {"PRICE", "COST"}:
        return "PRICE_OBJECTION"
    if label in {"SAFETY", "ASK_SAFETY"}:
        return "ASK_SAFETY"
    if label in {"EFFICACY", "ASK_EFFICACY"}:
        return "ASK_EFFICACY"
    if label in {"STOCK", "STOCK_AVAILABILITY"}:
        return "STOCK_AVAILABILITY"
    if label in {"REIMBURSEMENT", "CNAM", "CNAM_REIMBURSEMENT"}:
        return "CNAM_REIMBURSEMENT"
    if label == "COMPETITOR_COMPARISON":
        return label
    return label


def load_objection_dataset(csv_path: str = None) -> pd.DataFrame:
    if csv_path is None:
        csv_path = os.path.join(
            PROJECT_ROOT, "ai_backend", "data", "vital_bo6_dataset.csv"
        )

    if not os.path.exists(csv_path):
        print(f"⚠️  Dataset non trouvé: {csv_path}")
        return pd.DataFrame()

    df = pd.read_csv(csv_path)
    df = df.dropna(subset=["transcript", "main_objection_type"]).copy()
    df["main_objection_type"] = df["main_objection_type"].apply(
        normalize_objection_label
    )
    df = df[
        df["main_objection_type"].isin(
            {
                "ASK_SAFETY",
                "ASK_EFFICACY",
                "STOCK_AVAILABILITY",
                "CNAM_REIMBURSEMENT",
                "PRICE_OBJECTION",
                "COMPETITOR_COMPARISON",
            }
        )
    ]
    df = df.drop_duplicates(subset=["transcript", "main_objection_type"])
    return df


@lru_cache(maxsize=1)
def train_objection_classifier(
    csv_path: str = None, test_size: float = 0.2, random_state: int = 42
) -> dict:
    """Entraîne un classifieur local sur les embeddings du dataset et conserve une validation hold-out."""
    df = load_objection_dataset(csv_path)

    if df.empty:
        print("⚠️  Dataset vide - classifier non entraîné")
        return {"error": "Dataset vide"}

    embedder = get_sentence_transformer()
    texts = df["transcript"].astype(str).tolist()
    labels = df["main_objection_type"].astype(str).tolist()

    # Split train/validation with stratification
    X_train, X_valid, y_train, y_valid = train_test_split(
        texts, labels, test_size=test_size, stratify=labels, random_state=random_state
    )

    X_train_embeddings = embedder.encode(
        X_train, convert_to_numpy=True, show_progress_bar=False
    )
    X_valid_embeddings = embedder.encode(
        X_valid, convert_to_numpy=True, show_progress_bar=False
    )

    classifier = LogisticRegression(
        max_iter=2000,
        solver="lbfgs",
        class_weight="balanced",
        random_state=random_state,
    )
    classifier.fit(X_train_embeddings, y_train)

    train_predictions = classifier.predict(X_train_embeddings)
    train_accuracy = float(accuracy_score(y_train, train_predictions))

    valid_predictions = classifier.predict(X_valid_embeddings)
    valid_accuracy = float(accuracy_score(y_valid, valid_predictions))

    return {
        "classifier": classifier,
        "embedder": embedder,
        "X_train": X_train,
        "y_train": y_train,
        "X_valid": X_valid,
        "y_valid": y_valid,
        "X_train_embeddings": X_train_embeddings,
        "X_valid_embeddings": X_valid_embeddings,
        "train_accuracy": train_accuracy,
        "validation_accuracy": valid_accuracy,
        "train_predictions": train_predictions,
        "validation_predictions": valid_predictions,
        "classes": classifier.classes_,
    }


def predict_main_objection_type(dialogue_text: str) -> tuple:
    """Prédit le type d'objection principal en utilisant des règles et un classifieur appris."""
    lower = dialogue_text.lower()
    keyword_patterns = [
        (
            "COMPETITOR_COMPARISON",
            [
                "concurrent",
                "produit concurrent",
                "pourquoi changer",
                "comparaison",
                "alternatives",
            ],
        ),
        (
            "CNAM_REIMBURSEMENT",
            [
                "cnam",
                "remboursement",
                "couverture",
                "assurance",
                "prise en charge",
                "remboursé",
            ],
        ),
        (
            "PRICE_OBJECTION",
            ["prix", "coût", "budget", "tarif", "trop cher", "cher", "prix élevé"],
        ),
        (
            "ASK_SAFETY",
            [
                "effets secondaires",
                "sécurité",
                "risque",
                "tolérance",
                "inquiet",
                "inquiète",
                "allergie",
                "toléré",
            ],
        ),
        (
            "ASK_EFFICACY",
            [
                "efficacité",
                "efficace",
                "preuve",
                "étude",
                "study",
                "résultats",
                "amélioration",
                "performant",
            ],
        ),
        (
            "STOCK_AVAILABILITY",
            [
                "stock",
                "disponible",
                "grossiste",
                "livraison",
                "rupture",
                "en stock",
                "disponibilité",
                "approvisionnement",
            ],
        ),
    ]

    for label, keywords in keyword_patterns:
        if any(keyword in lower for keyword in keywords):
            return label, 0.92

    try:
        trained = train_objection_classifier()
        if "error" in trained:
            return "PRICE_OBJECTION", 0.5

        emb = get_sentence_transformer().encode(
            [dialogue_text], convert_to_numpy=True, show_progress_bar=False
        )[0]
        predicted = trained["classifier"].predict([emb])[0]
        proba = trained["classifier"].predict_proba([emb])[0]
        best_score = float(max(proba))

        return predicted, best_score
    except Exception as e:
        print(f"⚠️  Erreur classifier: {e}")
        return "PRICE_OBJECTION", 0.5


def extract_objection_sentence(text: str, label: str, max_len: int = 140) -> str:
    label = normalize_objection_label(label)
    sentence_keywords = {
        "ASK_SAFETY": [
            "effets secondaires",
            "sécurité",
            "risque",
            "tolérance",
            "inquiet",
            "inquiète",
            "allergie",
            "contre-indication",
            "douleur",
        ],
        "ASK_EFFICACY": [
            "efficacité",
            "étude",
            "preuves",
            "données cliniques",
            "performance",
            "résultats",
            "fonctionne",
            "prouvé",
            "amélioration",
        ],
        "PRICE_OBJECTION": [
            "prix",
            "coût",
            "budget",
            "tarif",
            "trop cher",
            "cher",
            "facturation",
        ],
        "STOCK_AVAILABILITY": [
            "stock",
            "disponible",
            "indisponible",
            "rupture",
            "en stock",
            "disponibilité",
            "livraison",
            "approvisionnement",
        ],
        "CNAM_REIMBURSEMENT": [
            "cnam",
            "remboursement",
            "couverture",
            "prise en charge",
            "assurance",
            "remboursé",
        ],
        "COMPETITOR_COMPARISON": [
            "concurrent",
            "produit concurrent",
            "comparaison",
            "alternatives",
            "autre produit",
            "concurrence",
            "autre marque",
        ],
    }
    keywords = sentence_keywords.get(label, [])
    sentences = re.split(r"(?<=[\.\?\!])\s+", text.replace("\n", " "))
    for sentence in sentences:
        lower = sentence.lower()
        if any(keyword in lower for keyword in keywords):
            excerpt = sentence.strip()
            return (
                excerpt
                if len(excerpt) <= max_len
                else excerpt[:max_len].rstrip() + "..."
            )
    # Fallback sur la première phrase
    first = sentences[0].strip() if sentences else text.strip()
    return first if len(first) <= max_len else first[:max_len].rstrip() + "..."


def evaluate_objection_classifier(csv_path: str = None) -> dict:
    """Évalue le classifieur local sur un jeu de validation séparé."""
    trained = train_objection_classifier(csv_path)

    if "error" in trained:
        return {"error": "Classifier non disponible"}

    y_valid = trained["y_valid"]
    y_pred = trained["validation_predictions"]
    proba = trained["classifier"].predict_proba(trained["X_valid_embeddings"])

    accuracy = float(accuracy_score(y_valid, y_pred))
    report = classification_report(y_valid, y_pred, output_dict=True, zero_division=0)

    predictions = []
    for true_label, pred_label, scores, text in zip(
        y_valid, y_pred, proba, trained["X_valid"]
    ):
        predictions.append(
            {
                "true": true_label,
                "predicted": pred_label,
                "confidence": float(max(scores)),
                "excerpt": extract_objection_sentence(text, true_label),
            }
        )

    return {
        "accuracy": accuracy,
        "total": len(y_valid),
        "correct": int(sum(1 for true, pred in zip(y_valid, y_pred) if true == pred)),
        "train_accuracy": trained["train_accuracy"],
        "validation_accuracy": accuracy,
        "classification_report": report,
        "predictions": predictions[:50],
    }


# ========================================
# 🔥 FILTRE PRODUITS PAR SPÉCIALITÉ
# ========================================
def filter_products_by_specialty(products, specialty):
    specialty_map = {
        "Cardiologie": ["cardio", "cardiovasculaire", "omega", "coeur"],
        "Dermatologie": ["acné", "peau", "dermato"],
        "Immunologie": ["immunité", "vitamine", "zinc"],
        "Neurologie": ["cerveau", "mémoire", "cognitif"],
        "Médecine Générale": [],
    }

    keywords = specialty_map.get(specialty, [])

    filtered = []
    for p in products:
        text = " ".join(safe_list(p.get("type_medical"))).lower()
        if any(k in text for k in keywords):
            filtered.append(p)

    return filtered if filtered else products


# ========================================
# 🔥 EXTRACTION PRODUIT
# ========================================
def extract_product_from_dialogue(dialogue, products):
    dialogue_lower = dialogue.lower()

    best_match = None
    best_score = 0

    for p in products:
        score = 0

        # nom produit
        if (p.get("name") or "").lower() in dialogue_lower:
            score += 5

        # 🔥 FIX ICI
        for t in p.get("type_medical") or []:
            if t.lower() in dialogue_lower:
                score += 2

        # 🔥 FIX ICI AUSSI
        for ind in p.get("indications") or []:
            if ind.lower() in dialogue_lower:
                score += 1

        if score > best_score:
            best_score = score
            best_match = p.get("name")

    return best_match


# ========================================
# 🔥 RECOMMANDATION PRODUITS
# ========================================
def safe_list(x):
    if isinstance(x, list):
        return x
    elif isinstance(x, str):
        return [x]
    else:
        return []


def extract_detected_needs(dialogue: str) -> list:
    text_lower = dialogue.lower()

    needs_dict = {
        "Fatigue": ["fatigue", "fatigué", "épuisé"],
        "Immunité": ["immunité", "immunitaire"],
        "Cardiovasculaire": ["coeur", "cardio"],
        "Stress": ["stress", "anxiété"],
        "Infection": ["infection", "viral"],
    }

    detected = []

    for need, keywords in needs_dict.items():
        for k in keywords:
            if k in text_lower:
                detected.append(need)
                break

    return detected


def recommend_products(dialogue, products, specialty):
    dialogue_lower = dialogue.lower()

    filtered = filter_products_by_specialty(products, specialty)
    needs = extract_detected_needs(dialogue)

    results = []

    for p in filtered:
        score = 0
        reasons = []

        # 🔥 type médical
        for keyword in safe_list(p.get("type_medical")):
            if keyword.lower() in dialogue_lower:
                score += 3
                reasons.append(f"lié à {keyword}")

        # 🔥 indications (plus important maintenant)
        for keyword in safe_list(p.get("indications")):
            if keyword.lower() in dialogue_lower:
                score += 4
                reasons.append(f"indiqué pour {keyword}")

        # 🔥 bénéfices
        for keyword in safe_list(p.get("benefices")):
            if keyword.lower() in dialogue_lower:
                score += 2
                reasons.append(f"améliore {keyword}")

        # 🔥 besoins détectés (ULTRA IMPORTANT)
        product_text = " ".join(
            safe_list(p.get("type_medical")) + safe_list(p.get("indications"))
        ).lower()

        matched_needs = []
        for need in needs:
            if need.lower() in product_text:
                score += 5  # 🔥 BOOST
                matched_needs.append(need)

        if matched_needs:
            reasons.append(f"répond aux besoins: {', '.join(matched_needs)}")

        # 🔥 pénalité si aucun lien réel
        if score < 3:
            continue

        results.append(
            {
                "name": p.get("name", "Produit inconnu"),
                "score": score,
                "why": generate_natural_explanation(reasons, needs),
            }
        )

    results.sort(key=lambda x: x["score"], reverse=True)

    return results[:3]


def generate_natural_explanation(reasons, needs):
    if not reasons:
        return "Produit recommandé basé sur la spécialité médicale."

    explanation = "Ce produit est recommandé car "

    if needs:
        explanation += f"il correspond aux besoins détectés ({', '.join(needs)}), "

    explanation += "et " + ", ".join(reasons[:2]) + "."

    return explanation


# ========================================
# 3. STRATÉGIES D'OBJECTIONS (AMÉLIORÉ)
# ========================================
def safe_generate_response(
    query: str, context_docs: list, system_prompt: str = None
) -> str:
    """
    Génère une réponse en sécurité en capturant les erreurs Groq.
    """
    try:
        return generate_response(query, context_docs, system_prompt)
    except Exception as e:
        err = str(e).lower()
        if (
            "quota groq" in err
            or "rate limit" in err
            or "tokens per day" in err
            or "rate_limit" in err
        ):
            return (
                "⚠️ Analyse Groq temporairement indisponible : limite de tokens atteinte. "
                "Réponse locale : analyse simplifiée basée sur le dialogue."
            )
        raise


def get_objection_strategies(
    objection_type: str, context_docs: list, dialogue: str = ""
) -> str:
    """
    Génère une stratégie de réponse enrichie pour chaque objection
    """

    # Prompts personnalisés par type d'objection
    strategies_prompts = {
        "Price Objection": """Tu es un expert en ventes médicales spécialisé dans la gestion des objections de prix.
Analyse le dialogue et propose une stratégie pour justifier le prix en mettant l'accent sur:
1. Le ROI à long terme
2. La qualité et l'efficacité supérieure
3. Les économies potentielles
4. Les options de flexibilité tarifaire

Fournis une réponse structurée et convaincante.""",
        "Safety Concern": """Tu es un pharmacologue expert en ventes médicales.
L'objectif est de rassurer sur la sécurité du produit.
Fournis une stratégie qui:
1. Reconnaît la préoccupation
2. Présente les données cliniques de sécurité
3. Compare avec les produits concurrents
4. Explique les protocoles de surveillance

Sois rassurant et factuel.""",
        "Efficacy Question": """Tu es un expert clinique en ventes médicales.
La question porte sur l'efficacité du produit.
Génère une stratégie qui:
1. Présente les résultats d'études cliniques
2. Explique les mécanismes d'action
3. Montre les bénéfices comparatifs
4. Propose des cas d'usage spécifiques

Utilise les données pertinentes du contexte.""",
        "Stock/Availability": """Tu es un gestionnaire de supply chain médical.
Crée une stratégie d'assurance de disponibilité qui:
1. Rassure sur la disponibilité actuelle
2. Explique le système de réapprovisionnement
3. Propose des délais de livraison
4. Offre des alternatives si nécessaire

Sois proactif et transparent.""",
        "Reimbursement": """Tu es un expert en remboursement CNAM/assurances.
La préoccupation: couverture et remboursement.
Stratégie:
1. Explique le statut de remboursement actuel
2. Présente le processus d'évaluation
3. Liste les aides financières disponibles
4. Propose des options de paiement

Sois informatif et encourageant.""",
    }

    system_prompt = strategies_prompts.get(
        objection_type, strategies_prompts["Price Objection"]
    )

    context_text = "\n".join(
        [f"📌 {doc['content'][:400]}" for doc in context_docs[:3]]  # Top 3 seulement
    )

    query = f"""Dialogue récent:
{dialogue[-500:] if dialogue else "Contexte général"}

Contexte de la base de données:
{context_text}

Génère une stratégie de réponse professionnelle et persuasive."""

    strategy = safe_generate_response(query, context_docs, system_prompt)

    return strategy


# ========================================
# 4. ANALYSE COMPLÈTE
# ========================================
def analyze_conversation(
    dialogue: str,
    rapport_type: str = "Analyse Objections",
    top_k: int = 5,
    use_finetuned: bool = True,
) -> dict:
    """
    Pipeline complet d'analyse d'une visite médicale
    HYBRID: Detection Objections + ML Classifier + RAG Retrieval + LLM Generation
    use_finetuned: Utiliser embeddings fine-tuned (True) ou standard (False)
    """

    # Parser la conversation
    parsed = parse_conversation(dialogue)
    exchanges = parsed["exchanges"]

    # Détecter objections
    objections = detect_objections(dialogue)

    # Récupérer contexte pour chaque objection
    enriched_objections = []
    for obj in objections:
        context = retrieve_context(
            obj["text"], top_k=top_k, use_finetuned=use_finetuned
        )

        # 🔥 FILTRER: Garder SEULEMENT les sources avec bon score
        context = [c for c in context if c["score"] > 0.3]

        if not context:
            continue  # Passer si pas de bon contexte

        # 🔥 AMÉLIORATION: Passer le dialogue complet pour meilleur contexte
        strategy = get_objection_strategies(
            obj["type"], context, dialogue=dialogue  # ← Dialogue entier
        )

        enriched_objections.append(
            {
                "type": obj["type"],
                "text": obj["text"],
                "strategy": strategy,
                "sources": context,
            }
        )

    # Générer analyse globale
    analysis_query = f"""Analysez cette visite médicale et générez un rapport {rapport_type}:
    
Dialogue:
{dialogue}

Objections détectées: {len(objections)}
"""

    context = retrieve_context(dialogue[:500], top_k=top_k, use_finetuned=use_finetuned)

    # 🔥 FILTRER: Garder seulement les sources avec bon score
    context = [c for c in context if c["score"] > 0.3]

    # Si Chroma est vide, créer un contexte par défaut
    if not context:
        context = [
            {
                "content": "Aucun document pertinent trouvé dans la base. Génération avec contexte générique.",
                "score": 0.0,
            }
        ]

    analysis = safe_generate_response(
        analysis_query,
        context,
        system_prompt="""Tu es un analyseur expert en visites médicales.
Analyse le dialogue et fournis:
1. Points clés de la visite
2. Objections majeures
3. Opportunités
4. Recommandations""",
    )

    # 🔥 NEW: ML Predictions
    predicted_main_objection, predicted_objection_score = predict_main_objection_type(
        dialogue
    )
    predicted_sentiment = predict_sentiment(dialogue)
    predicted_interest = predict_interest(dialogue)

    # 🔥 NEW: AMÉLIORATIONS - Extraire les nouvelles données
    detected_language = detect_language(dialogue)
    medical_specialty = detect_medical_specialty(dialogue)
    engagement_data = detect_engagement(dialogue)
    client_typology = classify_client_typology(dialogue)
    # 🔥 charger produits (IMPORTANT)
    products = load_products()  # ou passé en paramètre

    # 🔥 utiliser TES fonctions
    detected_needs = extract_detected_needs(dialogue)
    proposed_product = extract_product_from_dialogue(dialogue, products)

    recommended_products = recommend_products(dialogue, products, medical_specialty)

    # 🔥 NEW: Améliorer le score de visite avec le nouvel algorithme
    improved_visit_score = improve_visit_score(
        dialogue,
        objections_count=len(objections),
        engagement_score=engagement_data["score"],
        sentiment=predicted_sentiment,
    )

    return {
        "type": rapport_type,
        "analysis": analysis,
        "objections": enriched_objections,
        "sources": context,
        "predicted_sentiment": predicted_sentiment,
        "predicted_interest": predicted_interest,
        "predicted_main_objection": predicted_main_objection,
        "predicted_objection_score": predicted_objection_score,
        "key_points": {
            "Total Exchanges": len(exchanges),
            "Objections Found": len(objections),
            "Délégué Messages": len(
                [e for e in exchanges if e["speaker"] == "DÉLÉGUÉ"]
            ),
            "Médecin Messages": len(
                [e for e in exchanges if e["speaker"] == "MÉDECIN"]
            ),
        },
        "exchanges": exchanges,
        # 🔥 NEW: Ajouter les nouvelles données
        "detected_language": detected_language,
        "medical_specialty": medical_specialty,
        "engagement": engagement_data,
        "detected_needs": detected_needs,
        "client_typology": client_typology,
        "proposed_product": proposed_product,
        "recommended_products": recommended_products,
        "visit_score": improved_visit_score,
        "report_date": datetime.now().isoformat(),
    }

    # ========================================


# 4.. DETECTION AUTOMATIQUE DE LA SPÉCIALITÉ
# ========================================


# ========================================
# 4A. NOUVELLES FONCTIONS D'EXTRACTION (AMÉLIORATIONS)
# ========================================


def detect_language(text: str) -> str:
    text_lower = text.lower()

    french_keywords = [
        "bonjour",
        "merci",
        "docteur",
        "médecin",
        "prix",
        "efficacité",
        "sécurité",
        "produit",
        "disponible",
        "remboursement",
        "étude",
        "données",
        "résultat",
        "oui",
        "très bien",
        "patients",
        "fatigue",
    ]

    english_keywords = [
        "hello",
        "thank",
        "doctor",
        "price",
        "efficacy",
        "safety",
        "product",
        "available",
        "study",
        "data",
        "result",
        "yes",
        "go ahead",
        "interesting",
        "immune",
        "immunity",
        "fatigue",
    ]

    arabic_pattern = re.compile(r"[\u0600-\u06FF]")

    fr_count = sum(1 for word in french_keywords if word in text_lower)
    en_count = sum(1 for word in english_keywords if word in text_lower)
    ar_count = len(arabic_pattern.findall(text))

    has_french = fr_count >= 2
    has_english = en_count >= 2
    has_arabic = ar_count >= 5

    detected_count = sum([has_french, has_english, has_arabic])

    if detected_count >= 2:
        return "MIXTE"
    if has_arabic:
        return "ARABE"
    if has_french:
        return "FRANÇAIS"
    if has_english:
        return "ANGLAIS"

    return "INCONNU"


def detect_medical_specialty(dialogue: str) -> str:
    """
    Détection intelligente de spécialité médicale (ML + multi-langue)
    """

    embedder = get_sentence_transformer()

    # 🧠 Descriptions multi-langues
    specialties = {
        "Cardiologie": [
            "cardiology heart cardiovascular treatment blood pressure",
            "cardiologie coeur traitement cardiovasculaire hypertension",
            "طب القلب علاج القلب ضغط الدم",
        ],
        "Dermatologie": [
            "dermatology skin eczema acne rash",
            "dermatologie peau eczéma acné dermatite",
            "طب الجلد الاكزيما حب الشباب",
        ],
        "Gastroentérologie": [
            "gastroenterology stomach digestion reflux intestine",
            "gastroentérologie estomac digestion reflux intestin",
            "طب الجهاز الهضمي المعدة الهضم",
        ],
        "Endocrinologie": [
            "endocrinology diabetes insulin glucose metabolism",
            "endocrinologie diabète insuline glycémie",
            "طب الغدد الصماء السكري الانسولين",
        ],
        "Pneumologie": [
            "pulmonology lungs asthma breathing cough",
            "pneumologie poumon asthme respiration toux",
            "طب الرئة التنفس الربو",
        ],
    }

    # 🔍 Encoder le dialogue
    dialogue_embedding = embedder.encode(dialogue, convert_to_numpy=True)

    best_specialty = "Médecine Générale"
    best_score = 0

    # 🔥 Comparaison embeddings
    for specialty, descriptions in specialties.items():
        for desc in descriptions:
            desc_embedding = embedder.encode(desc, convert_to_numpy=True)
            score = cosine_similarity(dialogue_embedding, desc_embedding)

            if score > best_score:
                best_score = score
                best_specialty = specialty

    # 🎯 seuil minimum
    if best_score < 0.3:
        return "Médecine Générale"

    return best_specialty


def detect_engagement(dialogue: str) -> dict:
    """
    Détecte si l'engagement est obtenu ou non
    Retourne: {"obtained": bool, "score": float, "indicators": []}
    """
    text_lower = dialogue.lower()

    positive_indicators = [
        "d'accord",
        "oui",
        "ok",
        "excellent",
        "parfait",
        "intéressé",
        "intéressant",
        "je vais",
        "on peut",
        "très bien",
        "c'est bon",
        "je prends",
        "envoyer",
        "me montrer",
        "je veux",
        "impressionné",
        "convaincu",
        "merveilleux",
        "formidable",
        "ok d'accord",
        "je suis d'accord",
    ]

    negative_indicators = [
        "non",
        "pas intéressé",
        "déjà",
        "trop cher",
        "plus tard",
        "pas besoin",
        "je n'ai pas",
        "je suis pressé",
        "pas convaincant",
        "doute",
        "inquiet",
        "pas sûr",
        "je verrai",
        "peut-être",
        "pas vraiment",
        "risque",
    ]

    positive_count = sum(
        1 for indicator in positive_indicators if indicator in text_lower
    )
    negative_count = sum(
        1 for indicator in negative_indicators if indicator in text_lower
    )

    # Score d'engagement
    total = positive_count + negative_count
    if total == 0:
        engagement_score = 0.5
    else:
        engagement_score = positive_count / total

    engagement_obtained = engagement_score > 0.6

    indicators = []
    for indicator in positive_indicators:
        if indicator in text_lower:
            indicators.append(f"✅ {indicator}")
    for indicator in negative_indicators:
        if indicator in text_lower:
            indicators.append(f"❌ {indicator}")

    return {
        "obtained": engagement_obtained,
        "score": float(engagement_score),
        "indicators": indicators[:5],  # Top 5 indicators
    }


def extract_detected_needs(dialogue: str) -> list:
    """
    Extrait les besoins/symptômes détectés dans la conversation
    Retourne: ["fatigue", "insomnie", "grippe", ...]
    """
    text_lower = dialogue.lower()

    # Dictionnaire des besoins/symptômes
    needs_dict = {
        "Fatigue": [
            "fatigue",
            "fatigué",
            "épuisé",
            "épuisement",
            "asthénie",
            "manque d'énergie",
            "faiblesse",
            "lassitude",
        ],
        "Insomnie": [
            "insomnie",
            "insomnies",
            "sommeil",
            "dormir",
            "nuits blanches",
            "trouble du sommeil",
            "réveil nocturne",
        ],
        "Grippe": [
            "grippe",
            "fièvre",
            "toux",
            "rhume",
            "virus",
            "viral",
            "courbatures",
            "syndrome grippal",
            "frissons",
        ],
        "Allergies": [
            "allergie",
            "allergique",
            "rhinite",
            "urticaire",
            "démangeaison",
            "prurit",
            "éternuement",
            "eczéma",
        ],
        "Arthrose": [
            "arthrose",
            "arthrite",
            "articulation",
            "douleur articulaire",
            "raideur",
            "inflammation",
            "gonflement",
        ],
        "Digestion": [
            "digestion",
            "digestif",
            "intestinal",
            "gastrique",
            "reflux",
            "ulcère",
            "ballonnement",
            "constipation",
            "diarrhée",
            "brûlure d'estomac",
        ],
        "Stress": [
            "stress",
            "stressé",
            "anxiété",
            "anxieux",
            "nervosité",
            "tension",
            "pression",
            "angoisse",
        ],
        "Douleur": [
            "douleur",
            "mal",
            "souffrance",
            "souffre",
            "douleurs",
            "migraine",
            "céphalée",
            "crampe",
        ],
        "Infection": [
            "infection",
            "infectieuse",
            "bactérienne",
            "virale",
            "microbe",
            "inflammation",
            "abcès",
        ],
        "Immunité": [
            "immunité",
            "immunitaire",
            "défense",
            "système immunitaire",
            "faible immunité",
            "renforcer",
            "protection",
        ],
    }

    detected_needs = []
    for need, keywords in needs_dict.items():
        for keyword in keywords:
            if keyword in text_lower and need not in detected_needs:
                detected_needs.append(need)
                break

    return detected_needs


def classify_client_typology(dialogue: str) -> dict:
    import unicodedata

    # 🔧 Normalisation texte
    def normalize(text):
        return (
            unicodedata.normalize("NFKD", text)
            .encode("ascii", "ignore")
            .decode("utf-8")
            .lower()
        )

    text = normalize(dialogue)

    # 🎯 Typologies avec poids
    typologies = {
        "Promouvant": {
            "keywords": {
                "meilleur": 2,
                "leader": 2,
                "innovant": 2,
                "premium": 2,
                "top": 1,
                "référence": 1,
                "prix": 1,
                "cher": 1,
            },
            "score": 0,
        },
        "Facilitant": {
            "keywords": {
                "sécurité": 2,
                "tolérance": 2,
                "confort": 2,
                "effets secondaires": 2,
                "bien": 1,
                "facile": 1,
            },
            "score": 0,
        },
        "Contrôlant": {
            "keywords": {
                "comment": 2,
                "pourquoi": 2,
                "explique": 2,
                "avez-vous": 2,
                "y a-t-il": 2,
                "quel est": 1,
                "quelles": 1,
                "détail": 1,
            },
            "score": 0,
        },
        "Analysant": {
            "keywords": {
                "étude": 2,
                "preuves": 2,
                "données": 2,
                "résultats": 2,
                "clinique": 2,
                "essai": 2,
            },
            "score": 0,
        },
    }

    # 🔍 1. Score par mots (pondéré)
    for typology in typologies:
        for keyword, weight in typologies[typology]["keywords"].items():
            if keyword in text:
                typologies[typology]["score"] += weight

    # 🔥 2. Détection intelligente des comportements

    # ➤ Questions = Contrôlant
    question_count = text.count("?")
    typologies["Contrôlant"]["score"] += min(question_count, 4) * 1.5

    # ➤ Données scientifiques = Analysant
    if any(word in text for word in ["données", "étude", "clinique", "essai"]):
        typologies["Analysant"]["score"] += 2

    # ➤ Sécurité = Facilitant
    if any(word in text for word in ["sécurité", "tolérance", "effets secondaires"]):
        typologies["Facilitant"]["score"] += 2

    # ➤ Prix / coût = Promouvant (dimension business)
    if any(word in text for word in ["prix", "cher", "coût"]):
        typologies["Promouvant"]["score"] += 1.5

    # 🔥 3. Équilibrage dynamique (important)
    scores = {k: v["score"] for k, v in typologies.items()}

    # éviter domination extrême
    max_score = max(scores.values()) if scores else 1
    for k in scores:
        scores[k] = scores[k] / (max_score + 1)

    # 🔥 4. Normalisation avec smoothing
    total = sum(scores.values())
    percentages = {}

    for k in scores:
        percentages[k] = round(((scores[k] + 0.1) / (total + 0.4)) * 100, 2)

    # 🎯 5. Profil dominant
    dominant_type = max(percentages, key=percentages.get)
    confidence = percentages[dominant_type] / 100

    return {
        "primary": dominant_type,
        "confidence": confidence,
        "all_types": percentages,
    }


def improve_visit_score(
    dialogue: str,
    objections_count: int = 0,
    engagement_score: float = 0.5,
    sentiment: float = 0,
) -> float:
    """
    Améliore le calcul du score de visite - dynamique selon la discussion
    Prend en compte: sentiment, engagement, objections, longueur, questions, mots-clés positifs
    """
    base_score = 50

    # 1. SENTIMENT (±20 points)
    if sentiment > 0.7:
        base_score += 20
    elif sentiment > 0.4:
        base_score += 12
    elif sentiment > 0:
        base_score += 5
    elif sentiment < -0.7:
        base_score -= 20
    elif sentiment < -0.4:
        base_score -= 12
    elif sentiment < 0:
        base_score -= 5

    # 2. ENGAGEMENT (±25 points)
    if engagement_score > 0.8:
        base_score += 25
    elif engagement_score > 0.6:
        base_score += 15
    elif engagement_score > 0.4:
        base_score += 8
    elif engagement_score < 0.2:
        base_score -= 20

    # 3. OBJECTIONS - pénalité mais diminuée si bien gérées (0 à -15)
    if objections_count == 0:
        base_score += 5  # Bonus si aucune objection
    else:
        objection_malus = min(objections_count * 2, 15)
        base_score -= objection_malus

    # 4. LONGUEUR DIALOGUE - engagement (+10 points max)
    dialogue_length = len(dialogue.split())
    if dialogue_length > 500:
        base_score += 10
    elif dialogue_length > 300:
        base_score += 6
    elif dialogue_length > 150:
        base_score += 3

    # 5. QUESTIONS DU MEDECIN - engagement (+15 points max)
    question_count = dialogue.lower().count("?")
    base_score += min(question_count * 1.5, 15)

    # 6. MOTS-CLÉS POSITIFS (+20 points max)
    positive_keywords = [
        "intéressant", "excellent", "bon", "oui", "d'accord", "effectivement",
        "absolument", "ça me plaît", "bien sûr", "parfait", "test", "tester",
        "ok", "d'accord", "considérer", "envisager", "prescrire"
    ]
    positive_count = sum(1 for keyword in positive_keywords if keyword in dialogue.lower())
    base_score += min(positive_count * 1.5, 20)

    # 7. MOTS-CLÉS NÉGATIFS (-15 points max)
    negative_keywords = [
        "trop cher", "pas intéressé", "non", "pas besoin", "doute", "risque",
        "danger", "dangereux", "effet secondaire", "problème", "jam", "jamais"
    ]
    negative_count = sum(1 for keyword in negative_keywords if keyword in dialogue.lower())
    base_score -= min(negative_count * 2, 15)

    # 8. MOTS-CLÉS DE CONSENSUS - accord final (+10 points)
    consensus_keywords = ["approuver", "accord", "consensus", "validé", "convenus"]
    consensus_found = any(keyword in dialogue.lower() for keyword in consensus_keywords)
    if consensus_found:
        base_score += 10

    # Clamper entre 0 et 100
    final_score = max(0, min(100, base_score))
    print(f"[SCORE DEBUG] Dialogue length: {dialogue_length} | Objections: {objections_count} | Sentiment: {sentiment:.2f} | Engagement: {engagement_score:.2f} | Final: {final_score}")
    return float(final_score)


# ========================================
# 4B. SAUVEGARDE RAPPORT
# ========================================
def save_rapport(rapport: dict) -> str:
    """
    Sauvegarde le rapport en JSON et retourne le chemin

    Returns:
        Chemin du fichier sauvegardé
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"rapport_{timestamp}.json"
    filepath = RAPPORTS_DIR / filename

    # Convertir les objets complexes en sérialisables
    rapport_serializable = {
        "timestamp": timestamp,
        "type": rapport.get("type"),
        "analysis": rapport.get("analysis"),
        "key_points": rapport.get("key_points"),
        "objections": [
            {
                "type": obj["type"],
                "text": obj["text"],
                "strategy": obj["strategy"],
                "sources_count": len(obj.get("sources", [])),
            }
            for obj in rapport.get("objections", [])
        ],
        "sources_count": len(rapport.get("sources", [])),
        "exchanges_count": len(rapport.get("exchanges", [])),
        # 🔥 NEW: Ajouter les nouvelles données
        "detected_language": rapport.get("detected_language"),
        "medical_specialty": rapport.get("medical_specialty"),
        "engagement": rapport.get("engagement"),
        "detected_needs": rapport.get("detected_needs"),
        "client_typology": rapport.get("client_typology"),
        "proposed_product": rapport.get("proposed_product"),
        "visit_score": rapport.get("visit_score"),
        "report_date": rapport.get("report_date"),
    }

    # Sauvegarder
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(rapport_serializable, f, ensure_ascii=False, indent=2)

    return str(filepath)


# ========================================
# 4C. LISTER LES RAPPORTS SAUVEGARDÉS
# ========================================
def list_saved_rapports() -> list:
    """Liste tous les rapports sauvegardés"""
    if not RAPPORTS_DIR.exists():
        return []

    rapports = []
    for file in sorted(RAPPORTS_DIR.glob("rapport_*.json"), reverse=True):
        rapports.append(
            {"filename": file.name, "path": str(file), "created": file.stat().st_mtime}
        )
    return rapports


# ========================================
# 5. ANCIENNES FONCTIONS (COMPATIBILITÉ)
# ========================================
def generate_product_report(category: str = None) -> dict:
    """Rapport complet sur les produits"""
    from services.rag_service import rag_query

    query = (
        f"Produits de la catégorie {category}"
        if category
        else "Tous les produits disponibles"
    )

    rag_result = rag_query(query, top_k=10)

    return {
        "type": "Product Report",
        "category": category,
        "summary": rag_result["response"],
        "sources": rag_result["sources"],
    }


def generate_objection_analysis(objection_type: str) -> dict:
    """Analyser les objections récurrentes"""
    from services.rag_service import rag_query

    query = f"Comment répondre à une objection de type: {objection_type}"

    rag_result = rag_query(query, top_k=5)

    return {
        "type": "Objection Analysis",
        "objection": objection_type,
        "strategies": rag_result["response"],
        "references": rag_result["sources"],
    }


# ========================================
# TEST
# ========================================
if __name__ == "__main__":
    test_dialogue = """
DÉLÉGUÉ: Bonjour docteur, comment allez-vous?
MÉDECIN: Bien merci, que me proposez-vous?
DÉLÉGUÉ: Nous avons un nouveau produit pour la cardiologie
MÉDECIN: Intéressant, mais quel est le prix?
DÉLÉGUÉ: C'est 45 euros par boîte
MÉDECIN: C'est cher comparé à nos produits actuels
DÉLÉGUÉ: D'accord, mais les études montrent 30% plus d'efficacité
MÉDECIN: Avez-vous les données cliniques?
DÉLÉGUÉ: Oui, voici les résultats
MÉDECIN: Et la disponibilité? Avez-vous du stock?
    """

    result = analyze_conversation(test_dialogue, rapport_type="Analyse Objections")

    print("=" * 60)
    print("RAPPORT GÉNÉRÉ")
    print("=" * 60)
    print(f"\nType: {result['type']}")
    print(f"\nAnalyse:\n{result['analysis']}")
    print(f"\n\nPoints Clés:")
    for k, v in result["key_points"].items():
        print(f"  {k}: {v}")
    print(f"\n\nObjections ({len(result['objections'])} trouvées):")
    for i, obj in enumerate(result["objections"], 1):
        print(f"  {i}. {obj['type']}: {obj['text'][:100]}...")
