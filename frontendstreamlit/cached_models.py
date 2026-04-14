"""
Streamlit-specific caching for embedding models.
This prevents models from being reloaded on every Streamlit rerun.
"""
import streamlit as st
from pathlib import Path
from sentence_transformers import SentenceTransformer

AI_BACKEND_DIR = Path(__file__).parent.parent / "ai_backend"
FINETUNED_MODEL_PATH = AI_BACKEND_DIR / "models" / "finetuned_sentence_transformer"
EMBED_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"

@st.cache_resource
def load_finetuned_model():
    """Load fine-tuned model with Streamlit caching"""
    if (FINETUNED_MODEL_PATH / "model.safetensors").exists() or (FINETUNED_MODEL_PATH / "pytorch_model.bin").exists():
        return SentenceTransformer(str(FINETUNED_MODEL_PATH))
    else:
        return SentenceTransformer(EMBED_MODEL)

@st.cache_resource
def load_standard_model():
    """Load standard model with Streamlit caching"""
    return SentenceTransformer(EMBED_MODEL)

# Pre-load models on import
_ = load_finetuned_model()
_ = load_standard_model()
