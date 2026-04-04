import streamlit as st

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