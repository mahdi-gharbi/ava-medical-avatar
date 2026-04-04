"""
rag/ingest.py
-------------
Charge tous les documents VITAL (JSON), les découpe en chunks,
génère les embeddings et les stocke dans ChromaDB.

Version harmonisée pour projet commun BO1 + BO2 :
- garde la structure multi-collections de ingest.py
- ajoute la compatibilité avec l'ancien build_db.py
  (metadata 'produit', fallback 'highlights', champ 'Utilisation')

Lancer UNE FOIS :
    python rag/ingest.py
"""

import json
import chromadb
from chromadb.utils import embedding_functions
from pathlib import Path

# ── Config ───────────────────────────────────────────────────────────────────
DATA_DIR = Path(__file__).parent.parent.parent / "data"
CHROMA_DIR = Path(__file__).parent.parent / "chroma_db"

# Embedding model (local, gratuit, ~90 Mo)
EMBED_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"  # supporte le français

# ── ChromaDB client ───────────────────────────────────────────────────────────
client = chromadb.PersistentClient(path=str(CHROMA_DIR))
emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=EMBED_MODEL
)


def get_or_create_collection(name: str):
    return client.get_or_create_collection(
        name=name,
        embedding_function=emb_fn,
        metadata={"hnsw:space": "cosine"},
    )


# ── Helpers ───────────────────────────────────────────────────────────────────
def load_json(filename: str):
    with open(DATA_DIR / filename, encoding="utf-8") as f:
        return json.load(f)


def to_list_str(val) -> str:
    """
    Convertit n'importe quelle valeur (list, str, None, autre) en string joignable.
    Sécurise les champs JSON inconsistants du scraping.
    """
    if isinstance(val, list):
        return ", ".join([str(v) for v in val if v])
    elif isinstance(val, str):
        return val.strip()
    elif val is None:
        return ""
    else:
        return str(val)


def safe_meta(meta: dict) -> dict:
    """
    ChromaDB n'accepte que str, int, float, bool dans les métadonnées.
    Cette fonction convertit toute valeur non-conforme en string.
    """
    clean = {}
    for k, v in meta.items():
        if isinstance(v, (str, int, float, bool)):
            clean[k] = v
        elif v is None:
            clean[k] = ""
        else:
            clean[k] = str(v)
    return clean


def add_documents(collection, docs: list[dict], ids: list[str], metadatas: list[dict]):
    """
    Ajoute des documents en évitant les doublons.
    Si un id existe déjà, on ne le réinsère pas.
    """
    texts = [d["text"] for d in docs]
    existing = collection.get(ids=ids)["ids"]

    new_ids, new_texts, new_meta = [], [], []
    for doc_id, text, meta in zip(ids, texts, metadatas):
        if doc_id not in existing:
            new_ids.append(doc_id)
            new_texts.append(text)
            new_meta.append(safe_meta(meta))

    if new_ids:
        collection.add(documents=new_texts, ids=new_ids, metadatas=new_meta)
        print(f"  ✅ {len(new_ids)} chunks ajoutés dans '{collection.name}'")
    else:
        print(f"  ℹ️  Tous les chunks existent déjà dans '{collection.name}'")


# ── 1. Catalogue produits ─────────────────────────────────────────────────────
def ingest_products():
    col = get_or_create_collection("products")
    products = load_json("parapharmacie_vital_final_v2.json")

    docs, ids, metas = [], [], []

    for i, p in enumerate(products):
        # Compatibilité build_db.py :
        # - benefits possible via "benefices" OU "highlights"
        # - metadata "produit" ajoutée
        benefices = p.get("benefices", p.get("highlights", []))

        text = f"""Produit: {p.get('name', '')}
Gamme: {p.get('gamme', '')}
Catégories: {to_list_str(p.get('categories', []))}
Indications: {to_list_str(p.get('indications', []))}
Description: {p.get('description', '')}
Bénéfices: {to_list_str(benefices)}
Composition: {to_list_str(p.get('compositions', []))}
Posologie: {to_list_str(p.get('posologie_detaillee', []))}
Contre-indications: {to_list_str(p.get('contre_indications', []))}
Utilisation: complément alimentaire
"""

        docs.append({"text": text})
        ids.append(f"prod_{i}")
        metas.append({
            "source": "catalogue_vital",
            "name": p.get("name", f"produit_{i}"),
            "produit": p.get("name", f"produit_{i}"),   # compatibilité BO2 / dynamic_rag
            "gamme": p.get("gamme", ""),
            "type": "product",
            "categories": to_list_str(p.get("categories", [])),
        })

    add_documents(col, docs, ids, metas)


# ── 2. Scripts Top Sellers ────────────────────────────────────────────────────
def ingest_scripts():
    col = get_or_create_collection("scripts")
    scripts = load_json("scripts_top_sellers.json")

    docs, ids, metas = [], [], []

    for i, s in enumerate(scripts):
        objections_text = "\n".join(
            [
                f"  - Objection: {o.get('objection', '')} | "
                f"Clarifier: {o.get('clarifier', '')} | "
                f"Réponse: {o.get('reponse', '')}"
                for o in s.get("objections", [])
            ]
        )

        questions_decouverte = s.get("questions_decouverte", [])
        if not isinstance(questions_decouverte, list):
            questions_decouverte = [str(questions_decouverte)]

        text = f"""Produit: {s.get('produit', '')}
Catégorie: {s.get('categorie', '')}
Spécialités: {to_list_str(s.get('specialites', []))}
Message cœur: {s.get('message_coeur', '')}
Cibles: {to_list_str(s.get('cibles', []))}
Questions découverte: {' | '.join([str(q) for q in questions_decouverte if q])}
Argumentation: {to_list_str(s.get('argumentation', []))}
Script Flash: {s.get('scripts', {}).get('flash', '')}
Script Standard: {s.get('scripts', {}).get('standard', '')}
Objections et réponses:
{objections_text}
Suivi CRM: {s.get('suivi_crm', '')}
"""

        docs.append({"text": text})
        ids.append(f"script_{i}")
        metas.append({
            "source": "scripts_top_sellers",
            "produit": s.get("produit", f"script_{i}"),
            "name": s.get("produit", f"script_{i}"),
            "type": "script",
            "specialites": to_list_str(s.get("specialites", [])),
            "categorie": s.get("categorie", ""),
        })

    add_documents(col, docs, ids, metas)


# ── 3. Manuel visite (process + méthodes) ────────────────────────────────────
def ingest_manuel():
    col = get_or_create_collection("methodology")
    manuel = load_json("manuel_visite.json")

    docs, ids, metas = [], [], []

    # Chunk par étape du process
    for i, etape in enumerate(manuel.get("process_visite", {}).get("etapes", [])):
        text = f"""Étape {etape.get('numero', '')}: {etape.get('nom', '')}
Objectif: {etape.get('objectif', '')}
"""

        if "script_standard" in etape:
            text += f"Script: {etape['script_standard']}\n"
        if "phrase_type" in etape:
            text += f"Phrase type: {etape['phrase_type']}\n"
        if "methode" in etape:
            for k, v in etape["methode"].items():
                text += f"  {k}: {v}\n"
        if "objections_frequentes" in etape:
            for obj in etape["objections_frequentes"]:
                text += f"  Objection: {obj.get('objection', '')} → {obj.get('reponse', '')}\n"

        docs.append({"text": text})
        ids.append(f"etape_{etape.get('numero', i)}")
        metas.append({
            "source": "manuel_visite",
            "type": "process_step",
            "etape": etape.get("nom", ""),
        })

    # Chunk formats de visite
    for fmt, details in manuel.get("formats_visite", {}).items():
        text = f"""Format de visite: {fmt.upper()}
Durée: {details.get('duree', '')}
Structure: {details.get('structure', '')}
"""
        docs.append({"text": text})
        ids.append(f"format_{fmt}")
        metas.append({
            "source": "manuel_visite",
            "type": "visit_format",
            "format": fmt
        })

    # Chunk typologies médecins
    typologies = manuel.get("typologies_medecins", {})
    text = "Typologies de médecins (4 styles):\n"
    for style, desc in typologies.get("4_styles", {}).items():
        text += f"  - {style.capitalize()}: {desc}\n"

    text += "\nSONCAS (leviers d'argumentation):\n"
    for key, desc in typologies.get("soncas", {}).items():
        text += f"  - {key}: {desc}\n"

    docs.append({"text": text})
    ids.append("typologies_medecins")
    metas.append({
        "source": "manuel_visite",
        "type": "doctor_profiles"
    })

    # Chunk grille évaluation
    grille = manuel.get("grille_evaluation", {})
    text = "Grille d'évaluation ALIA (14 critères):\n"
    for c in grille.get("criteres", []):
        text += f"  {c.get('id', '')}. {c.get('nom', '')} (poids: {c.get('poids', '')})\n"

    docs.append({"text": text})
    ids.append("grille_evaluation")
    metas.append({
        "source": "manuel_visite",
        "type": "evaluation_grid"
    })

    add_documents(col, docs, ids, metas)


# ── 4. Niveaux de compétence ──────────────────────────────────────────────────
def ingest_niveaux():
    col = get_or_create_collection("competence_levels")
    niveaux = load_json("niveaux_competence.json")

    docs, ids, metas = [], [], []

    for n in niveaux:
        competences = n.get("competences", [])
        limites = n.get("limites", [])

        if not isinstance(competences, list):
            competences = [str(competences)]
        if not isinstance(limites, list):
            limites = [str(limites)]

        text = f"""Niveau ALIA: {n.get('niveau', '')} ({n.get('code', '')})
Profil: {n.get('profil', '')}
Compétences attendues:
{chr(10).join(['  - ' + str(c) for c in competences])}
Limites:
{chr(10).join(['  - ' + str(l) for l in limites])}
KPI: {json.dumps(n.get('kpi', {}), ensure_ascii=False)}
"""

        docs.append({"text": text})
        ids.append(f"niveau_{n.get('code', 'unknown')}")
        metas.append({
            "source": "niveaux_competence",
            "type": "competence_level",
            "niveau": n.get("niveau", ""),
            "code": n.get("code", ""),
        })

    add_documents(col, docs, ids, metas)

# ── 5. Global Docs (partagé entre tous les BO) ───────────────────────────────
def ingest_global_docs(data):
    col = get_or_create_collection("global_docs")

    docs, ids, metas = [], [], []

    for i, item in enumerate(data):

        text = f"""
Titre: {item.get("title", "")}
Contenu: {item.get("content", "")}
Source: upload_streamlit
"""

        docs.append({"text": text})
        ids.append(f"global_{i}")

        metas.append({
            "source": "global_docs",
            "type": "shared_knowledge",
            "title": item.get("title", f"doc_{i}")
        })

    add_documents(col, docs, ids, metas)
# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("🚀 Ingestion RAG ALIA — VITAL SA")
    print("=" * 50)

    print("\n📦 1. Catalogue produits...")
    ingest_products()

    print("\n📋 2. Scripts Top Sellers...")
    ingest_scripts()

    print("\n📖 3. Manuel visite (méthodologie)...")
    ingest_manuel()

    print("\n🎯 4. Niveaux de compétence...")
    ingest_niveaux()
    print("\n✅ Ingestion terminée !")
    print(f"   Base vectorielle sauvegardée dans : {CHROMA_DIR}")