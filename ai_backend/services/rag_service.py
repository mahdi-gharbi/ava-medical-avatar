# ========================================
# RAG SERVICE avec GROQ + CHROMA
# ========================================
import os
from groq import Groq
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
from pathlib import Path
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from functools import lru_cache

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
EMBED_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"
AI_BACKEND_DIR = Path(__file__).parent.parent
FINETUNED_MODEL_PATH = AI_BACKEND_DIR / "models" / "finetuned_sentence_transformer"

# Cache models globally to avoid reloading
_finetuned_model_cache = None
_standard_model_cache = None

def get_finetuned_model():
    """Retourne le modèle fine-tuné chargé en cache"""
    global _finetuned_model_cache
    if _finetuned_model_cache is None:
        try:
            if (FINETUNED_MODEL_PATH / "model.safetensors").exists() or (FINETUNED_MODEL_PATH / "pytorch_model.bin").exists():
                _finetuned_model_cache = SentenceTransformer(str(FINETUNED_MODEL_PATH))
            else:
                _finetuned_model_cache = SentenceTransformer(EMBED_MODEL)
        except Exception as e:
            print(f"[ERROR] Failed to load fine-tuned model: {e}")
            _finetuned_model_cache = SentenceTransformer(EMBED_MODEL)
    return _finetuned_model_cache

def get_standard_model():
    """Retourne le modèle standard chargé en cache"""
    global _standard_model_cache
    if _standard_model_cache is None:
        _standard_model_cache = SentenceTransformer(EMBED_MODEL)
    return _standard_model_cache

# Load models once at startup (if accessed directly, not through Streamlit)
# Lazy loading - only load when actually needed via get_finetuned_model() / get_standard_model()
# finetuned_model and standard_model will be set in retrieve_context() when first called

# Créer fonction d'embedding adaptée
def get_embedding_function():
    """Retourne la fonction d'embedding fine-tuné si elle existe, sinon standard"""
    if (FINETUNED_MODEL_PATH / "model.safetensors").exists() or (FINETUNED_MODEL_PATH / "pytorch_model.bin").exists():
        return embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=str(FINETUNED_MODEL_PATH)
        )
    else:
        return embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=EMBED_MODEL
        )

def get_standard_embedding_function():
    """Retourne TOUJOURS la fonction d'embedding standard (non fine-tuné)"""
    return embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBED_MODEL
    )

# Créer deux clients Chroma distincts avec des embedding functions différentes
# Cela permet de requêter la même collection avec différents modèles d'embedding
emb_fn = get_embedding_function()
standard_emb_fn = get_standard_embedding_function()

chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

# Collections avec fine-tuned embeddings
collection = chroma_client.get_or_create_collection(
    name="global_docs",
    embedding_function=emb_fn,
    metadata={"hnsw:space": "cosine"}
)

# Collections avec standard embeddings  
standard_collection = chroma_client.get_or_create_collection(
    name="global_docs_standard",
    embedding_function=standard_emb_fn,
    metadata={"hnsw:space": "cosine"}
)

# Pour l'A/B testing: créer deux clients séparés pour requêter "products" avec différents embeddings
chroma_client_finetuned = chromadb.PersistentClient(path=CHROMA_PATH)
chroma_client_standard = chromadb.PersistentClient(path=CHROMA_PATH)

# ========================================
# RETRIEVER : Chercher dans Chroma (AMÉLIORÉ)
# ========================================
def retrieve_context(query: str, top_k: int = 5, use_finetuned: bool = True) -> list[dict]:
    """
    Cherche les documents pertinents dans Chroma avec re-ranking par embeddings
    Permet véritable A/B testing en changeant le modèle d'embedding pour le scoring
    
    Args:
        query: Question utilisateur
        top_k: Nombre de résultats
        use_finetuned: Si True, utilise fine-tuned embeddings. Si False, utilise standard embeddings
    
    Returns:
        Liste de documents avec scores recalculés par le modèle d'embedding sélectionné
    """
    # Sélectionner le modèle d'embedding avec cache
    embed_model = get_finetuned_model() if use_finetuned else get_standard_model()
    model_type = "FINETUNED" if use_finetuned else "STANDARD"
    print(f"🔹 [{model_type}] Retrieving context with {model_type} embeddings")
    
    # 🔥 ENRICHIR la requête pour mieux matcher
    enriched_queries = [
        query,  # Original
        f"{query} produit médical cardiologie",  # Contexte medical
        f"{query} efficacité sécurité données cliniques",  # Données
        f"{query} prix coût remboursement CNAM",  # Economics
    ]
    
    all_results = []
    seen_ids = set()
    
    # Collections à chercher
    collection_names = ["products"]
    try:
        chroma_client.get_collection("bo5_data")
        collection_names.append("bo5_data")
    except:
        pass
    
    # Chercher dans les collections
    for col_name in collection_names:
        try:
            col = chroma_client.get_collection(col_name)
            
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
                    
                    # Éviter doublons
                    if doc_id in seen_ids:
                        continue
                    seen_ids.add(doc_id)
                    
                    all_results.append({
                        "id": doc_id,
                        "content": doc,
                        "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                        "original_score": 1 - float(results["distances"][0][i]),
                        "source": col_name
                    })
        except Exception as e:
            print(f"⚠️  Collection '{col_name}' not available: {str(e)}")
            continue
    
    # 🔥 RE-RANK all results using the selected embedding model
    if all_results:
        try:
            # Encode query with selected model
            query_embedding = embed_model.encode(query)
            
            # Re-score each result
            for result in all_results:
                doc_embedding = embed_model.encode(result["content"])
                # Compute cosine similarity
                similarity = cosine_similarity(
                    query_embedding.reshape(1, -1),
                    doc_embedding.reshape(1, -1)
                )[0][0]
                result["score"] = float(similarity)
            
            # Re-rank by new score
            all_results = sorted(all_results, key=lambda x: x["score"], reverse=True)[:top_k]
            
            avg_score = sum(r["score"] for r in all_results) / len(all_results)
            print(f"📊 Retrieved {len(all_results)} docs re-ranked with {model_type} (avg score: {avg_score:.3f})")
        except Exception as e:
            print(f"⚠️  Re-ranking failed: {str(e)}")
            # Fallback: sort by original score
            all_results = sorted(all_results, key=lambda x: x["original_score"], reverse=True)[:top_k]
    
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