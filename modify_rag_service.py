import re

with open('ai_backend/services/rag_service.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Modifier retrieve_context signature
old_sig = "def retrieve_context(query: str, top_k: int = 5) -> list[dict]:"
new_sig = "def retrieve_context(query: str, top_k: int = 5, use_finetuned: bool = True) -> list[dict]:"
content = content.replace(old_sig, new_sig)

# 2. Ajouter logique pour sélectionner la collection (après la docstring)
pos = content.find("def retrieve_context(query: str, top_k: int = 5, use_finetuned: bool = True)")
pos = content.find('"""', pos)
pos = content.find('"""', pos + 1) + 3

# Ajouter la logique de sélection
logic = """
    
    # Selectionner la collection avec le bon modele d'embeddings
    if use_finetuned:
        col_to_use = collection
        print(f"[FINETUNED] Using finetuned embeddings")
    else:
        col_to_use = get_standard_embedding_collection()
        print(f"[STANDARD] Using standard embeddings")"""

content = content[:pos] + logic + content[pos:]

with open('ai_backend/services/rag_service.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("OK - rag_service modified")
