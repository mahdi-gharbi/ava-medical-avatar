#!/usr/bin/env python3
"""
Sync documents from ingest-created collections to fine-tuned and standard collections.
This ensures A/B testing works with different embedding models.
"""
import os
import sys
from pathlib import Path

# Add parent to path
BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))

import chromadb
from chromadb.utils import embedding_functions

CHROMA_PATH = BASE_DIR / "ai_backend/rag/chroma_db"
EMBED_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"
AI_BACKEND_DIR = BASE_DIR / "ai_backend"
FINETUNED_MODEL_PATH = AI_BACKEND_DIR / "models" / "finetuned_sentence_transformer"

def get_embedding_function():
    """Get fine-tuned embedding function"""
    if (FINETUNED_MODEL_PATH / "model.safetensors").exists() or (FINETUNED_MODEL_PATH / "pytorch_model.bin").exists():
        print(f"✅ Using fine-tuned embeddings from: {FINETUNED_MODEL_PATH}")
        return embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=str(FINETUNED_MODEL_PATH)
        )
    else:
        print(f"⚠️ Fine-tuned model not found, using standard: {EMBED_MODEL}")
        return embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=EMBED_MODEL
        )

def get_standard_embedding_function():
    """Get standard embedding function"""
    return embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBED_MODEL
    )

client = chromadb.PersistentClient(path=str(CHROMA_PATH))

# Create collections with proper embedding functions
try:
    finetuned_fn = get_embedding_function()
    standard_fn = get_standard_embedding_function()
    
    # Delete old collections if they exist (to avoid conflicts)
    for col_name in ["products_finetuned", "products_standard"]:
        try:
            client.delete_collection(name=col_name)
            print(f"🗑️  Deleted old collection: {col_name}")
        except:
            pass
    
    # Create new collections with proper embedding functions
    products_ft = client.get_or_create_collection(
        name="products_finetuned",
        embedding_function=finetuned_fn,
        metadata={"hnsw:space": "cosine"}
    )
    
    products_std = client.get_or_create_collection(
        name="products_standard",
        embedding_function=standard_fn,
        metadata={"hnsw:space": "cosine"}
    )
    
    print(f"\n✅ Created collections:")
    print(f"   - products_finetuned (with fine-tuned embeddings)")
    print(f"   - products_standard (with standard embeddings)")
    
    # Try to get original products collection
    try:
        products_orig = client.get_collection("products")
        print(f"\n📦 Found original 'products' collection")
        
        # Get all documents from products
        all_docs = products_orig.get()
        
        if all_docs and all_docs.get("ids"):
            print(f"   Found {len(all_docs['ids'])} documents")
            
            # Add same documents to both fine-tuned and standard collections
            print(f"\n⏳ Syncing documents...")
            
            products_ft.add(
                ids=all_docs["ids"],
                documents=all_docs["documents"],
                metadatas=all_docs["metadatas"]
            )
            print(f"✅ Added {len(all_docs['ids'])} docs to products_finetuned")
            
            products_std.add(
                ids=all_docs["ids"],
                documents=all_docs["documents"],
                metadatas=all_docs["metadatas"]
            )
            print(f"✅ Added {len(all_docs['ids'])} docs to products_standard")
        else:
            print("⚠️  No documents found in products collection")
    except Exception as e:
        print(f"⚠️  Could not find or sync 'products' collection: {e}")
    
    print("\n✅ Sync complete!")
    print("\n📝 Update rag_service.py retrieve_context to use:")
    print("   - products_finetuned when use_finetuned=True")
    print("   - products_standard when use_finetuned=False")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
