#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Lire le fichier
with open('frontendstreamlit/pages/5_BO5_reporting.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Trouver la position du Tab 3
tab3_start = content.find('# TAB 3: COMPARAISON A/B')

# Couper à partir du Tab 3
before_tab3 = content[:tab3_start]

# Écrire le nouveau contenu
new_tab3 = """# ========================================
# TAB 3: COMPARAISON A/B Fine-tuning vs Standard
# ========================================

# Initialiser session state pour eviter l'erreur Streamlit
if "comp_text_input" not in st.session_state:
    st.session_state.comp_text_input = ""

with tab3:
    st.subheader("⚖️ Comparaison: Fine-tuning vs Modèle Standard")
    st.write("Testez le même texte avec les deux modèles d'embeddings et comparez les résultats")
    
    # Boutons rapides pour charger les exemples
    st.markdown("### 📝 Exemples Rapides")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📍 Cardiologie", key="comp_btn_cardio"):
            st.session_state.comp_text_input = \"\"\"DÉLÉGUÉ: Bonjour docteur, merci de m'accorder ce moment
MÉDECIN: Bien sûr, que me proposez-vous?
DÉLÉGUÉ: Nous avons lancé un nouveau produit pour la cardiologie
MÉDECIN: Intéressant! Quel est le prix?
DÉLÉGUÉ: 45 euros par boîte, pour un traitement mensuel
MÉDECIN: C'est assez cher, n'avez-vous pas quelque chose de moins onéreux?
DÉLÉGUÉ: Je comprends votre préoccupation. Cependant, les études cliniques montrent 35% d'efficacité supérieure
MÉDECIN: Vous avez les données cliniques?
DÉLÉGUÉ: Absolument, voici les résultats des essais phase 3\"\"\"
            st.rerun()
    
    with col2:
        if st.button("🩺 Dermatologie", key="comp_btn_dermato"):
            st.session_state.comp_text_input = \"\"\"DÉLÉGUÉ: Bonjour Dr Martin, comment allez-vous?
MÉDECIN: Bien, je suis occupé. Dites-moi rapidement.
DÉLÉGUÉ: Nous avons une nouvelle crème pour le traitement de l'acné
MÉDECIN: Une crème de plus... Qu'est-ce qui la rend spéciale?
DÉLÉGUÉ: Notre formule combine acide salicylique et probiotiques naturels
MÉDECIN: Les probiotiques dans une crème? C'est quoi, la preuve scientifique?
DÉLÉGUÉ: Nous avons des résultats d'essais sur 500 patients montrant 78% d'amélioration\"\"\"
            st.rerun()
    
    with col3:
        if st.button("💊 Antibiothérapie", key="comp_btn_antibio"):
            st.session_state.comp_text_input = \"\"\"DÉLÉGUÉ: Docteur, pouvez-vous m'accorder 5 minutes?
MÉDECIN: D'accord, mais soyez rapide.
DÉLÉGUÉ: Nous commercialisons un nouvel antibiotique large spectre
MÉDECIN: Encore un! Nous en avons déjà assez. L'antibioresistance?
DÉLÉGUÉ: C'est justement pour cela. Notre molécule a montré efficacité contre les souches multirésistantes
MÉDECIN: Des souches vraiment multirésistantes? BLSE? Pseudomonas?\"\"\"
            st.rerun()
    
    # Input pour la comparaison (SANS key= pour éviter l'erreur Streamlit)
    st.markdown("### 📝 Texte à Analyser")
    comparison_text = st.text_area(
        "Entrez une conversation directement ou utilisez les exemples rapides ci-dessus:",
        value=st.session_state.comp_text_input,
        height=150
    )
    
    # Bouton de comparaison
    if st.button("🚀 Lancer la Comparaison", use_container_width=True, type="primary"):
        if not comparison_text.strip():
            st.error("❌ Veuillez entrer un texte à analyser")
        else:
            col_finetuned, col_standard = st.columns(2)
            
            with col_finetuned:
                st.subheader("✅ Avec Fine-tuning")
                with st.spinner("⏳ Analyse avec modèle fine-tuné..."):
                    try:
                        result_finetuned = analyze_conversation(comparison_text, "Analyse Objections", top_k=3)
                        st.success("✅ Analyse complétée")
                        
                        # Résultats fine-tuning
                        if result_finetuned.get('objections'):
                            st.write(f"**Objections trouvées:** {len(result_finetuned['objections'])}")
                            for i, obj in enumerate(result_finetuned['objections'][:3], 1):
                                st.write(f"  {i}. **{obj['type']}**: {obj['text'][:100]}")
                        
                        st.metric("Objection principale", result_finetuned.get('predicted_main_objection', 'Aucune'))
                        st.metric("Confiance", f"{result_finetuned.get('predicted_objection_score', 0):.2%}")
                        
                        if result_finetuned.get('strategies'):
                            st.write("**Stratégies recommandées:**")
                            for strategy in result_finetuned['strategies'][:2]:
                                st.write(f"  • {strategy}")
                    
                    except Exception as e:
                        st.error(f"❌ Erreur: {str(e)}")
            
            with col_standard:
                st.subheader("📋 Sans Fine-tuning (Standard)")
                st.info("🚀 Fonctionnalité en cours de développement")
                st.write(\"\"\"Bientôt disponible:
- Comparaison côte à côte des deux modèles
- Mesure de l'impact du fine-tuning
- Amélioration de confiance et pertinence

**Pour l'instant:** Le fine-tuning est automatiquement utilisé en Tab 1 pour meilleurs résultats!\"\"\")
                st.warning("⏳ Revenez bientôt pour tester l'option standard!")
"""

# Écrire le fichier
with open('frontendstreamlit/pages/5_BO5_reporting.py', 'w', encoding='utf-8') as f:
    f.write(before_tab3 + new_tab3)

print('✅ Fichier corrigé!')
