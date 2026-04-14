import re

# Modify query_bo5_medical.py to pass use_finetuned parameter
with open('ai_backend/rag/query/query_bo5_medical.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all calls to retrieve_context and add use_finetuned parameter
# Pattern: retrieve_context(something)
# Replace with: retrieve_context(something, use_finetuned=use_finetuned)

# Find analyze_conversation function and add use_finetuned parameter
old_analyze = 'def analyze_conversation(query: str, rapport_type: str = "Analyse Objections", top_k: int = 3'
new_analyze = 'def analyze_conversation(query: str, rapport_type: str = "Analyse Objections", top_k: int = 3, use_finetuned: bool = True'

content = content.replace(old_analyze, new_analyze)

# Now find retrieve_context calls and add use_finetuned
content = re.sub(
    r'retrieve_context\(([^)]+)\)',
    lambda m: f'retrieve_context({m.group(1)}, use_finetuned=use_finetuned)',
    content
)

# But we need to avoid double use_finetuned, so fix any that already have it
content = re.sub(
    r'retrieve_context\(([^)]+), use_finetuned=use_finetuned, use_finetuned=use_finetuned\)',
    lambda m: f'retrieve_context({m.group(1)}, use_finetuned=use_finetuned)',
    content
)

with open('ai_backend/rag/query/query_bo5_medical.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("OK - query_bo5_medical modified")
