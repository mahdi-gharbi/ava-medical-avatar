with open('frontendstreamlit/pages/5_BO5_reporting.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Trouver la ligne "Sans Fine-tuning"
for i, line in enumerate(lines):
    if 'Sans Fine-tuning (Standard)' in line:
        # Trouver la fin de ce bloc (avant le prochain "if 'finetuned'")
        start_idx = i
        end_idx = start_idx
        for j in range(i+1, len(lines)):
            if "if 'finetuned' in st.session_state" in lines[j]:
                end_idx = j
                break
        
        # Remplacer les lignes
        new_lines = lines[:start_idx] + [
            '                st.subheader("📋 Sans Fine-tuning (Standard)")\n',
            '                with st.spinner("⏳ Analyse avec embeddings STANDARD..."):\n',
            '                    try:\n',
            '                        from ab_comparison import analyze_with_standard_embeddings\n',
            '                        result_standard = analyze_with_standard_embeddings(comparison_text, "Analyse Objections", top_k=3)\n',
            '                        st.success("✅ Analyse complétée")\n',
            '                        if result_standard.get(\'objections\'):\n',
            '                            st.write(f"**Objections trouvées:** {len(result_standard[\'objections\'])}")\n',
            '                            for i, obj in enumerate(result_standard[\'objections\'][:3], 1):\n',
            '                                st.write(f"  {i}. **{obj[\'type\']}**: {obj[\'text\'][:100]}")\n',
            '                        st.metric("Objection principale", result_standard.get(\'predicted_main_objection\', \'Aucune\'))\n',
            '                        st.metric("Confiance", f"{result_standard.get(\'predicted_objection_score\', 0):.2%}")\n',
            '                        if result_standard.get(\'strategies\'):\n',
            '                            st.write("**Stratégies recommandées:**")\n',
            '                            for strategy in result_standard[\'strategies\'][:2]:\n',
            '                                st.write(f"  • {strategy}")\n',
            '                    except Exception as e:\n',
            '                        st.error(f"❌ Erreur embeddings standard: {str(e)}")\n',
        ] + lines[end_idx:]
        
        with open('frontendstreamlit/pages/5_BO5_reporting.py', 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        
        print(f"✅ Tab 3 mise à jour! Lignes {start_idx} à {end_idx} remplacées")
        break
else:
    print("❌ Section non trouvée")
