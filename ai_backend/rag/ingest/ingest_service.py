# ingest_service.py — VERSION FIXÉE
import chromadb
import hashlib
import os
from chromadb.utils import embedding_functions

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
CHROMA_DIR = os.path.join(BASE_DIR, "ai_backend", "rag", "chroma_db")

EMBED_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"
emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBED_MODEL)

client = chromadb.PersistentClient(path=CHROMA_DIR)


def get_collection():
    return client.get_or_create_collection(
        name="global_docs",
        embedding_function=emb_fn,
        metadata={"hnsw:space": "cosine"},
    )


def make_doc_id(text: str) -> str:
    return "upload_" + hashlib.md5(text.strip().encode()).hexdigest()


def ingest_uploaded_data(data):
    col = get_collection()

    if isinstance(data, dict):
        data = [data]

    docs, ids, metas = [], [], []
    seen_ids = set()  # 🔥 déduplication LOCALE d'abord

    for item in data:
        text = f"""Produit: {item.get("name", "")}
Catégorie: {item.get("categories", "")}
Indications: {item.get("indications", "")}
Description: {item.get("description", "")}
Bénéfices: {item.get("highlights", "")}
"""
        doc_id = make_doc_id(text)

        # 🔥 skip si doublon dans le fichier JSON lui-même
        if doc_id in seen_ids:
            continue
        seen_ids.add(doc_id)

        docs.append(text)
        ids.append(doc_id)
        metas.append({
            "source": "streamlit_upload",
            "produit": str(item.get("name", "")),
            "type": "product"
        })

    if not ids:
        return 0, col.count()

    # 🔥 Vérifier les doublons côté ChromaDB sur des IDs uniques
    existing_ids = set(col.get(ids=ids)["ids"])

    new_docs, new_ids, new_metas = [], [], []
    for doc, doc_id, meta in zip(docs, ids, metas):
        if doc_id not in existing_ids:
            new_docs.append(doc)
            new_ids.append(doc_id)
            new_metas.append(meta)

    if new_docs:
        col.add(documents=new_docs, ids=new_ids, metadatas=new_metas)

    return len(new_docs), col.count()