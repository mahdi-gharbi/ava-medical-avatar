with open('ai_backend/services/rag_service.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the section where we search in collections
# After the line "# Ajouter bo5_data si elle existe"
# We need to add searching in col_to_use (fine-tuned or standard collection)

# Find where collection_names are used
old_section = """    # Chercher dans chaque collection
    for col_name in collection_names:"""

new_section = """    # Chercher dans la collection principale (fine-tuning ou standard)
    main_col_name = "global_docs"
    try:
        for enriched_query in enriched_queries:
            results = col_to_use.query(
                query_texts=[enriched_query],
                n_results=top_k * 2,
                include=["documents", "metadatas", "distances"]
            )
            
            if not results or not results.get("ids") or not results["ids"][0]:
                continue
            
            for i, doc in enumerate(results["documents"][0]):
                doc_id = f"{main_col_name}_{results['ids'][0][i]}"
                
                if doc_id in seen_ids:
                    continue
                seen_ids.add(doc_id)
                
                score = 1 - float(results["distances"][0][i])
                
                if score >= 0.25:
                    all_results.append({
                        "id": doc_id,
                        "content": doc,
                        "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                        "score": score,
                        "source": main_col_name
                    })
    except Exception as e:
        print(f"[DEBUG] Main collection search: {e}")
    
    # Chercher dans chaque collection
    for col_name in collection_names:"""

if old_section in content:
    content = content.replace(old_section, new_section)
    with open('ai_backend/services/rag_service.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK - Added main collection search")
else:
    print("ERROR - Section not found")
