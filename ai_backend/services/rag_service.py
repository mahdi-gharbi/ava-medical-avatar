# ========================================
# RAG SERVICE avec GROQ + CHROMA
# ========================================
import os
from groq import Groq
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
CHROMA_PATH = os.getenv("CHROMA_PATH", "ai_backend/rag/chroma_db")

# ========================================
# Initialiser Groq Client
# ========================================
groq_client = Groq(api_key=GROQ_API_KEY)

# ========================================
# Initialiser Chroma et Embedding
# ========================================
# NOTE PERF: On désactive l'usage du modèle fine-tuné pour éviter des chargements
# lourds et des latences. Un seul modèle standard est utilisé partout.
EMBED_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"

# Cache global du modèle standard (utilisé uniquement si on fait du scoring côté python)
_standard_model_cache = None


def get_standard_model() -> SentenceTransformer:
    global _standard_model_cache
    if _standard_model_cache is None:
        _standard_model_cache = SentenceTransformer(EMBED_MODEL)
    return _standard_model_cache


emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBED_MODEL)

chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)


def _get_collection(name: str):
    """Récupère une collection Chroma avec embedding function (nécessaire pour query_texts)."""
    try:
        return chroma_client.get_collection(name, embedding_function=emb_fn)
    except TypeError:
        # Compatibilité avec anciennes versions de chromadb
        return chroma_client.get_collection(name)

# ========================================
# RETRIEVER : Chercher dans Chroma (AMÉLIORÉ)
# ========================================
def retrieve_context(query: str, top_k: int = 5, use_finetuned: bool = False) -> list[dict]:
    """
    Cherche les documents pertinents dans Chroma.
    NOTE: le paramètre use_finetuned est conservé pour compatibilité API,
    mais est ignoré (finetuned désactivé pour performance).
    
    Args:
        query: Question utilisateur
        top_k: Nombre de résultats
        use_finetuned: Conservé pour compatibilité; finetuned est désactivé et ignoré.
    
    Returns:
        Liste de documents avec scores recalculés par le modèle d'embedding sélectionné
    """
    if use_finetuned:
        print("⚠️  use_finetuned=True ignoré (finetuned désactivé pour performance).")
    print("🔹 [STANDARD] Retrieving context with STANDARD embeddings")
    
    # 🔥 ENRICHIR la requête pour mieux matcher
    enriched_queries = [
        query,  # Original
        f"{query} produit médical cardiologie",  # Contexte medical
        f"{query} efficacité sécurité données cliniques",  # Données
        f"{query} prix coût remboursement CNAM",  # Economics
    ]
    
    all_results = []
    seen_ids = {}
    
    # Collections à chercher
    collection_names = ["products"]
    try:
        chroma_client.get_collection("bo5_data")
        collection_names.append("bo5_data")
    except:
        pass

    # 🔥 NEW: case-based reasoning (visites historiques) si collection existante
    try:
        chroma_client.get_collection("bo6_visits")
        collection_names.append("bo6_visits")
    except:
        pass
    
    # Chercher dans les collections
    for col_name in collection_names:
        try:
            col = _get_collection(col_name)
            
            # Chercher avec plusieurs variantes de requête
            for enriched_query in enriched_queries:
                results = col.query(
                    query_texts=[enriched_query],
                    n_results=top_k * 3,  # Get more to re-rank
                    include=["documents", "metadatas", "distances"]
                )
                
                if not results or not results.get("ids") or not results["ids"][0]:
                    continue
                
                for i, doc in enumerate(results["documents"][0]):
                    doc_id = f"{col_name}_{results['ids'][0][i]}"
                    
                    original_score = 1 - float(results["distances"][0][i])
                    metadata = results["metadatas"][0][i] if results["metadatas"] else {}

                    # Éviter doublons: garder le meilleur score si revu via enriched_queries
                    prev = seen_ids.get(doc_id)
                    if prev is None or original_score > prev["original_score"]:
                        seen_ids[doc_id] = {
                            "id": doc_id,
                            "content": doc,
                            "metadata": metadata,
                            "original_score": original_score,
                            "score": original_score,
                            "source": col_name,
                        }
        except Exception as e:
            print(f"⚠️  Collection '{col_name}' not available: {str(e)}")
            continue

    all_results = list(seen_ids.values())
    all_results = sorted(all_results, key=lambda x: x["score"], reverse=True)[:top_k]
    if all_results:
        avg_score = sum(r["score"] for r in all_results) / len(all_results)
        print(f"📊 Retrieved {len(all_results)} docs (avg score: {avg_score:.3f})")
    return all_results

# ========================================
# GENERATOR : Appeler Groq LLM
# ========================================
def generate_response(
    query: str,
    context_docs: list[dict],
    system_prompt: str = None
) -> str:
    """
    Génère une réponse avec Groq LLM + contexte
    
    Args:
        query: Question utilisateur
        context_docs: Documents récupérés
        system_prompt: Instruction personnalisée
    
    Returns:
        Réponse générée par Llama 3.3
    """
    # Formater le contexte
    context_text = "\n".join([
        f"- {doc['content'][:500]}"
        for doc in context_docs
    ])
    
    # Prompt par défaut
    if system_prompt is None:
        system_prompt = """Tu es un assistant IA spécialisé en recommandations médicales.
Utilise les documents fournis pour répondre précisément.
Sois concis et professionnel."""
    
    # Message à Groq
    user_message = f"""CONTEXTE:
{context_text}

QUESTION:
{query}

Réponds en te basant uniquement sur le contexte fourni."""
    
    # Appel Groq (chat.completions.create, pas messages.create)
    message = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        max_tokens=1024,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    )
    
    return message.choices[0].message.content

# ========================================
# RAG PIPELINE
# ========================================
def rag_query(query: str, top_k: int = 5) -> dict:
    """
    Pipeline RAG complet:
    1. Recherche contexte dans Chroma
    2. Génère réponse avec Groq LLM
    """
    # Retrieve
    context = retrieve_context(query, top_k=top_k)
    
    # Generate
    response = generate_response(query, context)
    
    return {
        "query": query,
        "response": response,
        "sources": [
            {
                "content": doc["content"][:200] + "...",
                "score": doc["score"]
            }
            for doc in context
        ]
    }

# ========================================
# TEST
# ========================================
if __name__ == "__main__":
    result = rag_query("Quels produits pour la cardiologie ?")
    print("Query:", result["query"])
    print("\nResponse:", result["response"])
    print("\nSources:", result["sources"])