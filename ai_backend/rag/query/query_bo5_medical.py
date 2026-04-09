# ========================================
# QUERY BO5 - Analyse Visite Médicale
# ========================================
import os
import re
import sys
import json
import pandas as pd
from pathlib import Path
from datetime import datetime

# ========================================
# FIX PATHS
# ========================================
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
                exchanges.append({"speaker": current_speaker, "text": current_text.strip()})
            current_speaker = "DÉLÉGUÉ"
            current_text = line.split(":", 1)[1] if ":" in line else ""
            delegue_text.append(current_text)
        
        elif line.upper().startswith("MÉDECIN:") or line.upper().startswith("MEDECIN:") or line.upper().startswith("DOCTOR:"):
            if current_speaker and current_text:
                exchanges.append({"speaker": current_speaker, "text": current_text.strip()})
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
        "full_dialogue": dialogue
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
            "type": "Price Objection"
        },
        "safety": {
            "keywords": ["effets secondaires", "safety", "tolérance", "tolerance", "sécurité", "side effects", "adverse"],
            "type": "Safety Concern"
        },
        "efficacy": {
            "keywords": ["efficacité", "efficacy", "étude", "study", "evidence", "preuve", "results"],
            "type": "Efficacy Question"
        },
        "stock": {
            "keywords": ["stock", "disponible", "availability", "grossiste", "available"],
            "type": "Stock/Availability"
        },
        "reimbursement": {
            "keywords": ["cnam", "reimbursement", "remboursement", "couverture", "coverage"],
            "type": "Reimbursement"
        }
    }
    
    text_lower = dialogue_text.lower()
    detected = []
    detected_types = set()  # 🔥 ÉVITER DOUBLONS
    
    for key, pattern in objection_patterns.items():
        for keyword in pattern["keywords"]:
            if keyword in text_lower and pattern["type"] not in detected_types:
                # Extraire le contexte (phrase contenant le keyword)
                sentences = re.split(r'[.!?]', dialogue_text)
                for sentence in sentences:
                    if keyword in sentence.lower():
                        detected.append({
                            "type": pattern["type"],
                            "text": sentence.strip(),
                            "keyword": keyword
                        })
                        detected_types.add(pattern["type"])  # 🔥 Marquer comme trouvé
                        break
                break  # 🔥 Passer à l'objection suivante
    
    return detected


# ========================================
# 3. STRATÉGIES D'OBJECTIONS (AMÉLIORÉ)
# ========================================
def get_objection_strategies(objection_type: str, context_docs: list, dialogue: str = "") -> str:
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

Sois informatif et encourageant."""
    }
    
    system_prompt = strategies_prompts.get(objection_type, strategies_prompts["Price Objection"])
    
    context_text = "\n".join([
        f"📌 {doc['content'][:400]}"
        for doc in context_docs[:3]  # Top 3 seulement
    ])
    
    query = f"""Dialogue récent:
{dialogue[-500:] if dialogue else "Contexte général"}

Contexte de la base de données:
{context_text}

Génère une stratégie de réponse professionnelle et persuasive."""
    
    strategy = generate_response(query, context_docs, system_prompt)
    
    return strategy


# ========================================
# 4. ANALYSE COMPLÈTE
# ========================================
def analyze_conversation(
    dialogue: str,
    rapport_type: str = "Analyse Objections",
    top_k: int = 5
) -> dict:
    """
    Pipeline complet d'analyse d'une visite médicale
    """
    
    # Parser la conversation
    parsed = parse_conversation(dialogue)
    exchanges = parsed["exchanges"]
    
    # Détecter objections
    objections = detect_objections(dialogue)
    
    # Récupérer contexte pour chaque objection
    enriched_objections = []
    for obj in objections:
        context = retrieve_context(obj["text"], top_k=top_k)
        
        # 🔥 FILTRER: Garder SEULEMENT les sources avec bon score
        context = [c for c in context if c["score"] > 0.3]
        
        if not context:
            continue  # Passer si pas de bon contexte
        
        # 🔥 AMÉLIORATION: Passer le dialogue complet pour meilleur contexte
        strategy = get_objection_strategies(
            obj["type"], 
            context,
            dialogue=dialogue  # ← Dialogue entier
        )
        
        enriched_objections.append({
            "type": obj["type"],
            "text": obj["text"],
            "strategy": strategy,
            "sources": context
        })
    
    # Générer analyse globale
    analysis_query = f"""Analysez cette visite médicale et générez un rapport {rapport_type}:
    
Dialogue:
{dialogue}

Objections détectées: {len(objections)}
"""
    
    context = retrieve_context(dialogue[:500], top_k=top_k)
    
    # 🔥 FILTRER: Garder seulement les sources avec bon score
    context = [c for c in context if c["score"] > 0.3]
    
    # Si Chroma est vide, créer un contexte par défaut
    if not context:
        context = [{
            "content": "Aucun document pertinent trouvé dans la base. Génération avec contexte générique.",
            "score": 0.0
        }]
    
    analysis = generate_response(
        analysis_query,
        context,
        system_prompt="""Tu es un analyseur expert en visites médicales.
Analyse le dialogue et fournis:
1. Points clés de la visite
2. Objections majeures
3. Opportunités
4. Recommandations"""
    )
    
    return {
        "type": rapport_type,
        "analysis": analysis,
        "objections": enriched_objections,
        "sources": context,
        "key_points": {
            "Total Exchanges": len(exchanges),
            "Objections Found": len(objections),
            "Délégué Messages": len([e for e in exchanges if e["speaker"] == "DÉLÉGUÉ"]),
            "Médecin Messages": len([e for e in exchanges if e["speaker"] == "MÉDECIN"])
        },
        "exchanges": exchanges
    }


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
                "sources_count": len(obj.get("sources", []))
            }
            for obj in rapport.get("objections", [])
        ],
        "sources_count": len(rapport.get("sources", [])),
        "exchanges_count": len(rapport.get("exchanges", []))
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
        rapports.append({
            "filename": file.name,
            "path": str(file),
            "created": file.stat().st_mtime
        })
    return rapports


# ========================================
# 5. ANCIENNES FONCTIONS (COMPATIBILITÉ)
# ========================================
def generate_product_report(category: str = None) -> dict:
    """Rapport complet sur les produits"""
    from services.rag_service import rag_query
    
    query = f"Produits de la catégorie {category}" if category else "Tous les produits disponibles"
    
    rag_result = rag_query(query, top_k=10)
    
    return {
        "type": "Product Report",
        "category": category,
        "summary": rag_result["response"],
        "sources": rag_result["sources"]
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
        "references": rag_result["sources"]
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
