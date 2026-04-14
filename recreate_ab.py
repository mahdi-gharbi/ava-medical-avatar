import os

# Remove old file
if os.path.exists('frontendstreamlit/ab_comparison.py'):
    os.remove('frontendstreamlit/ab_comparison.py')

# Create new simplified version
code = """# Analyse comparative standard
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR))

def analyze_with_standard_embeddings(text, rapport_type="Analyse Objections", top_k=3):
    from rag.query.query_bo5_medical import analyze_conversation
    print("🔄 Embeddings STANDARD...")
    return analyze_conversation(text, rapport_type, top_k=top_k)
"""

with open('frontendstreamlit/ab_comparison.py', 'w') as f:
    f.write(code)

print("✅ ab_comparison.py recréé correctement!")
