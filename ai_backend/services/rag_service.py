# ========================================
# RAG SERVICE avec GROQ + CHROMA
# ========================================
import os
from groq import Groq
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
CHROMA_PATH = os.getenv("CHROMA_PATH", "ai_backend/rag/chroma_db")

# ========================================
# Initialiser Groq Client
# ========================================
groq_client = Groq(api_key=GROQ_API_KEY)

# ========================================
# Initialiser Chroma
# ========================================
EMBED_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"
emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=EMBED_MODEL
)
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = chroma_client.get_or_create_collection(
    name="global_docs",
    embedding_function=emb_fn,
    metadata={"hnsw:space": "cosine"}
)

# ========================================
# RETRIEVER : Chercher dans Chroma (AMÉLIORÉ)
# ========================================
def retrieve_context(query: str, top_k: int = 5) -> list[dict]:
    """
    Cherche les documents pertinents dans Chroma (multi-collection)
    Stratégie: Requête enrichie + recherche dans products + bo5_data
    
    Args:
        query: Question utilisateur
        top_k: Nombre de résultats
    
    Returns:
        Liste de documents avec scores
    """
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
    
    # Ajouter bo5_data si elle existe
    try:
        bo5_col = chroma_client.get_collection("bo5_data")
        collection_names.append("bo5_data")
    except:
        pass
    
    # Chercher dans chaque collection
    for col_name in collection_names:
        try:
            col = chroma_client.get_collection(col_name)
            
            # Chercher avec plusieurs variantes
            for enriched_query in enriched_queries:
                results = col.query(
                    query_texts=[enriched_query],
                    n_results=top_k * 2,  # Get more to sort
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
                    
                    score = 1 - float(results["distances"][0][i])
                    
                    # Filter low scores
                    if score >= 0.25:
                        all_results.append({
                            "id": doc_id,
                            "content": doc,
                            "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                            "score": score,
                            "source": col_name
                        })
        except Exception as e:
            print(f"⚠️  Collection '{col_name}' not available: {str(e)}")
            continue
    
    # Trier par score et garder top_k
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