#!/usr/bin/env python3
# ========================================
# TEST BO5 - Script Complet
# ========================================
import sys
import os
from pathlib import Path

# Setup paths
BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR / "ai_backend"))

from rag.query.query_bo5_medical import analyze_conversation, save_rapport, list_saved_rapports

# ========================================
# TEST CONVERSATIONS
# ========================================
test_conversations = {
    "🏥 Cardiologie": """DÉLÉGUÉ: Bonjour docteur, comment allez-vous?
MÉDECIN: Bien, que me proposez-vous?
DÉLÉGUÉ: Un nouveau produit pour la cardiologie avec 35% plus d'efficacité
MÉDECIN: Le prix? Et la sécurité?
DÉLÉGUÉ: 45 euros/boîte. Profil sécurité excellent, études phase 3 terminees
MÉDECIN: Données cliniques disponibles?
DÉLÉGUÉ: Oui, je vous les envoie. Stock disponible immédiatement
MÉDECIN: Et remboursement CNAM?
DÉLÉGUÉ: En évaluation. Documentation fournie bientôt""",
    
    "🩺 Dermatologie": """DÉLÉGUÉ: Dr Martin, une nouvelle crème pour l'acné
MÉDECIN: Encore une? Quelle différence?
DÉLÉGUÉ: Combinaison acide salicylique + probiotiques. 78% d'amélioration
MÉDECIN: Probiotiques dans une crème? Preuves?
DÉLÉGUÉ: 500 patients testés. Hypoallergénique. 28€ par tube
MÉDECIN: Moins cher mais mieux? Comment?
DÉLÉGUÉ: Formule brevetée. Efficacité cliniquement prouvée""",
    
    "💊 Antibiotique": """DÉLÉGUÉ: Nouvel antibiotique large spectre
MÉDECIN: Efficacité contre multirésistants?
DÉLÉGUÉ: Oui, BLSE, Pseudomonas. Essai pédiatrique positif
MÉDECIN: Interactions médicamenteuses?
DÉLÉGUÉ: Très peu. Pénétration tissulaire excellente
MÉDECIN: Donnez-moi les données"""
}

# ========================================
# FONCTION TEST
# ========================================
def test_conversation(nom, dialogue, rapport_type="Analyse Objections"):
    """Test une conversation complète"""
    print("\n" + "="*70)
    print(f"🧪 TEST: {nom}")
    print("="*70)
    
    try:
        result = analyze_conversation(dialogue, rapport_type, top_k=5)
        
        # Afficher résultats
        print(f"\n✅ ANALYSE COMPLÉTÉE")
        print(f"\n📊 STATISTIQUES:")
        for k, v in result.get("key_points", {}).items():
            print(f"   {k}: {v}")
        
        print(f"\n🚫 OBJECTIONS ({len(result.get('objections', []))} trouvées):")
        for i, obj in enumerate(result.get("objections", [])[:3], 1):
            print(f"   {i}. {obj['type']}")
            print(f"      Score: {obj['sources'][0]['score']:.3f}" if obj.get('sources') else "      Score: N/A")
        
        print(f"\n📚 SOURCES (Top {len(result.get('sources', []))}):")
        for i, src in enumerate(result.get("sources", [])[:3], 1):
            print(f"   {i}. Score: {src['score']:.3f}")
        
        # Sauvegarder le rapport
        print(f"\n💾 SAUVEGARDE...")
        filepath = save_rapport(result)
        print(f"   ✅ Sauvegardé: {filepath}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERREUR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

# ========================================
# MAIN
# ========================================
if __name__ == "__main__":
    print("\n")
    print("🚀 TEST BO5 REPORTING - SUITE COMPLÈTE")
    print("="*70)
    
    results = {}
    
    # Tester chaque conversation
    for nom, dialogue in test_conversations.items():
        success = test_conversation(nom, dialogue)
        results[nom] = success
    
    # Résumé final
    print("\n" + "="*70)
    print("📋 RÉSUMÉ DES TESTS")
    print("="*70)
    
    for nom, success in results.items():
        status = "✅" if success else "❌"
        print(f"{status} {nom}")
    
    # Lister rapports sauvegardés
    print("\n📂 RAPPORTS SAUVEGARDÉS:")
    saved = list_saved_rapports()
    if saved:
        for i, rapport in enumerate(saved[:5], 1):
            print(f"   {i}. {rapport['filename']}")
    else:
        print("   ⚠️ Aucun rapport trouvé!")
    
    print("\n✅ TESTS TERMINÉS\n")
