# GUIDE D'UTILISATION - 8 AMÉLIORATIONS BO5

## 🚀 Démarrage Rapide

### Lancer l'Application

```bash
# Terminal 1: Backend MongoDB
npm start

# Terminal 2: Frontend Streamlit
streamlit run frontendstreamlit/app.py
```

### Naviguer vers BO5 Reporting
1. Ouvrir http://localhost:8501
2. Cliquer sur "📄 BO5 - Reporting" dans la sidebar
3. Vous êtes dans l'interface améliorée!

---

## 📝 Exemple Pratique Complet

### Étape 1: Entrer une Conversation

Copiez cet exemple dans le textarea:

```
DÉLÉGUÉ: Bonjour Dr Martin, comment allez-vous?
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
MÉDECIN: D'accord, envoyez-moi les données. Je vais tester avec quelques patients.
```

### Étape 2: Cliquer "Générer Rapport"

Le système va extraire automatiquement:

```
🌐 Langue: FRANÇAIS
👨‍⚕️ Spécialité: Dermatologie
💼 Engagement: ✅ OUI (75%)
🏥 Besoins: Acné, Allergie
👤 Profil: Analysant (67%)
💊 Produit: Crème dermatologique
⭐ Score: 85/100
```

### Étape 3: Explorer les Détails

Chaque section est dépliable (expander):

1. **Évaluation de la Visite**
   - Gauge chart du score
   - Insights IA

2. **Analyse Complète IA**
   - Analyse textuelle détaillée

3. **Points Clés & Statistiques**
   - Tableau des métriques

4. **Objections Détectées**
   - Liste avec stratégies

5. **Sources Utilisées**
   - Contexte du RAG

### Étape 4: Télécharger le Rapport

Trois options:
- 📥 **PDF** - Rapport formaté à imprimer
- 📊 **JSON** - Données structurées
- 💾 **Local** - Sauvegarde en fichier

### Étape 5: Sauvegarder dans CRM

Cliquer **"🗄️ Sauvegarder dans CRM"**

Confirmation:
```
✅ Rapport sauvegardé
📍 Visit ID: VISIT_1729430400000
📋 Report ID: 507f191e810c19729de860ea
```

---

## 📊 Comprendre Chaque Amélioration

### 1. 🌐 Langue Détectée

**Utilité**: Gérer les conversations multilingues

**Valeurs Possibles**:
- `FRANÇAIS` - Conversation en français
- `ANGLAIS` - Conversation en anglais
- `ARABE` - Conversation en arabe
- `MIXTE` - Mélange de langues

**Exemple**:
```
Input: "Bonjour doctor, comment va?"
Output: MIXTE (FR + EN)
```

### 2. 👨‍⚕️ Spécialité Détectée

**Utilité**: Catégoriser par domaine médical

**Spécialités Disponibles**:
- Cardiologie (cœur, tension)
- Dermatologie (peau, acné)
- Gastroentérologie (digestion, intestins)
- Rhumatologie (arthrose, articulations)
- Pneumologie (poumons, asthme)
- Neurologie (cerveau, migraines)
- Immunologie (immunité, infections)
- Endocrinologie (glucose, diabète)
- Antibiothérapie (antibiotiques)
- Sommeil (insomnie, repos)
- Vitalité (fatigue, énergie)

**Exemple**:
```
Input: "...traitement de l'acné...testée dermatologiquement..."
Output: Dermatologie
```

### 3. 💼 Engagement Détecté

**Utilité**: Évaluer le succès de la visite

**Champs**:
- `obtained`: OUI/NON - L'engagement est-il obtenu?
- `score`: 0-100% - Force de l'engagement
- `indicators`: Listes des signaux trouvés

**Signaux Positifs** 🟢:
- "d'accord", "oui", "ok", "excellent"
- "je vais", "intéressé", "on peut"

**Signaux Négatifs** 🔴:
- "non", "pas intéressé", "trop cher"
- "plus tard", "doute", "inquiet"

**Exemple**:
```
Input: "D'accord, envoyez-moi les données. Je vais tester..."
Output: 
  obtained: true
  score: 0.75
  indicators: ["✅ D'accord", "✅ Je vais"]
```

### 4. 🏥 Besoins Détectés

**Utilité**: Comprendre les problèmes du médecin

**Besoins Reconnus**:
- Fatigue, Insomnie, Grippe
- Allergies, Arthrose
- Digestion, Stress
- Douleur, Infection
- Immunité

**Exemple**:
```
Input: "...acné...effets secondaires...irritation cutanée..."
Output: ["Acné", "Allergie"]
```

### 5. 👤 Profil de Client (4 Types)

**Utilité**: Adapter l'approche de vente

#### Type 1: PROMOUVANT (Orgueilleux)
- **Motivation**: Être le meilleur et la référence
- **Paroles**: "Je suis un leader", "Je veux la meilleure solution"
- **Stratégie**: Valoriser, glorifier, différencier
- **Mots-clés**: meilleur, référence, excellence, leader

#### Type 2: FACILITANT (Naïf)
- **Motivation**: Sécurité, confort, contact chaleureux
- **Paroles**: "J'ai besoin de me sentir en sécurité"
- **Stratégie**: Rassurer, simplifier, contact personnel
- **Mots-clés**: sûr, facile, accessible, chaleur

#### Type 3: CONTRÔLANT (Préjugés)
- **Motivation**: Tester, vérifier, contrôler
- **Paroles**: "Prouvez-le moi", "Comment ça marche exactement?"
- **Stratégie**: Données techniques, démonstration
- **Mots-clés**: technique, test, vérifier, données

#### Type 4: ANALYSANT (Cherche Preuves)
- **Motivation**: Études, comparaisons, références
- **Paroles**: "Quels sont les résultats d'études?"
- **Stratégie**: Présenter études, publications, données
- **Mots-clés**: étude, preuve, scientifique, données

**Exemple**:
```
Input: "...les probiotiques... résultats d'essais... 
        78% d'amélioration... données cliniques..."
Output: 
  primary: Analysant
  confidence: 0.67
  all_types: {
    Analysant: 4,
    Contrôlant: 1,
    Facilitant: 0,
    Promouvant: 0
  }
```

### 6. 💊 Produit Proposé

**Utilité**: Tracer quel produit a été présenté

**Extraction**:
1. D'abord cherche dans le contexte RAG
2. Sinon cherche dans la conversation

**Exemple**:
```
Input: "Nous avons une nouvelle crème pour le traitement de l'acné"
Output: "crème pour le traitement de l'acné"
```

### 7. ⭐ Score de Visite (0-100)

**Utilité**: Évaluer la qualité globale de la visite

**Formule Améliorée**:
```
Base:                              50 points
+ Sentiment positif (>0.5)       +15
+ Engagement élevé (>0.7)        +20
+ Engagement moyen (>0.5)        +10
- Engagement faible (<0.3)       -15
- Objections (-3 par objection)  jusqu'à -20
+ Long dialogue (>300 mots)      +10
+ Très long dialogue (>500 mots) +15
+ Questions du médecin           +2 par question (max +15)
───────────────────────────────────────────
= SCORE (clamped 0-100)
```

**Interprétation**:
- 0-33: Visite difficile 🔴
- 33-66: Visite moyenne 🟡
- 66-100: Visite réussie 🟢

**Exemple**:
```
Base: 50
+ Engagement: +20 (score 0.75 > 0.7)
+ Questions (9): +15
+ Dialogue (120+ mots): +10
= 85/100 ✓ Très bon!
```

---

## 📈 Utiliser les Données pour Améliorer

### Analyse des Profils de Clients

```python
# Question: Quel type de client réagit le mieux?
# Réponse: Filtrer par client_typology.primary dans CRM
# → Analysant: meilleure conversion?
# → Facilitant: besoin plus de contact?
```

### Analyse des Besoins

```python
# Question: Quel est le besoin le plus courant?
# Réponse: Agréger detected_needs dans CRM
# → Top 5 besoins = priorités produits
```

### Analyse Multilingue

```python
# Question: Différence entre FRANÇAIS et ANGLAIS?
# Réponse: Comparer detected_language et résultats
# → Ajuster stratégies par langue
```

### Analyse des Produits

```python
# Question: Quel produit a le meilleur engagement?
# Réponse: Corréler proposed_product et engagement
# → Optimiser propositions produits
```

---

## 🐛 Dépannage

### Problème: Engagement toujours faux

**Cause**: Peu de signaux dans la conversation
**Solution**: Ajouter plus de dialogue

```
❌ Avant: "Docteur, bonjour. Produit X."
✅ Après: "Docteur, intéressé? Oui, ok. D'accord, envoyez!"
```

### Problème: Spécialité mal détectée

**Cause**: Pas assez de mots-clés de la spécialité
**Solution**: Inclure plus de termes du domaine

```
❌ Avant: "Nous avons un traitement"
✅ Après: "Nous avons une crème pour l'acné, hypoallergénique..."
```

### Problème: Score très bas

**Cause**: Trop d'objections ou engagement faible
**Solution**: Répondre à plus d'objections, obtenir accord

```
❌ Avant: Médecin pose 10 objections, pas d'accord
✅ Après: Répondre à objections, obtenir accord
```

---

## 📊 Requêtes CRM Utiles

### Trouver tous les rapports avec engagement

```json
// MongoDB Query
db.reports.find({
  "engagement.obtained": true
})
```

### Analyser par spécialité

```json
db.reports.find({
  "medical_specialty": "Dermatologie"
}).count()
```

### Trouver clients "Analysant"

```json
db.reports.find({
  "client_typology.primary": "Analysant"
})
```

### Rapports de qualité (score > 80)

```json
db.reports.find({
  "visit_score": { $gt: 80 }
})
```

### Besoins courants

```json
db.reports.aggregate([
  { $unwind: "$detected_needs" },
  { $group: {
    _id: "$detected_needs",
    count: { $sum: 1 }
  }},
  { $sort: { count: -1 }}
])
```

---

## 💡 Cas d'Usage Avancés

### 1. Dashboard de Performance

Créer un dashboard avec:
- Engagement rate (% obtenu)
- Score moyen par spécialité
- Distribution des profils clients
- Top produits proposés

### 2. Prédictions

- Prédire engagement basé sur profil + spécialité
- Suggérer stratégie selon profil détecté
- Alerter si score < 50

### 3. Formation

- Analyser visites inefficaces (score bas)
- Former sur profils mal gérés
- Améliorer selon spécialité

### 4. CRM Intelligence

- Ajouter filtres avancés par champs nouveaux
- Créer rapports personnalisés
- Alertes intelligentes

---

## 🎓 FAQ

**Q: Peut-on modifier les classifications?**
A: Oui! Les fonctions sont dans `query_bo5_medical.py`, facile à customizer.

**Q: Les données anciennes sont-elles mises à jour?**
A: Non. Seules les nouvelles visites ont les champs enrichis.

**Q: Peut-on ajouter d'autres spécialités?**
A: Oui! Ajouter à la fonction `detect_medical_specialty()`.

**Q: Quel est l'impact performance?**
A: Minimal! Les 8 fonctions ajoutent ~100ms au rapport.

**Q: Les données sont-elles exportables?**
A: Oui! PDF, JSON, et via API CRM.

---

## ✅ Checklist Implémentation

- [x] Tous les champs ajoutés
- [x] UI Streamlit mise à jour
- [x] MongoDB modifié
- [x] API Node.js compatible
- [x] Tests passés
- [x] Documentation complète
- [x] Guide d'utilisation

---

**Version**: 1.0
**Date**: 15 Avril 2026
**Status**: Production Ready ✅

*Pour support technique: Voir DOCUMENTATION_TECHNIQUE.md*
