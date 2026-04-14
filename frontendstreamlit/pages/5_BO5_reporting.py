# ========================================
# BO5 REPORTING avec RAG + GROQ
# ========================================
import streamlit as st
import pandas as pd
import sys
import os
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from fpdf import FPDF
import re

# ========================================
# FIX PATHS
# ========================================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
BACKEND_DIR = os.path.join(BASE_DIR, "ai_backend")

# Ajouter la racine au début du path
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, BACKEND_DIR)

# ========================================
# FONCTION POUR GÉNÉRER PDF
# ========================================
def generate_pdf_report(result: dict, rapport_type: str) -> bytes:
    """Génère un PDF du rapport"""
    try:
        pdf = FPDF(format='A4', unit='mm')
        pdf.set_margins(15, 15, 15)
        pdf.add_page()
        
        # Titre
        pdf.set_font("Helvetica", "B", 12)
        pdf.write(8, "RAPPORT BO5 - ANALYSE DE VISITE\n\n")
        
        # Date
        pdf.set_font("Helvetica", "I", 9)
        pdf.write(5, f"Date: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
        pdf.ln(3)
        
        # Résumé
        pdf.set_font("Helvetica", "B", 10)
        pdf.write(6, "Resume de la Visite\n")
        pdf.set_font("Helvetica", "", 9)
        
        analysis_text = result.get("analysis", "Pas d'analyse")
        first_lines = "\n".join(analysis_text.split('\n')[:2])[:300]
        pdf.write(5, first_lines + "\n\n")
        
        # Score
        score_match = re.search(r'(\d+)\s*/\s*100', analysis_text)
        score = int(score_match.group(1)) if score_match else 50
        pdf.set_font("Helvetica", "B", 10)
        pdf.write(6, f"Score Performance: {score}/100\n")
        pdf.ln(3)
        
        # Objections
        if result.get("objections"):
            pdf.set_font("Helvetica", "B", 10)
            pdf.write(6, f"Objections ({len(result['objections'])})\n")
            pdf.set_font("Helvetica", "", 8)
            
            for i, obj in enumerate(result["objections"][:3], 1):
                text = f"{i}. {obj['type']}: {obj['text'][:60]}\n"
                pdf.write(4, text)
            pdf.ln(2)
        
        # Points clés
        if result.get("key_points"):
            pdf.set_font("Helvetica", "B", 10)
            pdf.write(6, "Points Cles\n")
            pdf.set_font("Helvetica", "", 8)
            
            for key, value in list(result.get("key_points", {}).items())[:3]:
                text = f"- {key}: {str(value)[:40]}\n"
                pdf.write(4, text)
        
        pdf.ln(5)
        pdf.set_font("Helvetica", "I", 7)
        pdf.write(4, "Rapport genere par systeme BO5 - Confidential")
        
        pdf_output = pdf.output(dest='S')
        return bytes(pdf_output)
    except Exception as e:
        print(f"[PDF ERROR] {str(e)}")
        raise

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
# TABS FOR DIFFERENT FUNCTIONALITIES
# ========================================
tab1, tab2 = st.tabs(["📝 Analyse Conversation", "🎯 Fine-tuning Tests"])

with tab1:
    # ========================================
    # SIDEBAR FILTERS (TAB 1)
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
                
                # ========================================
                # RÉSUMÉ COURT DE LA VISITE
                # ========================================
                st.markdown("---")
                st.markdown("### 📋 Résumé de la Visite")
                
                # Générer un résumé court de ce qui s'est passé
                try:
                    from services.rag_service import generate_response
                    
                    # Créer un prompt pour résumer la visite
                    resume_prompt = f"""Basé sur cette conversation entre un délégué médical et un médecin, fais un résumé TRÈS COURT (3-4 lignes maximum) de:
- Ce qui a été présenté/discuté
- Les objections principales du médecin
- Conclusion/accord

Sois concis et factuel.

Conversation:
{query_input}"""
                    
                    resume = generate_response(
                        query=resume_prompt,
                        context_docs=[],
                        system_prompt="Tu es un résumeur d'entretiens médicaux. Soit très concis."
                    )
                    
                    st.markdown(f"**{resume}**")
                    
                except Exception as e:
                    # Si la génération échoue, créer un résumé basé sur l'analyse
                    first_lines = "\n".join(result["analysis"].split('\n')[:3])
                    st.markdown(f"**{first_lines}**")
                
                # ========================================
                # DÉTAILS DÉPLIABLES
                # ========================================
                st.markdown("---")
                st.markdown("### 📖 Détails Complets")
                
                # Stats du rapport
                num_objections = len(result.get("objections", []))
                num_sources = len(result.get("sources", []))
                avg_score = sum(s["score"] for s in result.get("sources", [])) / num_sources if num_sources > 0 else 0
                
                # ========================================
                # ANALYSE SIGNIFICATIVE DE LA VISITE
                # ========================================
                with st.expander("🎯 Évaluation de la Visite", expanded=True):
                    # Générer des insights significatifs
                    visite_score = None
                    try:
                        from services.rag_service import generate_response
                        import re
                        
                        insights_prompt = f"""Analyse cette visite médicale et donne une évaluation STRUCTURÉE avec:
1. **Score Global** (X/100): Comment s'est déroulée la visite globalement?
2. **Points Forts** (2-3 bullets): Qu'est-ce qui a bien marché?
3. **Points Faibles** (2-3 bullets): Qu'est-ce qui aurait pu mieux se passer?
4. **Risques** (si applicable): Y a-t-il des risques identifiés?
5. **Recommandations** (2-3 bullets): Que faire pour la prochaine visite?

IMPORTANT: Format le score EXACTEMENT comme "Score Global: 45/100"

Conversation:
{query_input}"""
                        
                        insights = generate_response(
                            query=insights_prompt,
                            context_docs=[],
                            system_prompt="Tu es un expert en ventes médicales. Fournis une analyse constructive et actionnable. Utilise le format exact pour le score: 'Score Global: XX/100'"
                        )
                        
                        st.markdown(insights)
                        
                        # Extraire le score du rapport avec le pattern XX/100
                        score_match = re.search(r'(\d+)\s*/\s*100', insights)
                        if score_match:
                            visite_score = int(score_match.group(1))
                            print(f"[DEBUG] Score extrait: {visite_score}")
                        else:
                            print(f"[DEBUG] Pas de score trouvé dans: {insights[:200]}")
                        
                    except Exception as e:
                        st.warning(f"⚠️ Impossible de générer l'analyse détaillée: {str(e)}")
                    
                    # Visualisation du score de visite
                    st.markdown("---")
                    
                    # Créer un gauge chart pour le score de visite
                    if visite_score is None:
                        # Si on n'a pas pu extraire le score, utiliser la formule par défaut
                        if num_objections > 0:
                            visite_score = min(100, 50 + (num_objections * 8) + (avg_score * 30))
                        else:
                            visite_score = 70 + (avg_score * 30)
                        print(f"[DEBUG] Score par défaut calculé: {visite_score}")
                    
                    visite_score = min(100, max(0, visite_score))
                    
                    fig_gauge = go.Figure(go.Indicator(
                        mode="gauge+number+delta",
                        value=visite_score,
                        domain={'x': [0, 1], 'y': [0, 1]},
                        title={'text': "Performance de la Visite"},
                        delta={'reference': 50},
                        gauge={
                            'axis': {'range': [None, 100]},
                            'bar': {'color': "darkblue"},
                            'steps': [
                                {'range': [0, 33], 'color': "lightgray"},
                                {'range': [33, 66], 'color': "gray"},
                                {'range': [66, 100], 'color': "lightgreen"}
                            ],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75,
                                'value': 90
                            }
                        }
                    ))
                    st.plotly_chart(fig_gauge, use_container_width=True)
                
                # Analyse détaillée en expander
                with st.expander("📝 Analyse Complète IA", expanded=False):
                    st.write(result["analysis"])
                
                # Points clés en expander avec tableau
                with st.expander("🎯 Points Clés & Statistiques", expanded=False):
                    if result.get("key_points"):
                        key_points_data = pd.DataFrame([
                            {"Métrique": key, "Valeur": value}
                            for key, value in result.get("key_points", {}).items()
                        ])
                        st.dataframe(key_points_data, use_container_width=True)
                    else:
                        for key, value in result.get("key_points", {}).items():
                            st.write(f"**{key}:** {value}")
                
                # Objections détectées avec analyse
                if result.get("objections"):
                    with st.expander(f"🚫 Objections Détectées ({num_objections})", expanded=False):
                        # Tableau des objections avec stratégies mieux visibles
                        objections_data = pd.DataFrame([
                            {
                                "Objection": obj['type'],
                                "Énoncé": obj['text'][:50] + "..." if len(obj['text']) > 50 else obj['text'],
                            }
                            for obj in result["objections"]
                        ])
                        st.dataframe(objections_data, use_container_width=True)
                        
                        # Stratégies pour chaque objection
                        st.markdown("**✅ Stratégies de Réponse:**")
                        for i, obj in enumerate(result["objections"], 1):
                            col1, col2 = st.columns([1, 3])
                            with col1:
                                st.write(f"**{obj['type']}:**")
                            with col2:
                                st.write(obj['strategy'])
                
                # Sources avec contexte
                with st.expander(f"📚 Sources Utilisées ({num_sources})", expanded=False):
                    if num_sources > 0:
                        st.info(f"Score moyen de pertinence: **{avg_score:.2f}** (plus proche de 1 = plus pertinent)")
                        for i, source in enumerate(result["sources"], 1):
                            col1, col2 = st.columns([1, 4])
                            with col1:
                                st.metric("Score", f"{source['score']:.2f}")
                            with col2:
                                st.write(source["content"][:300] + "...")
                
                # Export
                st.markdown("---")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    try:
                        pdf_bytes = generate_pdf_report(result, rapport_type)
                        st.download_button(
                            label="📥 Télécharger en PDF",
                            data=pdf_bytes,
                            file_name=f"rapport_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                            mime="application/pdf"
                        )
                    except Exception as e:
                        st.error(f"❌ Erreur PDF: {str(e)}")
                
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


# ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
# TAB 2: 🎯 FINE-TUNING TESTS
# ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

with tab2:
    st.header("🎯 Fine-tuning ML Classifier")
    st.write("Testez et validez les performances du ML classifier avec les données VITAL")
    
    # ========================================
    # DATASET SELECTION
    # ========================================
    st.subheader("📊 Sélection du Dataset")
    
    dataset_choice = st.selectbox(
        "Choisissez le dataset pour les tests:",
        [
            "vital_bo6_dataset.csv (Transcripts visites médicales)",
            "parapharmacie_vital_final_v2.json (Produits parapharmacie)"
        ]
    )
    
    # ========================================
    # LOAD & TEST DATASET
    # ========================================
    if dataset_choice == "vital_bo6_dataset.csv (Transcripts visites médicales)":
        try:
            csv_path = os.path.join(BACKEND_DIR, "data", "vital_bo6_dataset.csv")
            df = pd.read_csv(csv_path)
            st.success(f"✅ Dataset chargé: {len(df)} visites médicales")
            
            # Preview
            st.subheader("👀 Aperçu du Dataset")
            st.dataframe(df.head(), use_container_width=True)
            
            # Stats
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Visites", len(df))
            with col2:
                st.metric("Objections Uniques", df['main_objection_type'].nunique() if 'main_objection_type' in df.columns else 0)
            with col3:
                avg_sentiment = df['sentiment_score'].mean() if 'sentiment_score' in df.columns else 0
                st.metric("Sentiment Moyen", f"{avg_sentiment:.2f}")
            
            # ========================================
            # TESTING OPTIONS
            # ========================================
            st.subheader("🧪 Tests Fine-tuning")
            
            test_mode = st.radio(
                "Mode de test:",
                [
                    "🎲 Visite Aléatoire",
                    "📋 Batch Test (N visites)",
                    "🧠 Évaluer Modèle Complet"
                ],
                horizontal=True
            )
            
            # SESSION STATE
            if "bo5_test_mode" not in st.session_state:
                st.session_state.bo5_test_mode = None
            if "bo5_test_result" not in st.session_state:
                st.session_state.bo5_test_result = None
            
            if test_mode == "🎲 Visite Aléatoire":
                if st.button("🎲 Tirer une Visite Aléatoire"):
                    st.session_state.bo5_test_mode = "random"
                    st.session_state.bo5_test_result = None
                
                if st.session_state.bo5_test_mode == "random":
                    selected = df.sample(1).iloc[0]
                    transcript = selected.get('transcript', selected.get('text', str(selected)))
                    
                    st.markdown("### 📝 Visite Sélectionnée")
                    st.text_area("Transcript:", transcript, height=200, disabled=True)
                    
                    if st.button("🔍 Analyser cette Visite"):
                        with st.spinner("⏳ Analyse en cours..."):
                            try:
                                from rag.query.query_bo5_medical import analyze_conversation
                                result = analyze_conversation(transcript, "Analyse Objections", top_k=5)
                                st.session_state.bo5_test_result = result
                            except Exception as e:
                                st.error(f"Erreur: {e}")
                    
                    if st.session_state.bo5_test_result:
                        result = st.session_state.bo5_test_result
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("**Ground Truth (Dataset)**")
                            st.write(f"Objection: {selected.get('main_objection_type', 'N/A')}")
                            st.write(f"Sentiment: {selected.get('sentiment_score', 'N/A')}")
                            st.write(f"Intérêt: {selected.get('interest_level', 'N/A')}")
                        
                        with col2:
                            st.markdown("**Prédiction IA**")
                            st.write(f"Objection: {result.get('predicted_main_objection', 'N/A')}")
                            st.write(f"Sentiment: {result.get('predicted_sentiment', 0):.2f}")
                            st.write(f"Intérêt: {result.get('predicted_interest', 0)}")
                        
                        if result.get('predicted_main_objection') == selected.get('main_objection_type'):
                            st.success("✅ Objection correctement prédite !")
                        else:
                            st.warning("⚠️ Objection ne correspond pas")
            
            elif test_mode == "📋 Batch Test (N visites)":
                batch_size = st.slider("Nombre de visites à tester", 5, min(30, len(df)), 10)
                
                if st.button(f"🚀 Lancer Batch Test ({batch_size} visites)"):
                    from rag.query.query_bo5_medical import analyze_conversation
                    
                    sample_df = df.sample(min(batch_size, len(df)))
                    results_batch = []
                    
                    progress_bar = st.progress(0)
                    for i, (_, row) in enumerate(sample_df.iterrows()):
                        try:
                            transcript = row.get('transcript', row.get('text', str(row)))
                            result = analyze_conversation(transcript, "Analyse Objections", top_k=3)
                            predicted = result.get('predicted_main_objection')
                            truth = row.get('main_objection_type')
                            match = predicted == truth
                            
                            results_batch.append({
                                'Ground Truth': truth,
                                'Prédiction': predicted,
                                'Match': '✅' if match else '❌',
                                'Confiance': f"{result.get('predicted_objection_score', 0):.2f}"
                            })
                        except Exception as e:
                            st.warning(f"⚠️ Erreur visite {i}")
                        
                        progress_bar.progress((i + 1) / len(sample_df))
                    
                    # Résultats
                    st.subheader("📊 Résultats du Batch")
                    results_df = pd.DataFrame(results_batch)
                    st.dataframe(results_df, use_container_width=True)
                    
                    # Metrics
                    correct = sum(1 for r in results_batch if r['Match'] == '✅')
                    accuracy = correct / len(results_batch) if results_batch else 0
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Tests Réussis", len(results_batch))
                    with col2:
                        st.metric("Prédictions Correctes", correct)
                    with col3:
                        st.metric("Accuracy", f"{accuracy:.1%}")
            
            elif test_mode == "🧠 Évaluer Modèle Complet":
                if st.button("🧠 Évaluer le Classifier ML"):
                    with st.spinner("⏳ Évaluation du modèle en cours..."):
                        try:
                            from rag.query.query_bo5_medical import evaluate_objection_classifier
                            eval_report = evaluate_objection_classifier()
                            
                            st.success(f"✅ Évaluation Terminée")
                            
                            # Metrics principales
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.metric("Accuracy", f"{eval_report['validation_accuracy']:.1%}")
                            with col2:
                                st.metric("Train Accuracy", f"{eval_report['train_accuracy']:.1%}")
                            with col3:
                                st.metric("Total Samples", eval_report['total'])
                            with col4:
                                st.metric("Correct", eval_report['correct'])
                            
                            # Classification Report
                            st.subheader("📊 Rapport de Classification")
                            report_df = pd.DataFrame(eval_report['classification_report']).transpose()
                            st.dataframe(report_df, use_container_width=True)
                            
                            # Predictions détaillées
                            st.subheader("🔍 Exemples de Prédictions")
                            pred_df = pd.DataFrame(eval_report['predictions'][:10])
                            st.dataframe(pred_df, use_container_width=True)
                            
                        except Exception as e:
                            st.error(f"❌ Erreur évaluation: {str(e)}")
        
        except Exception as e:
            st.error(f"❌ Erreur chargement dataset CSV: {str(e)}")
    
    elif dataset_choice == "parapharmacie_vital_final_v2.json (Produits parapharmacie)":
        try:
            json_path = os.path.join(BACKEND_DIR, "data", "parapharmacie_vital_final_v2.json")
            with open(json_path, "r", encoding="utf-8") as f:
                products = json.load(f)
            
            st.success(f"✅ Dataset chargé: {len(products)} produits")
            
            # Preview
            st.subheader("👀 Aperçu Produits")
            df_prod = pd.DataFrame(products)
            st.dataframe(df_prod[['name', 'gamme']].head(10) if 'name' in df_prod.columns else df_prod.head(10), use_container_width=True)
            
            # Stats
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Produits", len(products))
            with col2:
                st.info("Test RAG Retrieval: Chercher dans la base de produits")
        
        except Exception as e:
            st.error(f"❌ Erreur dataset JSON: {str(e)}")