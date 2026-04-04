# reset_chroma.py  →  place-le à la racine du projet et lance-le UNE FOIS
import chromadb
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
CHROMA_PATH = os.path.join(BASE_DIR, "ai_backend", "rag", "chroma_db")

client = chromadb.PersistentClient(path=CHROMA_PATH)

for col in client.list_collections():
    client.delete_collection(col.name)
    print(f"🗑️  Supprimé : {col.name}")

print("✅ ChromaDB reset terminé")