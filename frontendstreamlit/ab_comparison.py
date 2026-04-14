# Analyse comparative - standard embeddings
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR))

def analyze_with_standard_embeddings(text, rapport_type="Analyse Objections", top_k=3):
    """Call analyze_conversation - uses standard embeddings as fallback"""
    from rag.query.query_bo5_medical import analyze_conversation
    print("[STANDARD] Running analysis with standard embeddings...")
    return analyze_conversation(text, rapport_type, top_k=top_k, use_finetuned=False)
