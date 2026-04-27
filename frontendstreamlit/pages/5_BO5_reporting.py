# ========================================
# BO5 REPORTING avec RAG + GROQ
# ========================================
import streamlit as st

# Pre-load and cache embedding models
try:
    from cached_models import load_finetuned_model, load_standard_model

    _ = load_finetuned_model()
    _ = load_standard_model()  # ✅ IMPORTANT ()

except Exception as e:
    print("⚠️ Model preload failed:", e)

import pandas as pd
import sys
import os
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from fpdf import FPDF
import re
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.insert(0, BASE_DIR)
from ai_backend.rag.query.query_bo5_medical import analyze_conversation

print(os.path.exists("../../fonts/DejaVuSans.ttf"))
print(os.path.exists("../../fonts/DejaVuSans-Bold.ttf"))


@st.cache_data
def load_products_safe():
    try:
        path = os.path.join(
            os.path.dirname(__file__),
            "../../ai_backend/data/parapharmacie_vital_final_v2.json",
        )

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    except Exception as e:
        st.error(f"❌ Erreur chargement produits: {e}")


# ========================================
# 🧠 INIT SESSION STATE
# ========================================
if "products_data" not in st.session_state:
    st.session_state["products_data"] = load_products_safe()

if "bo5_rapport_type" not in st.session_state:
    st.session_state["bo5_rapport_type"] = "manuel"

if "bo5_result" not in st.session_state:
    st.session_state["bo5_result"] = {}

# ========================================
# 🔐 SAFE ACCESS (IMPORTANT)
# ========================================
products_data = st.session_state.get("products_data", [])

# ========================================
# FIX PATHS
# ========================================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
BACKEND_DIR = os.path.join(BASE_DIR, "ai_backend")

# Ajouter la racine au début du path
sys.path.insert(0, BASE_DIR)


# ========================================
# FONCTION POUR SAUVEGARDER DANS CRM (MONGODB)
# ========================================
import requests


def save_report_to_crm(
    transcript,
    doctor_name,
    delegate_name,
    objections_detected,
    main_objection_type,
    strategies,
    sentiment,
    interest,
    visit_score,
    json_data,
    # 🔥 NOUVEAUX PARAMÈTRES
    detected_language=None,
    medical_specialty=None,
    engagement=None,
    detected_needs=None,
    client_typology=None,
    proposed_product=None,
    report_date=None,
):
    """Sauvegarde le rapport dans MongoDB via l'API Node.js"""
    try:
        # URL de l'API Node.js
        API_URL = "http://localhost:5000/api/reports"

        print(f"[DEBUG] Tentative de sauvegarde sur {API_URL}")

        # Données à envoyer
        payload = {
            "doctor_id": "DOC_001",  # Statique pour maintenant
            "doctor_name": doctor_name,
            "delegate_name": delegate_name or "Délégué",
            "transcript": transcript,
            "objections_detected": objections_detected,
            "main_objection_type": main_objection_type,
            "strategies": strategies,
            "sentiment": float(sentiment) if sentiment else 0,
            "interest": float(interest) if interest else 0,
            "visit_score": float(visit_score) if visit_score else 0,
            "json_data": json_data,
            # 🔥 NOUVEAUX CHAMPS (ne pas utiliser 'or' car cela remplace les valeurs légitimes)
            "detected_language": detected_language if detected_language is not None else "FRANÇAIS",
            "medical_specialty": medical_specialty if medical_specialty is not None else "Médecine Générale",
            "engagement": engagement if engagement is not None else {"obtained": False, "score": 0, "indicators": []},
            "detected_needs": detected_needs if detected_needs is not None else [],
            "client_typology": client_typology if client_typology is not None else {"primary": "Analysant", "confidence": 0},
            "proposed_product": proposed_product if proposed_product is not None else "Non spécifié",
            "report_date": report_date if report_date is not None else datetime.now().isoformat(),
        }

        print(f"[DEBUG] Payload créé avec {len(str(payload))} caractères")

        # Envoyer la requête POST
        response = requests.post(API_URL, json=payload, timeout=10)

        print(f"[DEBUG] Status code reçu: {response.status_code}")
        print(f"[DEBUG] Response body: {response.text[:300]}")

        if response.status_code == 201:
            data = response.json()
            print(f"[DEBUG] Sauvegarde réussie: {data}")
            return {
                "success": True,
                "message": data.get("message", "✅ Rapport sauvegardé"),
                "visit_id": data.get("visit_id"),
                "report_id": data.get("report_id"),
            }
        else:
            print(f"[DEBUG] Erreur {response.status_code}")
            return {
                "success": False,
                "message": f"❌ Erreur {response.status_code}: {response.text}",
            }

    except requests.exceptions.ConnectionError as e:
        print(f"[DEBUG] Erreur de connexion: {str(e)}")
        return {
            "success": False,
            "message": "❌ Erreur: Impossible de se connecter au serveur CRM (Node.js). Assurez-vous que le backend est lancé sur http://localhost:5000",
        }
    except Exception as e:
        print(f"[DEBUG] Erreur générale: {str(e)}")
        import traceback

        print(traceback.format_exc())
        return {
            "success": False,
            "message": f"❌ Erreur lors de la sauvegarde: {str(e)}",
        }


# ========================================
# FONCTION POUR GÉNÉRER PDF
# ========================================
def generate_pdf_report(result: dict, rapport_type: str) -> bytes:
    """Génère un PDF complet et détaillé du rapport"""
    try:
        pdf = FPDF(format="A4", unit="mm")
        pdf.set_margins(6, 6, 6)
        pdf.add_page()

        # Charger les fonts
        font_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../fonts")
        )
        pdf.add_font("DejaVu", "", os.path.join(font_dir, "DejaVuSans.ttf"), uni=True)
        pdf.add_font(
            "DejaVu", "B", os.path.join(font_dir, "DejaVuSans-Bold.ttf"), uni=True
        )

        # ========================================
        # HEADER
        # ========================================
        pdf.set_font("DejaVu", "B", 13)
        pdf.set_text_color(25, 118, 210)
        pdf.multi_cell(0, 5, "RAPPORT BO5", align="L")
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("DejaVu", "", 7)
        pdf.multi_cell(0, 3, "Analyse Intelligente de Visite Medicale", align="L")
        
        # Ligne séparation
        pdf.set_draw_color(25, 118, 210)
        pdf.line(6, pdf.get_y(), 204, pdf.get_y())
        pdf.ln(0.5)

        # Date et type
        pdf.set_font("DejaVu", "", 6)
        date_text = f"Date: {datetime.now().strftime('%d/%m/%Y %H:%M')} | Type: {rapport_type}"
        pdf.multi_cell(0, 2.5, date_text, align="L")
        pdf.ln(0.3)

        # ========================================
        # SECTION 1: METRIQUES
        # ========================================
        pdf.set_font("DejaVu", "B", 8)
        pdf.set_text_color(25, 118, 210)
        pdf.multi_cell(0, 3, "METRIQUES CLES", align="L")
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("DejaVu", "", 6)

        detected_language = result.get("detected_language", "FRANCAIS")
        medical_specialty = result.get("medical_specialty", "Medecine Generale")
        visit_score = result.get("visit_score", 0)
        sentiment = result.get("predicted_sentiment", 0)
        interest = result.get("predicted_interest", 0)

        # Utiliser multi_cell pour éviter les problèmes d'espace
        pdf.multi_cell(0, 2, f"Langue: {detected_language} | Specialite: {medical_specialty[:25]} | Score: {visit_score}/100 | Sentiment: {sentiment:.1f} | Interet: {interest}%", align="L")
        pdf.ln(0.2)

        # ========================================
        # SECTION 2: RESUME
        # ========================================
        pdf.set_font("DejaVu", "B", 8)
        pdf.set_text_color(25, 118, 210)
        pdf.multi_cell(0, 3, "RESUME DE LA VISITE", align="L")
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("DejaVu", "", 6)

        analysis_text = result.get("analysis", "Pas d'analyse")
        pdf.multi_cell(0, 2.5, analysis_text[:350], align="L")
        pdf.ln(0.2)

        # ========================================
        # SECTION 3: INFORMATIONS DETAILLEES
        # ========================================
        pdf.set_font("DejaVu", "B", 8)
        pdf.set_text_color(25, 118, 210)
        pdf.multi_cell(0, 3, "INFORMATIONS DETAILLEES", align="L")
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("DejaVu", "", 6)

        engagement = result.get("engagement", {})
        engagement_status = "OUI" if engagement.get("obtained") else "NON"
        engagement_score = int(engagement.get("score", 0)*100)
        pdf.multi_cell(0, 2, f"Engagement: {engagement_status} ({engagement_score}%)", align="L")

        detected_needs = result.get("detected_needs", [])
        needs = ", ".join(detected_needs) if detected_needs else "Aucun"
        pdf.multi_cell(0, 2, f"Besoins Detectes: {needs[:65]}", align="L")

        client_typology = result.get("client_typology", {})
        profile = client_typology.get("primary", "N/A")
        confidence = int(client_typology.get("confidence", 0)*100)
        pdf.multi_cell(0, 2, f"Profil Client: {profile} ({confidence}%)", align="L")

        proposed_product = result.get("proposed_product", "N/A")
        pdf.multi_cell(0, 2, f"Produit Propose: {proposed_product[:55]}", align="L")
        pdf.ln(0.2)

        # ========================================
        # SECTION 4: OBJECTIONS
        # ========================================
        objections = result.get("objections", [])
        if objections:
            pdf.set_font("DejaVu", "B", 8)
            pdf.set_text_color(25, 118, 210)
            pdf.multi_cell(0, 3, f"OBJECTIONS DETAILLEES ({len(objections)})", align="L")
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("DejaVu", "", 6)

            for i, obj in enumerate(objections[:4], 1):
                obj_type = obj.get("type", "N/A")
                obj_text = obj.get("text", "")[:50]
                pdf.multi_cell(0, 1.8, f"{i}. {obj_type}: {obj_text}", align="L")
            pdf.ln(0.2)

        # ========================================
        # SECTION 5: STRATEGIES
        # ========================================
        strategies = result.get("objections", [])
        if strategies:
            pdf.set_font("DejaVu", "B", 8)
            pdf.set_text_color(25, 118, 210)
            pdf.multi_cell(0, 3, "STRATEGIES DE REPONSE", align="L")
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("DejaVu", "", 6)

            for i, obj in enumerate(strategies[:3], 1):
                strategy = obj.get("strategy", "")
                if strategy:
                    pdf.multi_cell(0, 1.8, f"{i}. {strategy[:70]}", align="L")
            pdf.ln(0.2)

        # ========================================
        # SECTION 6: PRODUITS RECOMMANDES
        # ========================================
        recommended_products = result.get("recommended_products", [])
        if recommended_products:
            pdf.set_font("DejaVu", "B", 8)
            pdf.set_text_color(25, 118, 210)
            pdf.multi_cell(0, 3, f"PRODUITS RECOMMANDES ({len(recommended_products)})", align="L")
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("DejaVu", "", 6)

            for i, prod in enumerate(recommended_products[:4], 1):
                prod_name = prod.get("name", "N/A")[:50]
                prod_score = prod.get("score", 0)
                pdf.multi_cell(0, 1.8, f"{i}. {prod_name} (Score: {prod_score}/100)", align="L")
            pdf.ln(0.2)

        # ========================================
        # SECTION 7: STATISTIQUES
        # ========================================
        pdf.set_font("DejaVu", "B", 8)
        pdf.set_text_color(25, 118, 210)
        pdf.multi_cell(0, 3, "STATISTIQUES", align="L")
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("DejaVu", "", 6)

        key_points = result.get("key_points", {})
        for key, value in list(key_points.items())[:5]:
            pdf.multi_cell(0, 1.8, f"{key}: {value}", align="L")
        pdf.ln(0.2)

        # ========================================
        # SECTION 8: SOURCES
        # ========================================
        sources = result.get("sources", [])
        if sources:
            pdf.set_font("DejaVu", "B", 8)
            pdf.set_text_color(25, 118, 210)
            pdf.multi_cell(0, 3, f"SOURCES UTILISEES ({len(sources)})", align="L")
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("DejaVu", "", 5)

            for i, source in enumerate(sources[:4], 1):
                content = source.get("content", "")[:45]
                score = source.get("score", 0)
                pdf.multi_cell(0, 1.5, f"{i}. {content}... (score: {score:.2f})", align="L")
            pdf.ln(0.2)

        # ========================================
        # FOOTER
        # ========================================
        pdf.set_draw_color(25, 118, 210)
        pdf.line(6, pdf.get_y(), 204, pdf.get_y())
        pdf.set_font("DejaVu", "", 5)
        pdf.set_text_color(100, 100, 100)
        pdf.multi_cell(0, 2, "Rapport genere par systeme BO5 - Confidential | AVA", align="L")

        pdf_output = pdf.output(dest="S")
        return bytes(pdf_output)
    except Exception as e:
        print(f"[PDF ERROR] {str(e)}")
        raise


# ========================================
# PAGE CONFIG
# ========================================
st.set_page_config(page_title="BO5 - Reporting", layout="wide", page_icon="📄")

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
    ["Analyse Objections", "Synthèse Produits", "Recommandations", "Statistiques"],
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
        DÉLÉGUÉ: En stock. 35 euros par boîte 30 gélules, très compétitif""",
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
    "Dialogue complet:", value=exemples[choix], height=250, key="dialogue_textarea"
)
col1, col2 = st.columns([3, 1])

with col1:
    st.write("**Format attendu:** Alternez DÉLÉGUÉ: et MÉDECIN:")

with col2:
    generate_btn = st.button("🚀 Générer Rapport ", use_container_width=True)

# Vérifier si un rapport existe déjà en session_state
# Si oui, l'afficher directement sans avoir besoin de regénérer
if "bo5_result" in st.session_state and st.session_state.bo5_result:
    st.info("✅ Rapport généré trouvé en mémoire (cliquez pour regénérer)")
    use_existing = True
else:
    use_existing = False

if generate_btn or use_existing:
    if not use_existing and not query_input.strip():
        st.error("❌ Veuillez entrer la conversation")
    else:
        if generate_btn:
            # Regénérer le rapport
            with st.spinner("⏳ Analyse de la discussion..."):
                try:
                    # Analyser la conversation complète
                    result = analyze_conversation(
                        dialogue=query_input, rapport_type=rapport_type, top_k=top_k
                    )

                    # Sauvegarder dans session_state pour persister entre les reruns
                    st.session_state.bo5_result = result
                    st.session_state.bo5_query_input = query_input
                    st.session_state.bo5_rapport_type = rapport_type

                except Exception as e:
                    st.error(f"❌ Erreur lors de l'analyse: {str(e)}")
                    import traceback

                    st.code(traceback.format_exc())

        # Afficher le rapport (soit généré, soit depuis session_state)
        if "bo5_result" in st.session_state:
            result = st.session_state.bo5_result
            query_input_display = st.session_state.bo5_query_input
            rapport_type_display = st.session_state.bo5_rapport_type

            # Display Response
            st.success("✅ Rapport généré!")

# ========================================
# 📤 UPLOAD CONVERSATION (PDF / JSON)
# ========================================
st.markdown("### 📤 Upload Conversation (PDF / JSON)")

uploaded_file = st.file_uploader("Choisir un fichier", type=["pdf", "json"])

# ---------- PDF ----------
import PyPDF2


def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""

    for page in reader.pages:
        text += page.extract_text() + "\n"

    return text


# ---------- JSON ----------
import json


def extract_text_from_json(file):
    data = json.load(file)

    if isinstance(data, dict):
        return data.get("dialogue", str(data))

    elif isinstance(data, list):
        return "\n".join(str(item) for item in data)

    return ""


# ---------- PROCESS ----------
if uploaded_file:

    if uploaded_file.type == "application/pdf":
        dialogue = extract_text_from_pdf(uploaded_file)

    elif uploaded_file.type == "application/json":
        dialogue = extract_text_from_json(uploaded_file)

    else:
        dialogue = ""

    st.text_area("📄 Conversation extraite", dialogue, height=200)

    if st.button("🚀 Analyser le fichier uploadé"):

        result = analyze_conversation(dialogue)

        st.session_state["bo5_result"] = result
        st.session_state["bo5_query_input"] = dialogue

        st.success("✅ Analyse terminée !")

        # ========================================
# 📋 Résumé de la Visite (MANUEL + UPLOAD)
# ========================================
# ========================================
# 📋 Résumé de la Visite (AFFICHAGE CONDITIONNEL)
# ========================================

if "bo5_result" in st.session_state:

    result = st.session_state.get("bo5_result", {})

    st.markdown("---")
    st.markdown("### 📋 Résumé de la Visite")

    try:
        from services.rag_service import generate_response

        # 🔥 IMPORTANT : prendre bon texte
        dialogue_text = st.session_state.get("bo5_query_input", "")

        resume_prompt = f"""
Fais un résumé DIRECT sans introduction.
3-4 lignes maximum.

Conversation:
{dialogue_text}
"""

        resume = generate_response(
            query=resume_prompt,
            context_docs=[],
            system_prompt="Tu es un expert en visites médicales. Sois très concis.",
        )

        if resume and resume.strip():
            st.markdown(f"**{resume}**")
        else:
            raise Exception("Empty response")

    except:
        # fallback
        analysis_text = result.get("analysis", "")

        if analysis_text:
            fallback = "\n".join(analysis_text.split("\n")[:3])
            st.markdown(f"**{fallback}**")
        else:
            st.info("ℹ️ Aucun résumé disponible")

        # ========================================
        # DÉTAILS DÉPLIABLES
        # ========================================
        st.markdown("---")
        st.markdown("### 📖 Détails Complets")

        # Stats du rapport
        num_objections = len(result.get("objections", []))
        num_sources = len(result.get("sources", []))
        avg_score = (
            sum(s["score"] for s in result.get("sources", [])) / num_sources
            if num_sources > 0
            else 0
        )

        # 🔥 NEW: Afficher les informations générales du rapport
        st.markdown("---")
        # ========================================
        # 🎯 AMÉLIORATIONS - NOUVELLE INTERFACE
        # ========================================
if "bo5_result" in st.session_state:

    result = st.session_state.bo5_result

    card_style = """
    background: linear-gradient(145deg, #1e1e2f, #2a2a40);
    padding:20px;
    border-radius:15px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    color:white;
    text-align:center;
    """

    col1, col2, col3 = st.columns(3)

    # 🌐 LANGUE
    with col1:
        st.markdown(
            f"""
    <div style="{card_style}">
        <div style="font-size:14px;color:#aaa;">🌐 Langue</div>
        <div style="font-size:28px;font-weight:bold;">
            {result.get("detected_language")}
        </div>
    </div>
    """,
            unsafe_allow_html=True,
        )

    # 👨‍⚕️ SPÉCIALITÉ
    with col2:
        st.markdown(
            f"""
    <div style="{card_style}">
        <div style="font-size:14px;color:#aaa;">👨‍⚕️ Spécialité</div>
        <div style="font-size:28px;font-weight:bold;">
            {result.get("medical_specialty")}
        </div>
    </div>
    """,
            unsafe_allow_html=True,
        )

    # ⭐ SCORE
    with col3:
        score = result.get("visit_score", 0)

        color = "#4CAF50" if score >= 80 else "#FFC107" if score >= 60 else "#F44336"

        st.markdown(
            f"""
    <div style="{card_style}">
        <div style="font-size:14px;color:#aaa;">⭐ Performance</div>
        <div style="font-size:32px;font-weight:bold;color:{color};">
            {score}/100
        </div>
    </div>
    """,
            unsafe_allow_html=True,
        )

    # ========================================
    # Section 2: ENGAGEMENT (Détaillé)
    # ========================================

if "bo5_result" in st.session_state:

    result = st.session_state.bo5_result

    st.markdown("---")
    st.markdown("### 💼 Engagement Client")

    engagement = result.get("engagement", {})
    engagement_obtained = engagement.get("obtained", False)
    engagement_score = engagement.get("score", 0)
    engagement_indicators = engagement.get("indicators", [])

    col1, col2 = st.columns([1.5, 2])

    # 🎯 LEFT SIDE
    with col1:
        if engagement_obtained:
            st.success("✅ **ENGAGEMENT OBTENU**")
        else:
            st.warning("❌ **ENGAGEMENT À CONFIRMER**")

        st.progress(
            value=min(1.0, engagement_score), text=f"Score: {engagement_score:.0%}"
        )

    # 📊 RIGHT SIDE
    with col2:
        st.markdown("**Indicateurs Détectés:**")

        if engagement_indicators:
            for indicator in engagement_indicators[:5]:

                indicator_clean = indicator.replace("✅", "").replace("❌", "").strip()

                if (
                    "✅" in indicator
                    or "oui" in indicator.lower()
                    or "accord" in indicator.lower()
                ):
                    st.markdown(f"✅ {indicator_clean}")
                else:
                    st.markdown(f"❌ {indicator_clean}")
        else:
            st.markdown("*Aucun indicateur détecté*")

# ========================================
# Section 3: BESOINS DÉTECTÉS
# ========================================
if "bo5_result" in st.session_state:

    result = st.session_state.bo5_result
    st.markdown("---")
    st.markdown("### 🏥 Besoins Détectés")

    detected_needs = result.get("detected_needs", [])

    if detected_needs:

        # 🔥 couleurs par type de besoin
        color_map = {
            "Fatigue": "#ff9800",
            "Infection": "#f44336",
            "Stress": "#2196f3",
            "Immunité": "#4caf50",
            "Cardiovasculaire": "#9c27b0",
        }

        cols = st.columns(min(4, len(detected_needs)))

        for idx, need in enumerate(detected_needs[:4]):
            with cols[idx % len(cols)]:

                color = color_map.get(need, "#444")

                st.markdown(
                    f"""
                    <div style="
                        background:{color};
                        padding:12px;
                        border-radius:10px;
                        text-align:center;
                        color:white;
                        font-weight:bold;
                        box-shadow:0 2px 6px rgba(0,0,0,0.3);
                    ">
                        {need}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        # 🔥 besoins supplémentaires
        if len(detected_needs) > 4:
            st.markdown(
                f"**➕ Et {len(detected_needs) - 4} autre(s) besoin(s):** {', '.join(detected_needs[4:])}"
            )

    else:
        st.info("ℹ️ Aucun besoin spécifique détecté dans cette visite")

# ========================================
# Section 4: PROFIL CLIENT (4 Typologies)
# ========================================


if "bo5_result" in st.session_state:
    result = st.session_state.bo5_result

    st.markdown("---")
    st.markdown("### 👤 Profil du Client")

    # ✅ ICI (indenté)
    client_typology = result.get("client_typology", {})

    if client_typology:
        primary_type = client_typology.get("primary", "Analysant")
        confidence = client_typology.get("confidence", 0)
        all_types = client_typology.get("all_types", {})

        col1, col2 = st.columns([1, 2])

        # 🎯 LEFT SIDE
        with col1:
            st.markdown(f"**Profil Principal:** {primary_type}")
            st.progress(confidence, text=f"Confiance: {confidence:.0%}")

        # 🎨 RADAR
        with col2:
            if all_types:

                categories = list(all_types.keys())
                values = list(all_types.values())

                categories.append(categories[0])
                values.append(values[0])

                fig = go.Figure()

                fig.add_trace(
                    go.Scatterpolar(
                        r=values,
                        theta=categories,
                        fill="toself",
                        line=dict(color="#00AEEF", width=3),
                        fillcolor="rgba(0, 174, 239, 0.3)",
                    )
                )

                fig.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                    showlegend=False,
                    template="plotly_dark",
                    height=400,
                )

                st.plotly_chart(fig, use_container_width=True)

# ========================================
# Section 5: PRODUIT PROPOSÉ
# ========================================

# Initialize products_data in session_state if not present
if "products_data" not in st.session_state:
    try:
        # Try multiple possible paths
        possible_paths = [
            os.path.join("ai_backend", "data", "parapharmacie_vital_final_v2.json"),
            os.path.join(
                "..", "ai_backend", "data", "parapharmacie_vital_final_v2.json"
            ),
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "..",
                "ai_backend",
                "data",
                "parapharmacie_vital_final_v2.json",
            ),
        ]

        products_raw = None
        for path in possible_paths:
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    products_raw = json.load(f)
                break

        if products_raw:
            # Filter products without 'name' field to avoid KeyError
            st.session_state.products_data = [
                p for p in products_raw if "name" in p and p["name"]
            ]
        else:
            st.warning("⚠️ Fichier produits non trouvé")
            st.session_state.products_data = []

    except Exception as e:
        st.error(f"❌ Erreur chargement produits: {e}")
        st.session_state.products_data = []

# Safely get products_data from session_state
products_data = st.session_state.products_data

# ========================================
# 🧠 TEXTE CONVERSATION
# ========================================
text = ""

if "bo5_query_input" in st.session_state:
    text = st.session_state.bo5_query_input.lower()

# ========================================
# 💊 PRODUIT PROPOSÉ
# ========================================
if "bo5_result" in st.session_state:

    result = st.session_state.bo5_result

    st.markdown("---")
    st.markdown("### 💊 Produit Proposé")

    main_product = result.get("proposed_product")

    if main_product and main_product != "Non spécifié":

        st.markdown(
            f"""
        <div style="
            background: linear-gradient(135deg, #1b5e20, #2e7d32);
            padding:18px;
            border-radius:12px;
            color:white;
            font-size:18px;
            font-weight:bold;
            box-shadow:0 4px 15px rgba(0,0,0,0.3);
        ">
            💊 Produit proposé : {main_product}
        </div>
        """,
            unsafe_allow_html=True,
        )

    else:
        st.warning("⚠️ Aucun produit détecté")


# ========================================
# 💡 PRODUITS RECOMMANDÉS
# ========================================
if "bo5_result" in st.session_state:

    result = st.session_state.bo5_result

    st.markdown("---")
    st.markdown("### 💊 Produits Recommandés")

    recommended_products = result.get("recommended_products", [])

    if recommended_products:

        for p in recommended_products:
            st.markdown(
                f"""
            <div style="
                background:#1e1e2f;
                padding:15px;
                border-radius:10px;
                margin-bottom:10px;
                color:white;
                border:1px solid #333;
            ">
                <b>💊 {p['name']}</b><br>
                ⭐ Score: {p['score']}<br>
                💡 Pourquoi: {p['why']}
            </div>
            """,
                unsafe_allow_html=True,
            )

    else:
        st.info("ℹ️ Aucun produit recommandé")

    # ========================================
# 📊 ANALYSE DE LA VISITE (MANUEL + UPLOAD)
# ========================================
# ========================================
# 📊 ANALYSE DE LA VISITE (UNIQUE)
# ========================================
if "bo5_result" in st.session_state:

    result = st.session_state.get("bo5_result", {})
    analysis = result.get("analysis", "Non disponible")

    dialogue_text = st.session_state.get("bo5_query_input", "")
    if not dialogue_text:
        dialogue_text = st.session_state.get("uploaded_dialogue", "")

    objections = result.get("objections", []) or []
    num_objections = len(objections)

    sources = result.get("sources", []) or []
    num_sources = len(sources)

    avg_score = (
        sum(s.get("score", 0) for s in sources) / num_sources if num_sources > 0 else 0
    )

    st.markdown("---")
    st.markdown("## 📊 Analyse de la Visite")

    # 1. Analyse complète
    with st.expander("Voir l'analyse complète", expanded=False):
        st.markdown(analysis)

    # 2. Analyse détaillée
    with st.expander("🎯 Analyse détaillée de la visite", expanded=False):
        try:
            from services.rag_service import generate_response

            # Utiliser le contexte disponible du résultat
            context_docs = result.get("sources", [])
            if not context_docs and result.get("analysis"):
                context_docs = [{"content": result.get("analysis", "")}]
            
            client_profile = result.get("client_typology", {}).get("primary", "Général")
            medical_specialty = result.get("medical_specialty", "Non détectée")

            insights_prompt = f"""
Analyse cette visite médicale et donne une évaluation structurée :

1. Points forts (2-3 éléments positifs observés)
2. Points d'amélioration (2-3 domaines à travailler)
3. Recommandations concrètes (2-3 actions spécifiques)
4. Stratégies adaptées au profil client: {client_profile}
5. Contexte de spécialité: {medical_specialty}

Conversation:
{dialogue_text}
"""

            insights = generate_response(
                query=insights_prompt,
                context_docs=context_docs if context_docs else [{"content": "Analyse basée sur la visite médicale"}],
                system_prompt="Tu es un expert senior en ventes médicales. Fournis une analyse structurée, constructive et actionnelle basée sur les faits observés.",
            )

            if insights and insights.strip():
                st.markdown(insights)
            else:
                st.info("ℹ️ Analyse détaillée non disponible")

        except Exception as e:
            st.warning(f"⚠️ Impossible de générer l'analyse détaillée : {str(e)}")

    # 3. Points clés
    with st.expander("🎯 Points Clés & Statistiques", expanded=False):
        key_points = result.get("key_points", {}) or {}

        if key_points:
            key_points_data = pd.DataFrame(
                [
                    {"Métrique": key, "Valeur": value}
                    for key, value in key_points.items()
                ]
            )
            st.dataframe(key_points_data, use_container_width=True)
        else:
            st.info("ℹ️ Aucun point clé disponible")

    # 4. Objections
    with st.expander(f"🚫 Objections Détectées ({num_objections})", expanded=False):
        if objections:
            objections_data = pd.DataFrame(
                [
                    {
                        "Objection": obj.get("type", "N/A"),
                        "Énoncé": (
                            obj.get("text", "")[:50] + "..."
                            if len(obj.get("text", "")) > 50
                            else obj.get("text", "")
                        ),
                    }
                    for obj in objections
                ]
            )
            st.dataframe(objections_data, use_container_width=True)

            st.markdown("**✅ Stratégies de Réponse :**")
            for obj in objections:
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.write(f"**{obj.get('type', 'N/A')}**")
                with col2:
                    st.write(obj.get("strategy", "Non disponible"))
        else:
            st.info("ℹ️ Aucune objection détectée")

    # 5. Sources
    with st.expander(f"📚 Sources Utilisées ({num_sources})", expanded=False):
        if num_sources > 0:
            st.info(f"Score moyen de pertinence : **{avg_score:.2f}**")
            for source in sources:
                col1, col2 = st.columns([1, 4])
                with col1:
                    st.metric("Score", f"{source.get('score', 0):.2f}")
                with col2:
                    st.write(source.get("content", "")[:300] + "...")
        else:
            st.info("ℹ️ Aucune source utilisée")

    # Export
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        try:
            pdf_bytes = generate_pdf_report(
                st.session_state.bo5_result, st.session_state.bo5_rapport_type
            )
            st.download_button(
                label="📥 Télécharger en PDF",
                data=pdf_bytes,
                file_name=f"rapport_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf",
            )
        except Exception as e:
            st.error(f"❌ Erreur PDF: {str(e)}")

    with col2:
        if st.button("📊 Exporter en JSON"):
            st.download_button(
                label="Télécharger JSON",
                data=str(st.session_state.bo5_result),
                file_name=f"rapport_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            )

    with col3:
        if st.button("💾 Sauvegarder"):
            try:
                from rag.query.query_bo5_medical import save_rapport

                filepath = save_rapport(st.session_state.bo5_result)
                st.success(f"✅ Rapport sauvegardé !\n📁 {filepath}")
            except Exception as e:
                st.error(f"❌ Erreur sauvegarde: {str(e)}")
                import traceback

                st.code(traceback.format_exc())

    # 🆕 BOUTON SAUVEGARDER DANS CRM (MONGODB)
    with col4:
        if st.button("🗄️ Sauvegarder dans CRM", key="save_crm_btn"):
            print("[STREAMLIT DEBUG] Bouton cliqué !")

            with st.spinner("📤 Sauvegarde dans MongoDB..."):
                try:
                    # Préparer les données
                    objections_list = [
                        obj["type"]
                        for obj in st.session_state.bo5_result.get("objections", [])
                    ]
                    strategies_dict = {
                        obj["type"]: obj["strategy"]
                        for obj in st.session_state.bo5_result.get("objections", [])
                    }

                    # Sentiments et intérêt (à extraire ou par défaut)
                    sentiment_val = st.session_state.bo5_result.get(
                        "predicted_sentiment", 0
                    )
                    interest_val = st.session_state.bo5_result.get(
                        "predicted_interest", 70
                    )
                    visit_score_val = st.session_state.bo5_result.get("visit_score", 70)

                    print(
                        f"[STREAMLIT DEBUG] Données préparées: visit_score={visit_score_val}"
                    )

                    # 🔥 NOUVELLES DONNÉES
                    detected_language = st.session_state.bo5_result.get(
                        "detected_language", "FRANÇAIS"
                    )
                    medical_specialty = st.session_state.bo5_result.get(
                        "medical_specialty", "Médecine Générale"
                    )
                    engagement_data = st.session_state.bo5_result.get(
                        "engagement", {"obtained": False, "score": 0}
                    )
                    detected_needs = st.session_state.bo5_result.get(
                        "detected_needs", []
                    )
                    client_typology = st.session_state.bo5_result.get(
                        "client_typology", {}
                    )
                    proposed_product = st.session_state.bo5_result.get(
                        "proposed_product", "Non spécifié"
                    )
                    report_date = st.session_state.bo5_result.get(
                        "report_date", datetime.now().isoformat()
                    )

                    # Appeler la fonction de sauvegarde
                    crm_result = save_report_to_crm(
                        transcript=st.session_state.bo5_query_input[
                            :2000
                        ],  # Limiter la taille
                        doctor_name="Docteur Cardiologue",  # À adapter si data disponible
                        delegate_name="Délégué Médical",
                        objections_detected=objections_list,
                        main_objection_type=(
                            objections_list[0] if objections_list else None
                        ),
                        strategies=strategies_dict,
                        sentiment=sentiment_val,
                        interest=interest_val,
                        visit_score=visit_score_val,
                        json_data={
                            "analysis": st.session_state.bo5_result.get("analysis", "")[
                                :1000
                            ],
                            "objections_count": len(objections_list),
                            "sources_count": len(
                                st.session_state.bo5_result.get("sources", [])
                            ),
                        },
                        # 🔥 NOUVEAUX PARAMÈTRES
                        detected_language=detected_language,
                        medical_specialty=medical_specialty,
                        engagement=engagement_data,
                        detected_needs=detected_needs,
                        client_typology=client_typology,
                        proposed_product=proposed_product,
                        report_date=report_date,
                    )

                    print(f"[STREAMLIT DEBUG] Résultat: {crm_result}")

                    # Afficher le résultat IMMÉDIATEMENT
                    if crm_result["success"]:
                        st.success(crm_result["message"])
                        st.info(
                            f"📍 **Visit ID:** {crm_result['visit_id']}\n📋 **Report ID:** {crm_result['report_id']}"
                        )
                    else:
                        st.error(crm_result["message"])
                        st.error(f"Détail: {crm_result.get('message')}")

                except Exception as e:
                    print(f"[STREAMLIT ERROR] Exception: {str(e)}")
                    import traceback

                    print(traceback.format_exc())
                    st.error(f"❌ Erreur exception: {str(e)}")
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
        st.info("""...""")


# ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
# TAB 2: 🎯 FINE-TUNING TESTS
# ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

with tab2:
    st.header("🎯 Fine-tuning ML Classifier")
    st.write(
        "Testez et validez les performances du ML classifier avec les données VITAL"
    )

    # ========================================
    # DATASET SELECTION
    # ========================================
    st.subheader("📊 Sélection du Dataset")

    dataset_choice = st.selectbox(
        "Choisissez le dataset pour les tests:",
        [
            "vital_bo6_dataset.csv (Transcripts visites médicales)",
            "parapharmacie_vital_final_v2.json (Produits parapharmacie)",
        ],
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
                st.metric(
                    "Objections Uniques",
                    (
                        df["main_objection_type"].nunique()
                        if "main_objection_type" in df.columns
                        else 0
                    ),
                )
            with col3:
                avg_sentiment = (
                    df["sentiment_score"].mean()
                    if "sentiment_score" in df.columns
                    else 0
                )
                st.metric("Sentiment Moyen", f"{avg_sentiment:.2f}")

            # ========================================
            # TESTING OPTIONS
            # ========================================
            st.subheader("🧪 Tests Fine-tuning")

            # ========================================
            # SECTION FINE-TUNING
            # ========================================
            st.markdown("---")
            st.markdown("### 🔧 Fine-tuning du SentenceTransformer")

            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(
                    "Améliorez le modèle d'embeddings en le fine-tunant sur vos données médicales"
                )
            with col2:
                finetune_epochs = st.number_input(
                    "Epochs", min_value=1, max_value=5, value=2
                )

            if st.button("🚀 Lancer Fine-tuning Complet", use_container_width=True):
                with st.spinner("⏳ Fine-tuning en cours (peut prendre 2-5 min)..."):
                    try:
                        from rag.query.query_bo5_medical import full_finetuning_pipeline

                        result = full_finetuning_pipeline(epochs=int(finetune_epochs))

                        st.success("✅ Fine-tuning Terminé avec Succès !")

                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric(
                                "Train Accuracy", f"{result['train_accuracy']:.1%}"
                            )
                        with col2:
                            st.metric(
                                "Validation Accuracy",
                                f"{result['validation_accuracy']:.1%}",
                            )

                        st.info(
                            f"💡 Le modèle fine-tuné est sauvegardé et sera utilisé pour les prochaines analyses."
                        )

                    except Exception as e:
                        st.error(f"❌ Erreur fine-tuning: {str(e)}")
                        import traceback

                        st.code(traceback.format_exc())

            st.markdown("---")

            test_mode = st.radio(
                "Mode de test:",
                [
                    "🎲 Visite Aléatoire",
                    "📋 Batch Test (N visites)",
                    "🧠 Évaluer Modèle Complet",
                ],
                horizontal=True,
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
                    transcript = selected.get(
                        "transcript", selected.get("text", str(selected))
                    )

                    st.markdown("### 📝 Visite Sélectionnée")
                    st.text_area("Transcript:", transcript, height=200, disabled=True)

                    if st.button("🔍 Analyser cette Visite"):
                        with st.spinner("⏳ Analyse en cours..."):
                            try:
                                from rag.query.query_bo5_medical import (
                                    analyze_conversation,
                                )

                                result = analyze_conversation(
                                    transcript, "Analyse Objections", top_k=5
                                )
                                st.session_state.bo5_test_result = result
                            except Exception as e:
                                st.error(f"Erreur: {e}")

                    if st.session_state.bo5_test_result:
                        result = st.session_state.bo5_test_result

                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("**Ground Truth (Dataset)**")
                            st.write(
                                f"Objection: {selected.get('main_objection_type', 'N/A')}"
                            )
                            st.write(
                                f"Sentiment: {selected.get('sentiment_score', 'N/A')}"
                            )
                            st.write(
                                f"Intérêt: {selected.get('interest_level', 'N/A')}"
                            )

                        with col2:
                            st.markdown("**Prédiction IA**")
                            st.write(
                                f"Objection: {result.get('predicted_main_objection', 'N/A')}"
                            )
                            st.write(
                                f"Sentiment: {result.get('predicted_sentiment', 0):.2f}"
                            )
                            st.write(f"Intérêt: {result.get('predicted_interest', 0)}")

                        if result.get("predicted_main_objection") == selected.get(
                            "main_objection_type"
                        ):
                            st.success("✅ Objection correctement prédite !")
                        else:
                            st.warning("⚠️ Objection ne correspond pas")

            elif test_mode == "📋 Batch Test (N visites)":
                batch_size = st.slider(
                    "Nombre de visites à tester", 5, min(30, len(df)), 10
                )

                if st.button(f"🚀 Lancer Batch Test ({batch_size} visites)"):
                    sample_df = df.sample(min(batch_size, len(df)))
                    results_batch = []

                    progress_bar = st.progress(0)
                    for i, (_, row) in enumerate(sample_df.iterrows()):
                        try:
                            transcript = row.get(
                                "transcript", row.get("text", str(row))
                            )
                            result = analyze_conversation(
                                transcript, "Analyse Objections", top_k=3
                            )
                            predicted = result.get("predicted_main_objection")
                            truth = row.get("main_objection_type")
                            match = predicted == truth

                            results_batch.append(
                                {
                                    "Ground Truth": truth,
                                    "Prédiction": predicted,
                                    "Match": "✅" if match else "❌",
                                    "Confiance": f"{result.get('predicted_objection_score', 0):.2f}",
                                }
                            )
                        except Exception as e:
                            st.warning(f"⚠️ Erreur visite {i}")

                        progress_bar.progress((i + 1) / len(sample_df))

                    # Résultats
                    st.subheader("📊 Résultats du Batch")
                    results_df = pd.DataFrame(results_batch)
                    st.dataframe(results_df, use_container_width=True)

                    # Metrics
                    correct = sum(1 for r in results_batch if r["Match"] == "✅")
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
                            from rag.query.query_bo5_medical import (
                                evaluate_objection_classifier,
                            )

                            eval_report = evaluate_objection_classifier()

                            st.success(f"✅ Évaluation Terminée")

                            # Metrics principales
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.metric(
                                    "Accuracy",
                                    f"{eval_report['validation_accuracy']:.1%}",
                                )
                            with col2:
                                st.metric(
                                    "Train Accuracy",
                                    f"{eval_report['train_accuracy']:.1%}",
                                )
                            with col3:
                                st.metric("Total Samples", eval_report["total"])
                            with col4:
                                st.metric("Correct", eval_report["correct"])

                            # Classification Report
                            st.subheader("📊 Rapport de Classification")
                            report_df = pd.DataFrame(
                                eval_report["classification_report"]
                            ).transpose()
                            st.dataframe(report_df, use_container_width=True)

                            # Predictions détaillées
                            st.subheader("🔍 Exemples de Prédictions")
                            pred_df = pd.DataFrame(eval_report["predictions"][:10])
                            st.dataframe(pred_df, use_container_width=True)

                        except Exception as e:
                            st.error(f"❌ Erreur évaluation: {str(e)}")

        except Exception as e:
            st.error(f"❌ Erreur chargement dataset CSV: {str(e)}")

    elif dataset_choice == "parapharmacie_vital_final_v2.json (Produits parapharmacie)":
        try:
            json_path = os.path.join(
                BACKEND_DIR, "data", "parapharmacie_vital_final_v2.json"
            )
            with open(json_path, "r", encoding="utf-8") as f:
                products = json.load(f)

            st.success(f"✅ Dataset chargé: {len(products)} produits")

            # Preview
            st.subheader("👀 Aperçu Produits")
            df_prod = pd.DataFrame(products)
            st.dataframe(
                (
                    df_prod[["name", "gamme"]].head(10)
                    if "name" in df_prod.columns
                    else df_prod.head(10)
                ),
                use_container_width=True,
            )

            # Stats
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Produits", len(products))
            with col2:
                st.info("Test RAG Retrieval: Chercher dans la base de produits")

        except Exception as e:
            st.error(f"❌ Erreur dataset JSON: {str(e)}")
