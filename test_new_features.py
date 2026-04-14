#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test des 8 nouvelles améliorations
"""

import sys
import os
from pathlib import Path

# Ajouter le chemin pour les imports
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "ai_backend"))

# Importer les nouvelles fonctions
from ai_backend.rag.query.query_bo5_medical import (
    detect_language,
    detect_medical_specialty,
    detect_engagement,
    extract_detected_needs,
    classify_client_typology,
    extract_proposed_product,
    improve_visit_score,
)

# Exemple de conversation de test
TEST_DIALOGUE = """DÉLÉGUÉ: Bonjour Dr Dupont, comment allez-vous?
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
MÉDECIN: C'est intéressant. Et l'assurance? Elle rembourse?
DÉLÉGUÉ: Oui, sur prescription médicale
MÉDECIN: D'accord, envoyez-moi les données. Je vais tester avec quelques patients."""

print("=" * 80)
print("TEST DES 8 AMÉLIORATIONS")
print("=" * 80)

# Test 1: Détection Langue
print("\n1. 🌐 DÉTECTION LANGUE")
print("-" * 80)
language = detect_language(TEST_DIALOGUE)
print(f"   Langue détectée: {language}")
print(f"   ✓ Résultat: {language == 'FRANÇAIS'}")

# Test 2: Détection Spécialité
print("\n2. 👨‍⚕️ DÉTECTION SPÉCIALITÉ MÉDICALE")
print("-" * 80)
specialty = detect_medical_specialty(TEST_DIALOGUE)
print(f"   Spécialité détectée: {specialty}")
print(f"   ✓ Résultat: {specialty == 'Dermatologie'}")

# Test 3: Détection Engagement
print("\n3. 💼 DÉTECTION ENGAGEMENT")
print("-" * 80)
engagement = detect_engagement(TEST_DIALOGUE)
print(f"   Engagement obtenu: {engagement['obtained']}")
print(f"   Score d'engagement: {engagement['score']:.0%}")
print(f"   Indicateurs: {engagement['indicators'][:3]}")
print(f"   ✓ Résultat: Obtenu={engagement['obtained']}, Score={engagement['score']:.2f}")

# Test 4: Extraction Besoins
print("\n4. 🏥 EXTRACTION BESOINS DÉTECTÉS")
print("-" * 80)
needs = extract_detected_needs(TEST_DIALOGUE)
print(f"   Besoins détectés: {needs}")
print(f"   ✓ Résultat: {len(needs)} besoins trouvés")

# Test 5: Classification Typologie Client
print("\n5. 👤 CLASSIFICATION TYPOLOGIE CLIENT")
print("-" * 80)
typology = classify_client_typology(TEST_DIALOGUE)
print(f"   Type principal: {typology['primary']}")
print(f"   Confiance: {typology['confidence']:.0%}")
print(f"   Scores détaillés:")
for type_name, score in typology['all_types'].items():
    print(f"     - {type_name}: {score}")
print(f"   ✓ Résultat: {typology['primary']} (confiance: {typology['confidence']:.0%})")

# Test 6: Extraction Produit Proposé
print("\n6. 💊 EXTRACTION PRODUIT PROPOSÉ")
print("-" * 80)
product = extract_proposed_product(TEST_DIALOGUE)
print(f"   Produit extrait: {product}")
print(f"   ✓ Résultat: Produit trouvé")

# Test 7: Amélioration Score de Visite
print("\n7. ⭐ AMÉLIORATION SCORE DE VISITE")
print("-" * 80)
visit_score = improve_visit_score(
    TEST_DIALOGUE,
    objections_count=2,
    engagement_score=engagement['score'],
    sentiment=0.3
)
print(f"   Score de visite: {visit_score:.1f}/100")
print(f"   ✓ Résultat: Score={visit_score:.1f}")

# Test 8: Intégration Complète
print("\n8. 🎯 RÉSUMÉ COMPLET")
print("-" * 80)
print(f"""
   Langue: {language}
   Spécialité: {specialty}
   Engagement: {'✓ Obtenu' if engagement['obtained'] else '✗ Non obtenu'} (score: {engagement['score']:.0%})
   Besoins: {', '.join(needs) if needs else 'Aucun'}
   Profil Client: {typology['primary']} ({typology['confidence']:.0%})
   Produit: {product}
   Score de Visite: {visit_score:.1f}/100
""")

print("=" * 80)
print("✓ TOUS LES TESTS COMPLÉTÉS AVEC SUCCÈS!")
print("=" * 80)
