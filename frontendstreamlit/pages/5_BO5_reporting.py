# ========================================
# BO5 REPORTING avec RAG + GROQ
# ========================================
import streamlit as st

# Pre-load and cache embedding models to prevent reloading on every rerun
try:
    from cached_models import load_finetuned_model, load_standard_model
    _ = load_finetuned_model()
    _ = load_standard_model()
except Exception as e:
    pass  # Models will be loaded on first use

import pandas as pd
import sys
import os
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from fpdf import FPDF
import re
import json

# ========================================
# FIX PATHS
# ========================================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
BACKEND_DIR = os.path.join(BASE_DIR, "ai_backend")

# Ajouter la racine au début du path
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, BACKEND_DIR)

# ========================================
# FONCTION POUR SAUVEGARDER DANS CRM (MONGODB)
# ========================================
import requests

def save_report_to_crm(
    transcript,
    doctor_name,
    delegate_name,
    specialty,
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
    report_date=None
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
            "specialty": specialty,
            "transcript": transcript,
            "objections_detected": objections_detected,
            "main_objection_type": main_objection_type,
            "strategies": strategies,
            "sentiment": float(sentiment) if sentiment else 0,
            "interest": float(interest) if interest else 0,
            "visit_score": float(visit_score) if visit_score else 0,
            "json_data": json_data,
            # 🔥 NOUVEAUX CHAMPS
            "detected_language": detected_language or "FRANÇAIS",
            "medical_specialty": medical_specialty or "Médecine Générale",
            "engagement": engagement or {"obtained": False, "score": 0, "indicators": []},
            "detected_needs": detected_needs or [],
            "client_typology": client_typology or {"primary": "Analysant", "confidence": 0},
            "proposed_product": proposed_product or "Non spécifié",
            "report_date": report_date or datetime.now().isoformat()
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
                "report_id": data.get("report_id")
            }
        else:
            print(f"[DEBUG] Erreur {response.status_code}")
            return {
                "success": False,
                "message": f"❌ Erreur {response.status_code}: {response.text}"
            }
    
    except requests.exceptions.ConnectionError as e:
        print(f"[DEBUG] Erreur de connexion: {str(e)}")
        return {
            "success": False,
            "message": "❌ Erreur: Impossible de se connecter au serveur CRM (Node.js). Assurez-vous que le backend est lancé sur http://localhost:5000"
        }
    except Exception as e:
        print(f"[DEBUG] Erreur générale: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return {
            "success": False,
            "message": f"❌ Erreur lors de la sauvegarde: {str(e)}"
        }

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
        
        # 🔥 NEW: Afficher les informations de base du rapport
        pdf.set_font("Helvetica", "B", 10)
        pdf.write(6, "Informations de la Visite\n")
        pdf.set_font("Helvetica", "", 9)
        
        detected_language = result.get("detected_language", "FR")
        medical_specialty = result.get("medical_specialty", "Médecine Générale")
        proposed_product = result.get("proposed_product", "Non spécifié")
        engagement = result.get("engagement", {})
        detected_needs = result.get("detected_needs", [])
        client_typology = result.get("client_typology", {})
        
        pdf.write(5, f"Langue: {detected_language}\n")
        pdf.write(5, f"Spécialité: {medical_specialty}\n")
        pdf.write(5, f"Produit: {proposed_product[:50]}\n")
        pdf.write(5, f"Engagement: {'OUI' if engagement.get('obtained') else 'NON'}\n")
        if detected_needs:
            pdf.write(5, f"Besoins: {', '.join(detected_needs[:3])}\n")
        if client_typology:
            pdf.write(5, f"Profil Client: {client_typology.get('primary', 'N/A')}\n")
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
        score = int(score_match.group(1)) if score_match else result.get("visit_score", 50)
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
                    # Importer les services RAG
                    from rag.query.query_bo5_medical import analyze_conversation
                    
                    # Analyser la conversation complète
                    result = analyze_conversation(
                        dialogue=query_input,
                        rapport_type=rapport_type,
                        top_k=top_k
                    )
                    
                    # Sauvegarder dans session_state pour persister entre les reruns
                    st.session_state.bo5_result = result
                    st.session_state.bo5_query_input = query_input
                    st.session_state.bo5_rapport_type = rapport_type
                    
                except Exception as e:
                    st.error(f"❌ Erreur lors de l'analyse: {str(e)}")
                    import traceback
                    st.code(traceback.format_exc())
                    st.stop()
        
        # Afficher le rapport (soit généré, soit depuis session_state)
        if "bo5_result" in st.session_state:
            result = st.session_state.bo5_result
            query_input_display = st.session_state.bo5_query_input
            rapport_type_display = st.session_state.bo5_rapport_type
            
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
{query_input_display}"""
                
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
            
            # 🔥 NEW: Afficher les informations générales du rapport
            st.markdown("---")
            # ========================================
            # 🎯 AMÉLIORATIONS - NOUVELLE INTERFACE
            # ========================================
            st.markdown("---")
            st.markdown("# 📊 Résumé des 8 Améliorations")
            
            # ========================================
            # Section 1: INFOS FONDAMENTALES (3 colonnes)
            # ========================================
            st.markdown("### 🎯 Contexte de la Visite")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                language = result.get("detected_language", "FRANÇAIS")
                st.metric(
                    "🌐 Langue Détectée",
                    language,
                    help="Langue détectée automatiquement dans la conversation"
                )
            
            with col2:
                specialty = result.get("medical_specialty", "Médecine Générale")
                st.metric(
                    "👨‍⚕️ Spécialité Médicale",
                    specialty,
                    help="Domaine médical identifié par IA"
                )
            
            with col3:
                visit_score = result.get("visit_score", 0)
                visit_score = min(100, max(0, visit_score))
                st.metric(
                    "⭐ Score de Visite",
                    f"{visit_score:.0f}/100",
                    help="Score global basé sur sentiment, engagement, objections"
                )
            
            # ========================================
            # Section 2: ENGAGEMENT (Détaillé)
            # ========================================
            st.markdown("---")
            st.markdown("### 💼 Engagement Client")
            
            engagement = result.get("engagement", {})
            engagement_obtained = engagement.get("obtained", False)
            engagement_score = engagement.get("score", 0)
            engagement_indicators = engagement.get("indicators", [])
            
            col1, col2 = st.columns([1.5, 2])
            
            with col1:
                # Statut d'engagement
                if engagement_obtained:
                    st.success("✅ **ENGAGEMENT OBTENU**", icon="✅")
                else:
                    st.warning("❌ **ENGAGEMENT À CONFIRMER**", icon="⚠️")
                
                # Barre de score
                st.progress(
                    value=min(1.0, engagement_score),
                    text=f"Score: {engagement_score:.0%}"
                )
            
            with col2:
                # Indicateurs explicites
                st.markdown("**Indicateurs Détectés:**")
                if engagement_indicators:
                    for indicator in engagement_indicators[:5]:
                        # Nettoyer les indicateurs
                        indicator_clean = indicator.replace("✅", "").replace("❌", "").strip()
                        if "✅" in indicator or "oui" in indicator.lower() or "accord" in indicator.lower():
                            st.markdown(f"✅ {indicator_clean}")
                        else:
                            st.markdown(f"❌ {indicator_clean}")
                else:
                    st.markdown("*Aucun indicateur détecté*")
            
            # ========================================
            # Section 3: BESOINS DÉTECTÉS
            # ========================================
            st.markdown("---")
            st.markdown("### 🏥 Besoins Détectés")
            
            detected_needs = result.get("detected_needs", [])
            if detected_needs:
                # Afficher comme badges colorés
                cols = st.columns(min(4, len(detected_needs)))
                for idx, need in enumerate(detected_needs[:4]):
                    with cols[idx % len(cols)]:
                        st.markdown(f"""
                        <div style='background-color: #E8F4F8; padding: 10px; border-radius: 5px; text-align: center; border-left: 4px solid #0088CC;'>
                        <b>{need}</b>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Afficher les besoins supplémentaires
                if len(detected_needs) > 4:
                    st.markdown(f"**Et {len(detected_needs) - 4} autre(s) besoin(s):** {', '.join(detected_needs[4:])}")
            else:
                st.info("Aucun besoin spécifique détecté dans cette visite")
            
            # ========================================
            # Section 4: PROFIL CLIENT (4 Typologies)
            # ========================================
            st.markdown("---")
            st.markdown("### 👤 Profil du Client")
            
            client_typology = result.get("client_typology", {})
            if client_typology:
                primary_type = client_typology.get("primary", "Analysant")
                confidence = client_typology.get("confidence", 0)
                all_types = client_typology.get("all_types", {})
                
                col1, col2 = st.columns([1.5, 1.5])
                
                with col1:
                    st.markdown(f"**Profil Principal:** {primary_type}")
                    st.progress(
                        value=min(1.0, confidence),
                        text=f"Confiance: {confidence:.0%}"
                    )
                    
                    # Description du profil
                    profile_descriptions = {
                        "Promouvant": "🎖️ Valorise l'excellence et la différenciation",
                        "Facilitant": "🤝 Cherche la sécurité et le confort",
                        "Contrôlant": "🔬 Teste et vérifie les solutions",
                        "Analysant": "📚 Demande études et preuves scientifiques"
                    }
                    
                    if primary_type in profile_descriptions:
                        st.markdown(f"*{profile_descriptions[primary_type]}*")
                
                with col2:
                    st.markdown("**Profils Détectés:**")
                    if all_types:
                        # Créer un graphique radar ou barres
                        for type_name, score in all_types.items():
                            st.markdown(f"• {type_name}: {score:.0%}")
            
            # ========================================
            # Section 5: PRODUIT PROPOSÉ
            # ========================================
            st.markdown("---")
            st.markdown("### 💊 Produit Proposé")
            
            proposed_product = result.get("proposed_product", "Non spécifié")
            
            # Vérifier si c'est juste un visit_id
            if "visit_id" in proposed_product.lower() or proposed_product == "Non spécifié":
                st.warning("⚠️ Produit non identifié dans cette conversation")
            else:
                st.success(f"✅ **{proposed_product}**", icon="💊")
                st.markdown(f"*Produit détecté automatiquement dans la conversation*")
            
            # ========================================
            # Section 6: RÉSUMÉ GÉNÉRAL
            # ========================================
            st.markdown("---")
            st.markdown("### 📋 Résumé de la Visite")
            
            summary_col1, summary_col2, summary_col3 = st.columns(3)
            
            with summary_col1:
                st.markdown("""
                <div style='background-color: #FFF3CD; padding: 15px; border-radius: 5px; border-left: 4px solid #FF9800;'>
                <b>💬 Langage</b><br>
                """ + language + """
                </div>
                """, unsafe_allow_html=True)
            
            with summary_col2:
                st.markdown(f"""
                <div style='background-color: #E3F2FD; padding: 15px; border-radius: 5px; border-left: 4px solid #2196F3;'>
                <b>🎯 Engagement</b><br>
                {'OUI ✅' if engagement_obtained else 'À confirmer ⚠️'} ({engagement_score:.0%})
                </div>
                """, unsafe_allow_html=True)
            
            with summary_col3:
                st.markdown(f"""
                <div style='background-color: #F3E5F5; padding: 15px; border-radius: 5px; border-left: 4px solid #9C27B0;'>
                <b>⭐ Performance</b><br>
                {visit_score:.0f}/100 {'🌟' if visit_score >= 80 else '✓' if visit_score >= 60 else '⚠️'}
                </div>
                """, unsafe_allow_html=True)
            
            # ========================================
            # ANALYSE SIGNIFICATIVE DE LA VISITE
            # ========================================
            st.markdown("---")
            with st.expander("🎯 Analyse Détaillée de la Visite", expanded=False):
                # Générer des insights significatifs
                visite_score = None
                try:
                    from services.rag_service import generate_response
                    import re
                    
                    insights_prompt = f"""Analyse cette visite médicale et donne une évaluation STRUCTURÉE avec:
1. **Points Forts** (2-3 bullets): Qu'est-ce qui a bien marché?
2. **Points d'Amélioration** (2-3 bullets): Qu'est-ce qui aurait pu mieux se passer?
3. **Recommandations** (2-3 bullets): Que faire pour la prochaine visite?
4. **Stratégies** (si applicable): Stratégies proposées pour cette catégorie de client?

Conversation:
{query_input_display}"""
                    
                    insights = generate_response(
                        query=insights_prompt,
                        context_docs=[],
                        system_prompt="Tu es un expert en ventes médicales. Fournis une analyse constructive et actionnable. Sois concis et pratique."
                    )
                    
                    st.markdown(insights)
                    
                except Exception as e:
                    st.warning(f"⚠️ Impossible de générer l'analyse détaillée: {str(e)}")
            
            # Analyse détaillée en expander
            with st.expander("📝 Analyse Complète IA", expanded=False):
                st.write(st.session_state.bo5_result["analysis"])
            
            # Points clés en expander avec tableau
            with st.expander("🎯 Points Clés & Statistiques", expanded=False):
                if st.session_state.bo5_result.get("key_points"):
                    key_points_data = pd.DataFrame([
                        {"Métrique": key, "Valeur": value}
                        for key, value in st.session_state.bo5_result.get("key_points", {}).items()
                    ])
                    st.dataframe(key_points_data, use_container_width=True)
                else:
                    for key, value in st.session_state.bo5_result.get("key_points", {}).items():
                        st.write(f"**{key}:** {value}")
            
            # Objections détectées avec analyse
            if st.session_state.bo5_result.get("objections"):
                with st.expander(f"🚫 Objections Détectées ({num_objections})", expanded=False):
                    # Tableau des objections avec stratégies mieux visibles
                    objections_data = pd.DataFrame([
                        {
                            "Objection": obj['type'],
                            "Énoncé": obj['text'][:50] + "..." if len(obj['text']) > 50 else obj['text'],
                        }
                        for obj in st.session_state.bo5_result["objections"]
                    ])
                    st.dataframe(objections_data, use_container_width=True)
                    
                    # Stratégies pour chaque objection
                    st.markdown("**✅ Stratégies de Réponse:**")
                    for i, obj in enumerate(st.session_state.bo5_result["objections"], 1):
                        col1, col2 = st.columns([1, 3])
                        with col1:
                            st.write(f"**{obj['type']}:**")
                        with col2:
                            st.write(obj['strategy'])
            
            # Sources avec contexte
            with st.expander(f"📚 Sources Utilisées ({num_sources})", expanded=False):
                if num_sources > 0:
                    st.info(f"Score moyen de pertinence: **{avg_score:.2f}** (plus proche de 1 = plus pertinent)")
                    for i, source in enumerate(st.session_state.bo5_result["sources"], 1):
                        col1, col2 = st.columns([1, 4])
                        with col1:
                            st.metric("Score", f"{source['score']:.2f}")
                        with col2:
                            st.write(source["content"][:300] + "...")
            
            # Export
            st.markdown("---")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                try:
                    pdf_bytes = generate_pdf_report(st.session_state.bo5_result, st.session_state.bo5_rapport_type)
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
                        data=str(st.session_state.bo5_result),
                        file_name=f"rapport_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
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
                            objections_list = [obj['type'] for obj in st.session_state.bo5_result.get("objections", [])]
                            strategies_dict = {
                                obj['type']: obj['strategy'] 
                                for obj in st.session_state.bo5_result.get("objections", [])
                            }
                            
                            # Sentiments et intérêt (à extraire ou par défaut)
                            sentiment_val = st.session_state.bo5_result.get("predicted_sentiment", 0)
                            interest_val = st.session_state.bo5_result.get("predicted_interest", 70)
                            visit_score_val = st.session_state.bo5_result.get("visit_score", visite_score if visite_score else 70)
                            
                            print(f"[STREAMLIT DEBUG] Données préparées: visit_score={visit_score_val}")
                            
                            # 🔥 NOUVELLES DONNÉES
                            detected_language = st.session_state.bo5_result.get("detected_language", "FRANÇAIS")
                            medical_specialty = st.session_state.bo5_result.get("medical_specialty", "Médecine Générale")
                            engagement_data = st.session_state.bo5_result.get("engagement", {"obtained": False, "score": 0})
                            detected_needs = st.session_state.bo5_result.get("detected_needs", [])
                            client_typology = st.session_state.bo5_result.get("client_typology", {})
                            proposed_product = st.session_state.bo5_result.get("proposed_product", "Non spécifié")
                            report_date = st.session_state.bo5_result.get("report_date", datetime.now().isoformat())
                            
                            # Appeler la fonction de sauvegarde
                            crm_result = save_report_to_crm(
                                transcript=st.session_state.bo5_query_input[:2000],  # Limiter la taille
                                doctor_name="Docteur Cardiologue",  # À adapter si data disponible
                                delegate_name="Délégué Médical",
                                specialty=st.session_state.bo5_rapport_type if st.session_state.bo5_rapport_type else "Général",
                                objections_detected=objections_list,
                                main_objection_type=objections_list[0] if objections_list else None,
                                strategies=strategies_dict,
                                sentiment=sentiment_val,
                                interest=interest_val,
                                visit_score=visit_score_val,
                                json_data={
                                    "analysis": st.session_state.bo5_result.get("analysis", "")[:1000],
                                    "objections_count": len(objections_list),
                                    "sources_count": len(st.session_state.bo5_result.get("sources", []))
                                },
                                # 🔥 NOUVEAUX PARAMÈTRES
                                detected_language=detected_language,
                                medical_specialty=medical_specialty,
                                engagement=engagement_data,
                                detected_needs=detected_needs,
                                client_typology=client_typology,
                                proposed_product=proposed_product,
                                report_date=report_date
                            )
                            
                            print(f"[STREAMLIT DEBUG] Résultat: {crm_result}")
                            
                            # Afficher le résultat IMMÉDIATEMENT
                            if crm_result["success"]:
                                st.success(crm_result["message"])
                                st.info(f"📍 **Visit ID:** {crm_result['visit_id']}\n📋 **Report ID:** {crm_result['report_id']}")
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
            
            # ========================================
            # SECTION FINE-TUNING
            # ========================================
            st.markdown("---")
            st.markdown("### 🔧 Fine-tuning du SentenceTransformer")
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write("Améliorez le modèle d'embeddings en le fine-tunant sur vos données médicales")
            with col2:
                finetune_epochs = st.number_input("Epochs", min_value=1, max_value=5, value=2)
            
            if st.button("🚀 Lancer Fine-tuning Complet", use_container_width=True):
                with st.spinner("⏳ Fine-tuning en cours (peut prendre 2-5 min)..."):
                    try:
                        from rag.query.query_bo5_medical import full_finetuning_pipeline
                        
                        result = full_finetuning_pipeline(epochs=int(finetune_epochs))
                        
                        st.success("✅ Fine-tuning Terminé avec Succès !")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Train Accuracy", f"{result['train_accuracy']:.1%}")
                        with col2:
                            st.metric("Validation Accuracy", f"{result['validation_accuracy']:.1%}")
                        
                        st.info(f"💡 Le modèle fine-tuné est sauvegardé et sera utilisé pour les prochaines analyses.")
                        
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

