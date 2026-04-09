#!/usr/bin/env python3
"""
Indexe vital_bo6_dataset.csv dans Chroma DB
Améliore les scores de retrieval pour BO5
"""

import sys
import csv
from pathlib import Path

BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / "ai_backend"))

import chromadb
from chromadb.utils import embedding_functions

# ========================================
# CONFIGURATION
# ========================================
CHROMA_PATH = "ai_backend/rag/chroma_db"
DATA_DIR = Path("ai_backend/data")
EMBED_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"

emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=EMBED_MODEL
)

client = chromadb.PersistentClient(path=CHROMA_PATH)

# ========================================
# INDEXER vital_bo6_dataset.csv
# ========================================
def ingest_bo6_dataset():
    """Charge et indexe le dataset BO6/BO5"""
    
    csv_file = DATA_DIR / "vital_bo6_dataset.csv"
    
    if not csv_file.exists():
        print(f"❌ Fichier non trouvé: {csv_file}")
        return
    
    print(f"📂 Chargement: {csv_file}")
    
    # Get or create collection
    collection = client.get_or_create_collection(
        name="bo5_data",
        embedding_function=emb_fn,
        metadata={"hnsw:space": "cosine"}
    )
    
    docs = []
    ids = []
    metadatas = []
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            
            print(f"📄 Total lignes: {len(rows)}")
            
            for i, row in enumerate(rows):
                # Construire le texte du document
                text_parts = []
                
                for key, value in row.items():
                    if value and value.strip():
                        text_parts.append(f"{key}: {value}")
                
                text = "\n".join(text_parts)
                
                if not text.strip():
                    continue
                
                # Créer ID unique
                doc_id = f"bo5_{i}"
                
                # Métadonnées (seulement str, int, float, bool)
                metadata = {
                    "source": "vital_bo6_dataset",
                    "type": "bo5_data",
                    "row_index": i
                }
                
                # Ajouter cols utiles aux métadatas
                for key in ['title', 'name', 'product', 'produit', 'category', 'catégorie']:
                    if key in row and row[key]:
                        metadata[key] = str(row[key])[:100]  # Limiter à 100 chars
                
                docs.append(text)
                ids.append(doc_id)
                metadatas.append(metadata)
            
            print(f"✅ Documents à indexer: {len(docs)}")
            
            if docs:
                collection.add(
                    documents=docs,
                    ids=ids,
                    metadatas=metadatas
                )
                print(f"✅ {len(docs)} documents indexés dans 'bo5_data'")
                
                # Vérifier
                count = collection.count()
                print(f"📊 Total dans 'bo5_data': {count}")
            
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        import traceback
        traceback.print_exc()

# ========================================
# TEST DE RETRIEVAL
# ========================================
def test_retrieval():
    """Test la retrieval après indexation"""
    
    print("\n" + "="*80)
    print("🔍 TEST DE RETRIEVAL - BO5 DATA")
    print("="*80)
    
    try:
        collection = client.get_collection("bo5_data")
        
        test_queries = [
            "prix coût euros remboursement",
            "efficacité données cliniques",
            "objections sécurité",
            "rapport stratégie vente",
        ]
        
        for query in test_queries:
            print(f"\n📝 Requête: '{query}'")
            results = collection.query(
                query_texts=[query],
                n_results=2,
                include=['documents', 'distances']
            )
            
            if results['ids'][0]:
                for i, (doc_id, dist) in enumerate(zip(results['ids'][0], results['distances'][0]), 1):
                    score = 1 - dist
                    doc_preview = results['documents'][0][i-1][:80].replace('\n', ' ')
                    print(f"   {i}. Score: {score:.3f} | {doc_preview}...")
            else:
                print("   ⚠️  Aucun résultat")
    
    except Exception as e:
        print(f"❌ Erreur retrieval: {str(e)}")

# ========================================
# MAIN
# ========================================
if __name__ == "__main__":
    print("="*80)
    print("🚀 INDEXATION vital_bo6_dataset.csv")
    print("="*80 + "\n")
    
    ingest_bo6_dataset()
    test_retrieval()
    
    print("\n" + "="*80)
    print("✅ Indexation complete!")
    print("="*80)
