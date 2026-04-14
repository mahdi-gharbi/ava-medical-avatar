import streamlit as st

# Pre-load and cache embedding models to prevent reloading on every rerun
try:
    from cached_models import load_finetuned_model, load_standard_model
    _ = load_finetuned_model()
    _ = load_standard_model()
except Exception as e:
    print(f"[WARN] Could not pre-load models: {e}")

# Configuration page
st.set_page_config(
    page_title="AVA System",
    page_icon="🤖",
    layout="wide"
)

# Page principale
st.title("🤖 AVA System")
st.write("Welcome to the AVA platform")

st.markdown("""
### 📌 Description
This is a simple interface for the AVA project.

### 📂 Navigation
Use the sidebar to access different modules:

- 🎯 BO1 → Training  
- 💬 BO2 → Commercial  
- 📊 BO3 → Recommendation  
- 📝 BO4 → Content Generation  
- 📄 BO5 → Reporting  

""")

# Sidebar info (optionnel)
st.sidebar.title("AVA Navigation")
st.sidebar.info("Select a page above")

# Footer
st.markdown("---")
st.write("AVA Project - Streamlit Version")