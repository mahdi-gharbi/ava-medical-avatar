#!/usr/bin/env python3
"""
Diagnostic: Vérifier ce qui est indexé dans Chroma DB
Objectif: Comprendre pourquoi les scores sont faibles
"""

import sys
import os
from pathlib import Path

# Fix paths
BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / "ai_backend"))

import chromadb
from chromadb.utils import embedding_functions

# ========================================
# CHARGER CHROMA DB
# ========================================
CHROMA_PATH = "ai_backend/rag/chroma_db"
EMBED_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"

emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=EMBED_MODEL
)

client = chromadb.PersistentClient(path=CHROMA_PATH)

print("=" * 80)
print("📊 DIAGNOSTIC CHROMA DB")
print("=" * 80)

# 1. Liste des collections
collections = client.list_collections()
print(f"\n📚 Collections disponibles: {len(collections)}")
for col in collections:
    print(f"   - {col.name}")

# 2. Détails par collection
for col_obj in collections:
    print(f"\n{'='*80}")
    print(f"📦 Collection: {col_obj.name}")
    print(f"{'='*80}")
    
    try:
        col = client.get_collection(col_obj.name)
        count = col.count()
        print(f"   ✅ Total documents: {count}")
        
        # Sample quelques documents
        if count > 0:
            sample = col.get(limit=3, include=['documents', 'metadatas'])
            print(f"\n   📄 échantillons (3 premiers):")
            for i, (doc_id, metadata) in enumerate(zip(sample['ids'], sample['metadatas']), 1):
                print(f"\n      Sample {i}:")
                print(f"      - ID: {doc_id}")
                print(f"      - Type: {metadata.get('type', 'N/A')}")
                print(f"      - Source: {metadata.get('source', 'N/A')}")
                if 'name' in metadata:
                    print(f"      - Nom: {metadata['name'][:50]}...")
    except Exception as e:
        print(f"   ❌ Erreur: {str(e)}")

# 3. Test de retrieval
print(f"\n{'='*80}")
print("🔍 TEST DE RETRIEVAL")
print(f"{'='*80}")

test_queries = [
    "cardiologie produit nouveau efficacité",
    "prix coût euros",
    "sécurité effets secondaires",
]

try:
    products_col = client.get_collection("products")
    
    for query in test_queries:
        print(f"\n📝 Requête: '{query}'")
        results = products_col.query(
            query_texts=[query],
            n_results=3,
            include=['documents', 'metadatas', 'distances']
        )
        
        if results['ids'][0]:
            for i, (doc_id, dist, meta) in enumerate(zip(
                results['ids'][0],
                results['distances'][0],
                results['metadatas'][0]
            ), 1):
                score = 1 - dist  # cosine similarity
                print(f"   {i}. Score: {score:.3f} | {meta.get('name', 'N/A')[:40]}")
        else:
            print("   ⚠️  Aucun résultat")
            
except Exception as e:
    print(f"   ❌ Erreur retrieval: {str(e)}")

# 4. Statistiques
print(f"\n{'='*80}")
print("📈 STATISTIQUES")
print(f"{'='*80}")

try:
    total_docs = sum(client.get_collection(c.name).count() for c in collections)
    print(f"   Total documents CHROMA: {total_docs}")
    
    # Check data files
    data_dir = Path("ai_backend/data")
    print(f"\n   📁 Fichiers disponibles dans {data_dir}:")
    for file in sorted(data_dir.glob("*")):
        size_mb = file.stat().st_size / (1024*1024)
        print(f"      - {file.name} ({size_mb:.2f} MB)")
        
except Exception as e:
    print(f"   ❌ Erreur stats: {str(e)}")

print("\n" + "=" * 80)
print("✅ Diagnostic terminé!")
print("=" * 80)
