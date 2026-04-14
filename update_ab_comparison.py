with open('frontendstreamlit/ab_comparison.py', 'w', encoding='utf-8') as f:
    f.write("""# Analyse comparative - standard embeddings
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR))

def analyze_with_standard_embeddings(text, rapport_type="Analyse Objections", top_k=3):
    \"\"\"Analyse avec embeddings STANDARD (pas fine-tuning)\"\"\"
    from rag.query.query_bo5_medical import analyze_conversation
    print("[STANDARD] Running with STANDARD embeddings (no finetuning)...")
    return analyze_conversation(text, rapport_type, top_k=top_k, use_finetuned=False)
""")

print("OK")
