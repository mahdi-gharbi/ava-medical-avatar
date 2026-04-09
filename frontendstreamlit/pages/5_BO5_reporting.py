# ========================================
# BO5 REPORTING avec RAG + GROQ
# ========================================
import streamlit as st
import pandas as pd
import sys
import os
from datetime import datetime

# ========================================
# FIX PATHS
# ========================================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
BACKEND_DIR = os.path.join(BASE_DIR, "ai_backend")

# Ajouter la racine au début du path
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, BACKEND_DIR)

# ========================================
# PAGE CONFIG
# ========================================
st.set_page_config(
    page_title="BO5 - Reporting",
    layout="wide",
    page_icon="📄"
)

st.title("📄 BO5 - Reporting avec IA")
st.write("Génération de rapports intelligents utilisant Groq LLM + Chroma")

# ========================================
# SIDEBAR FILTERS
# ========================================
st.sidebar.header("📋 Paramètres Rapport")

rapport_type = st.sidebar.selectbox(
    "Type de rapport",
    ["Analyse Objections", "Synthèse Produits", "Recommandations", "Statistiques"]
)

st.sidebar.markdown("---")

# Exemple de conversations
exemples = {
    "📍 Cardiologie (défaut)": """DÉLÉGUÉ: Bonjour docteur, merci de m'accorder ce moment
MÉDECIN: Bien sûr, que me proposez-vous?
DÉLÉGUÉ: Nous avons lancé un nouveau produit pour la cardiologie
MÉDECIN: Intéressant! Quel est le prix?
DÉLÉGUÉ: 45 euros par boîte, pour un traitement mensuel
MÉDECIN: C'est assez cher, n'avez-vous pas quelque chose de moins onéreux?
DÉLÉGUÉ: Je comprends votre préoccupation. Cependant, les études cliniques montrent 35% d'efficacité supérieure
MÉDECIN: Vous avez les données cliniques?
DÉLÉGUÉ: Absolument, voici les résultats des essais phase 3
MÉDECIN: Et la sécurité? Y a-t-il des effets secondaires?
DÉLÉGUÉ: Le profil de sécurité est excellent, tolérance supérieure aux produits concurrents
MÉDECIN: Bon, et la disponibilité? Avez-vous du stock?
DÉLÉGUÉ: Oui, nous avons en stock chez notre grossiste
MÉDECIN: Et la couverture CNAM?
DÉLÉGUÉ: C'est en cours d'évaluation, mais je vous fournirai la documentation""",
    
    "🩺 Dermatologie": """DÉLÉGUÉ: Bonjour Dr Martin, comment allez-vous?
MÉDECIN: Bien, je suis occupé. Dites-moi rapidement.
DÉLÉGUÉ: Nous avons une nouvelle crème pour le traitement de l'acné
MÉDECIN: Une crème de plus... Qu'est-ce qui la rend spéciale?
DÉLÉGUÉ: Notre formule combine acide salicylique et probiotiques naturels
MÉDECIN: Les probiotiques dans une crème? C'est quoi, la preuve scientifique?
DÉLÉGUÉ: Nous avons des résultats d'essais sur 500 patients montrant 78% d'amélioration
MÉDECIN: Et les effets secondaires? L'irritation cutanée?
DÉLÉGUÉ: Non, elle est hypoallergénique et testée dermatologiquement
MÉDECIN: Quel est le prix comparé à Duac?
DÉLÉGUÉ: 28 euros par tube, moins cher de 30% mais plus efficace
MÉDECIN: Et l'assurance? Elle rembourse?
DÉLÉGUÉ: Oui, sur prescription médicale""",
    
    "💊 Antibiothérapie": """DÉLÉGUÉ: Docteur, pouvez-vous m'accorder 5 minutes?
MÉDECIN: D'accord, mais soyez rapide.
DÉLÉGUÉ: Nous commercialisons un nouvel antibiotique large spectre
MÉDECIN: Encore un! Nous en avons déjà assez. L'antibioresistance?
DÉLÉGUÉ: C'est justement pour cela. Notre molécule a montré efficacité contre les souches multirésistantes
MÉDECIN: Des souches vraiment multirésistantes? BLSE? Pseudomonas?
DÉLÉGUÉ: Oui, spécifiquement. Essai pédiatrique en cours d'évaluation
MÉDECIN: Pédiatrique? Les effets secondaires chez l'enfant?
DÉLÉGUÉ: Sécurité démontrée dans tous les groupes d'âge. Dosage pédiatrique disponible
MÉDECIN: Qu'en est-il de la pharmacocinétique? Interactions médicamenteuses?
DÉLÉGUÉ: Excellente pénétration tissulaire. Très peu d'interactions. Documentation complète disponible
MÉDECIN: OK, envoyez-moi les données d'essai""",
    
    "📈 Cas Simple": """DÉLÉGUÉ: Bonjour, voici le produit X
MÉDECIN: Pourquoi je devrais l'utiliser?
DÉLÉGUÉ: Meilleur que les concurrents
MÉDECIN: Comment? Données?
DÉLÉGUÉ: Nous avons des études
MÉDECIN: Quelles études?
DÉLÉGUÉ: Je vais vous les envoyer""",
    
    "🫧 Gastroentérologie": """DÉLÉGUÉ: Docteur, j'aimerais vous présenter notre nouveau complément probiotique
MÉDECIN: Je prescris déjà plusieurs marques. Quel est l'intérêt?
DÉLÉGUÉ: Notre formule contient 9 souches brevetées avec une viabilité de 95% jusqu'à l'intestin
MÉDECIN: Viabilité? Comment vous le prouvez?
DÉLÉGUÉ: Études indépendantes réalisées à l'Université de Lyon, publiées en 2025
MÉDECIN: Et les contre-indications? Je traite beaucoup d'immunodéprimés
DÉLÉGUÉ: Aucune contre-indication majeure. Déjà utilisé en milieu hospitalier
MÉDECIN: Quel est le coût par cure?
DÉLÉGUÉ: 32 euros pour 30 jours, moins cher que nos concurrents directs
MÉDECIN: C'est remboursé?
DÉLÉGUÉ: Actuellement en attente d'inscription ANSM, devrais être approuvé en Q3 2026""",
    
    "💉 Immunologie": """DÉLÉGUÉ: Dr Dubois, une visite rapide pour vous parler d'un nouveau produit de renforcement immunitaire
MÉDECIN: Renforcement immunitaire? C'est vague. Soyez précis.
DÉLÉGUÉ: Notre formule combine vitamine D3, zinc et extrait de sureau noir
MÉDECIN: Des preuves d'efficacité contre la grippe?
DÉLÉGUÉ: Oui, essai clinique randomisé montrant 40% de réduction des infections respiratoires
MÉDECIN: Sur combien de patients?
DÉLÉGUÉ: 1200 patients sur 12 mois, publié dans le Journal of Immunology 2025
MÉDECIN: Et les effets indésirables? Allergie possible?
DÉLÉGUÉ: Très bien toléré. Moins de 2% d'effets secondaires mineurs
MÉDECIN: Quelle est la posologie?
DÉLÉGUÉ: 1 gélule par jour pendant les mois d'hiver
MÉDECIN: Stock disponible?
DÉLÉGUÉ: Oui, livraison sous 48h. En stock chez nos partenaires""",
    
    "🦴 Rhumatologie": """DÉLÉGUÉ: Docteur, je viens vous parler d'une solution pour l'arthrose et les douleurs articulaires
MÉDECIN: J'en prescris déjà 3-4 marques différentes. Pourquoi celle-ci?
DÉLÉGUÉ: Notre formule combine curcuma 95% curcuminoïdes, bambou silicium et boswellia serrata
MÉDECIN: Curcuma encore? Le curcuma seul n'est pas très biodisponible
DÉLÉGUÉ: C'est pourquoi nous l'avons combiné avec de la pipérine pour augmenter l'absorption de 2000%
MÉDECIN: 2000%? C'est énorme. Des études?
DÉLÉGUÉ: Oui, essai comparatif contre glucosamine classique, notre formule 2x plus efficace
MÉDECIN: Et pour les patients sous anticoagulants? Je dois être prudent.
DÉLÉGUÉ: Aucune interaction connue avec warfarine ou autres anticoagulants
MÉDECIN: Prix compétitif?
DÉLÉGUÉ: 24 euros par boîte 60 gélules, parmi les moins chers du marché
MÉDECIN: Remboursement?
DÉLÉGUÉ: Complément alimentaire, non remboursé mais très abordable""",
    
    "😴 Sommeil & Stress": """DÉLÉGUÉ: Dr Sophie, vous êtes toujours débordée? J'ai quelque chose qui pourrait aider vos patients
MÉDECIN: Des problèmes de sommeil? Oui, 30% de mes patients se plaignent
DÉLÉGUÉ: Nous avons une formule avec mélatonine 1.9mg, L-théanine et passiflore
MÉDECIN: Mélatonine... elle crée une dépendance?
DÉLÉGUÉ: Aucune dépendance cliniquement prouvée. La mélatonine est naturelle, produite par le corps
MÉDECIN: Et les effets indésirables?
DÉLÉGUÉ: Très bien toléré, estudos montrent 5% d'effets secondaires légers (maux de tête occasionnels)
MÉDECIN: Pour quelle durée de traitement?
DÉLÉGUÉ: Recommandée 2-3 mois pour réinitialiser les cycles, sans dépendance après arrêt
MÉDECIN: Et le prix?
DÉLÉGUÉ: 19.90 euros pour 30 jours, vraiment accessible pour vos patients
MÉDECIN: Prescription obligatoire ou en libre accès?
DÉLÉGUÉ: Libre accès en pharmacie, ou sur prescription pour meilleure prise en charge""",
    
    "⚡ Fatigue & Vitalité": """DÉLÉGUÉ: Bonjour Dr Martin, vous voyez beaucoup de patients fatigués?
MÉDECIN: Oui, surtout après 50 ans. Burnout, fatigue chronique...
DÉLÉGUÉ: Nos patients rapportent une amélioration significative avec notre formule CoQ10 + ginseng
MÉDECIN: CoQ10 300mg? C'est élevé. Efficacité prouvée?
DÉLÉGUÉ: Oui, étude cardiologique montrant amélioration de 35% des niveaux d'énergie
MÉDECIN: Des risques? Je prescris des statines à beaucoup de patients
MÉDECIN: C'est bon, CoQ10 complète les statines qui les épuisent
MÉDECIN: Combinaison ginseng + CoQ10, pas d'interaction?
DÉLÉGUÉ: Aucune interaction connue. Les deux agissent de manière synergique
MÉDECIN: Combien de temps avant résultats?
DÉLÉGUÉ: 3-4 semaines généralement pour une amélioration notable
MÉDECIN: Stock? Prix?
DÉLÉGUÉ: En stock. 35 euros par boîte 30 gélules, très compétitif"""
}

st.sidebar.subheader("🎯 Exemples de Conversations")
choix = st.sidebar.selectbox("Sélectionnez un exemple:", list(exemples.keys()))

top_k = st.sidebar.slider("Nombre de sources", 1, 10, 5)

# ========================================
# MAIN CONTENT
# ========================================

st.markdown("---")
st.subheader("📞 Entrez la Discussion Délégué-Médecin")

query_input = st.text_area(
    "Dialogue complet:",
    value=exemples[choix],
    height=250,
    key="dialogue_textarea"
)

col1, col2 = st.columns([3, 1])

with col1:
    st.write("**Format attendu:** Alternez DÉLÉGUÉ: et MÉDECIN:")

with col2:
    generate_btn = st.button("🚀 Générer Rapport avec IA", use_container_width=True)

if generate_btn:
    if not query_input.strip():
        st.error("❌ Veuillez entrer la conversation")
    else:
        with st.spinner("⏳ Analyse de la discussion..."):
            try:
                # Importer les services RAG
                from rag.query.query_bo5_medical import analyze_conversation
                
                # Analyser la conversation complète
                result = analyze_conversation(
                    dialogue=query_input,
                    rapport_type=rapport_type,
                    top_k=top_k
                )
                
                # Display Response
                st.success("✅ Rapport généré!")
                
                # Afficher analyse
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown("### 📝 Analyse IA")
                    st.write(result["analysis"])
                
                with col2:
                    st.markdown("### 🎯 Points Clés")
                    for key, value in result.get("key_points", {}).items():
                        st.write(f"**{key}:** {value}")
                
                # Objections détectées
                if result.get("objections"):
                    st.markdown("### 🚫 Objections Détectées")
                    for i, obj in enumerate(result["objections"], 1):
                        with st.expander(f"Objection {i}: {obj['type']}"):
                            st.write(f"**Énoncé:** {obj['text']}")
                            st.write(f"**Stratégie:** {obj['strategy']}")
                
                # Sources
                st.markdown("### 📚 Sources Utilisées")
                for i, source in enumerate(result["sources"], 1):
                    with st.expander(f"Source {i} (Score: {source['score']:.3f})"):
                        st.write(source["content"][:500] + "...")
                
                # Export
                st.markdown("---")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("📥 Télécharger en PDF"):
                        st.info("PDF export coming soon...")
                
                with col2:
                    if st.button("📊 Exporter en JSON"):
                        st.download_button(
                            label="Télécharger JSON",
                            data=str(result),
                            file_name=f"rapport_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                        )
                
                with col3:
                    if st.button("💾 Sauvegarder"):
                        try:
                            from rag.query.query_bo5_medical import save_rapport
                            filepath = save_rapport(result)
                            st.success(f"✅ Rapport sauvegardé !\n📁 {filepath}")
                        except Exception as e:
                            st.error(f"❌ Erreur sauvegarde: {str(e)}")
                            import traceback
                            st.code(traceback.format_exc())
                
                # Afficher rapports existants
                st.markdown("---")
                st.subheader("📂 Rapports Sauvegardés")
                
                try:
                    from rag.query.query_bo5_medical import list_saved_rapports
                    saved = list_saved_rapports()
                    
                    if saved:
                        for i, rapport in enumerate(saved[:5], 1):
                            st.write(f"{i}. 📄 {rapport['filename']}")
                    else:
                        st.info("Aucun rapport sauvegardé pour le moment")
                except ImportError as e:
                    st.warning(f"⚠️ Rechargez la page si les listes ne s'affichent pas: {str(e)}")
            
            except Exception as e:
                st.error(f"❌ Erreur: {str(e)}")
                import traceback
                st.code(traceback.format_exc())
else:
    st.info("""
    💡 **Comment utiliser:**
    1. Collez la conversation entre le délégué et le médecin
    2. Sélectionnez le type de rapport
    3. Cliquez sur "Générer Rapport"
    4. L'IA analysera les objections et générera des stratégies
    
    **Exemple de format acceptable:**
    ```
    DÉLÉGUÉ: Bonjour docteur...
    MÉDECIN: Réponse...
    DÉLÉGUÉ: Sujet suivant...
    MÉDECIN: Réaction...
    ```
    """)