"""
Streamlit-specific caching for embedding models.
This prevents models from being reloaded on every Streamlit rerun.
"""
import streamlit as st
from sentence_transformers import SentenceTransformer

EMBED_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"

@st.cache_resource
def load_standard_model():
    """Load standard model with Streamlit caching"""
    return SentenceTransformer(EMBED_MODEL)

# Pre-load standard model on import
_ = load_standard_model()
