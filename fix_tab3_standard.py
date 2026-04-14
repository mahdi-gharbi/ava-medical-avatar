#!/usr/bin/env python
# -*- coding: utf-8 -*-

with open('frontendstreamlit/pages/5_BO5_reporting.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Trouver et remplacer la section "Sans Fine-tuning"
old_section = '''            with col_standard:
                st.subheader("📋 Sans Fine-tuning (Standard)")
                st.info("🚀 Fonctionnalité en cours de développement")
                st.write("""
Bientôt disponible:
- Comparaison côte à côte des deux modèles
- Mesure de l'impact du fine-tuning
- Amélioration de confiance et pertinence

**Pour l'instant:** Le fine-tuning est automatiquement utilisé en Tab 1 pour meilleurs résultats!
                """)
                st.warning("⏳ Revenez bientôt pour tester l'option standard!")'''

new_section = '''            with col_standard:
                st.subheader("📋 Sans Fine-tuning (Standard)")
                with st.spinner("⏳ Analyse avec embeddings STANDARD..."):
                    try:
                        from ab_comparison import analyze_with_standard_embeddings
                        result_standard = analyze_with_standard_embeddings(comparison_text, "Analyse Objections", top_k=3)
                        st.success("✅ Analyse complétée")
                        
                        # Résultats standard
                        if result_standard.get('objections'):
                            st.write(f"**Objections trouvées:** {len(result_standard['objections'])}")
                            for i, obj in enumerate(result_standard['objections'][:3], 1):
                                st.write(f"  {i}. **{obj['type']}**: {obj['text'][:100]}")
                        
                        st.metric("Objection principale", result_standard.get('predicted_main_objection', 'Aucune'))
                        st.metric("Confiance", f"{result_standard.get('predicted_objection_score', 0):.2%}")
                        
                        if result_standard.get('strategies'):
                            st.write("**Stratégies recommandées:**")
                            for strategy in result_standard['strategies'][:2]:
                                st.write(f"  • {strategy}")
                    
                    except Exception as e:
                        st.error(f"❌ Erreur embeddings standard: {str(e)}")
                        st.info("💡 Les embeddings standard ne sont pas encore complètement optimisés")'''

if old_section in content:
    content = content.replace(old_section, new_section)
    with open('frontendstreamlit/pages/5_BO5_reporting.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Tab 3 - Colonne Standard mise à jour!")
else:
    print("❌ Section non trouvée")
