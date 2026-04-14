import chromadb

CHROMA_PATH = "ai_backend/rag/chroma_db"
client = chromadb.PersistentClient(path=CHROMA_PATH)
collections = client.list_collections()

print(f"Total collections: {len(collections)}")
for c in collections:
    print(f"- {c.name}: {c.count()} docs")
