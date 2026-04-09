# 📄 BO5 REPORTING - Guide Complet

## 🎯 Overview

**BO5** = Module d'analyse intelligente des visites médicales utilisant RAG (Retrieval Augmented Generation) + Groq LLM (Llama 3.3 70B).

### Cas d'Usage
- Analyser des conversations délégué-médecin
- Détecter les objections
- Générer des stratégies personnalisées
- Sauvegarder et exporter les rapports

---

## 🚀 Démarrage Rapide

### Option 1 : Interface Streamlit (Facile)

```bash
cd "C:\Users\Lenovo\Desktop\AVA"
streamlit run frontendstreamlit/app.py
```

Puis:
1. Cliquez "BO5 reporting" dans le sidebar
2. Sélectionnez une conversation d'exemple
3. Ajustez "Nombre de sources" (5-10)
4. Cliquez "🚀 Générer Rapport avec IA"

### Option 2 : Test en Terminal (Avancé)

```bash
cd "C:\Users\Lenovo\Desktop\AVA"
python test_bo5_complete.py
```

Cela teste 3 conversations différentes et sauvegarde les rapports.

---

## 📊 Améliorations des Scores (> 0.7)

### Avant
```
Score: 0.218 ❌
Raison: Requête simple, peu de contexte
```

### Après (Votre Version)
```
Score: 0.4-0.5 ✅
Raison: Enrichissement automatique + Top-K
```

### Stratégies pour Améliorer Davantage > 0.7

**1. Ajouter Plus de Contexte Spécifique**
```
Actuellement: 298 documents génériques

À ajouter:
- Données produits détaillées par catégorie
- Pricing stratégies
- Cas réels de clients
- Objections fréquentes avec solutions
```

**2. Tuner les Requêtes Enrichies**

Dans `rag_service.py`, modifier:
```python
enriched_queries = [
    query,  # Original
    f"{query} votre_mot_clé_specifique",
    f"{query} contexte_medical",
    f"{query} solution_commerciale",
]
```

**3. Augmenter top_k**

Interface Streamlit → Augmenter "Nombre de sources" de 5 à 10

---

## 🎨 Personnaliser les Rapports

### Modifier les Types de Rapports

Dans le sidebar Streamlit, choisir parmi:
- ✅ Analyse Objections (défaut)
- ⬜ Synthèse Produits
- ⬜ Recommandations
- ⬜ Statistiques

### Ajouter Nouveaux Types

Modifier `query_bo5_medical.py`:

```python
def analyze_conversation(..., rapport_type="Analyse Objections"):
    
    # Ajouter un nouveau type?
    if rapport_type == "Mon Rapport Custom":
        analysis_query = f"""Analysez spécifiquement:
        1. Mes critères
        2. Mes métriques
        3. Mon format
        """
```

### Changer les Stratégies Personnalisées

Dans `query_bo5_medical.py`:

```python
strategies_prompts = {
    "Ma Objection Custom": """Ton prompt personnalisé ici...
    Définis exactement ce que tu veux faire""",
}
```

---

## 💾 Gestion des Rapports

### Où sont Sauvegardés?
```
C:\Users\Lenovo\Desktop\AVA\rapports_archives\
└─ rapport_20260405_120530.json
└─ rapport_20260405_121045.json
└─ ...
```

### Contenus d'un Rapport Sauvegardé
```json
{
  "timestamp": "20260405_120530",
  "type": "Analyse Objections",
  "analysis": "Rapport généré par LLM...",
  "key_points": {...},
  "objections": [
    {
      "type": "Price Objection",
      "text": "C'est assez cher...",
      "strategy": "Stratégie personnalisée...",
      "sources_count": 3
    }
  ],
  "sources_count": 5
}
```

### Exporter les Rapports
```
3 formats:
1. 📄 JSON (native)
2. 📊 Excel (feature future)
3. 📥 PDF (feature future)
```

---

## 💬 Tester Différentes Conversations

### Conversations d'Exemple Intégrées

```
1. 📍 Cardiologie (défaut)
   - Produit nouveau pour coeur
   - Objections: prix, sécurité, CNAM

2. 🩺 Dermatologie
   - Crème acné innovante
   - Objections: efficacité, prix

3. 💊 Antibiothérapie
   - Antibiotique large spectre
   - Objections: résistance, effets secondaires

4. 📈 Cas Simple
   - Engagement basique
   - Bon pour débuter
```

### Format de Conversation

**Requis:**
```
DÉLÉGUÉ: Message
MÉDECIN: Réponse
DÉLÉGUÉ: Suivi
MÉDECIN: Objection
...
```

**Conseils:**
- Minimum 5-6 échanges
- Incluez les objections réelles
- Variez les sujets (prix, sécurité, disponibilité, CNAM)

---

## 🔧 Configuration Avancée

### Ajuster top_k (Nombre de Sources)

**Faible (1-3)**
```
+ Réponses rapides
+ Contexte focalisé
- Moins d'informations
```

**Moyen (5)**
```
+ Bon équilibre (défaut)
+ Réponses précises
+ Performance OK
```

**Élevé (8-10)**
```
+ Maximum contexte
+ Réponses très détaillées
- Temps plus long
- Parfois trop verbeux
```

### Modifier le Seuil de Score

Dans `query_bo5_medical.py`:

```python
# Actuellement
context = [c for c in context if c["score"] > 0.3]

# Plus strict = résultats meilleurs
context = [c for c in context if c["score"] > 0.5]

# Plus tolérant = plus de contexte
context = [c for c in context if c["score"] > 0.2]
```

---

## 🐛 Troubleshooting

### Rapports Sauvegardés Vides

```
Problème: rapports_archives existe mais est vide

Solutions:
1. Vérifier permissions dossier
2. Relancer Streamlit (Ctrl+C puis restart)
3. Vérifier chemin dans query_bo5_medical.py
   RAPPORTS_DIR = PROJECT_ROOT / "rapports_archives"
```

### Scores Bas (< 0.3)

```
Problème: Données Chroma peu pertinentes

Solutions:
1. Uploader plus de données via "upload data"
2. Utiliser les exemples fournis
3. Augmenter top_k
4. Modifier enriched_queries dans rag_service.py
```

### Objections Doublons

```
Problème: Même objection détectée plusieurs fois

Solutions:
1. Relancer Streamlit (cache)
2. Vérifier detect_objections() filtre doublons
3. Augmenter seuil de score
```

---

## 📈 Performance

| Métrique | Valeur |
|----------|--------|
| Temps génération | 5-15s (selon Groq) |
| Mémoire utilisée | ~500MB |
| Documents indexés | 298 |
| Score average | 0.4-0.5 |
| Objections détectées | 3-5 |

### Optimisations Futures

```
[ ] Caching des résultats
[ ] Batch processing
[ ] Streaming responses
[ ] Multi-language support
[ ] Custom model fine-tuning
```

---

## 👥 Use Cases Réels

### Cas 1: Formation Vendeurs
```
Utilisation: Analyser leurs conversations réelles
Résultat: Feedback sur gestion objections, points forts/faibles
```

### Cas 2: QA Manager
```
Utilisation: Vérifier qualité appels clients
Résultat: Rapport automatisé des performances
```

### Cas 3: Product Manager
```
Utilisation: Identifier objections les plus fréquentes
Résultat: Data-driven product improvements
```

### Cas 4: Analyse Concurrence
```
Utilisation: Simuler conversations avec prod concurrents
Résultat: Stratégies de positionnement
```

---

## 📝 Notes de Version

**v1.0 (Actuelle)**
- ✅ RAG complet avec Groq LLM
- ✅ Détection objections
- ✅ 4 conversations d'exemple
- ✅ Sauvegarde JSON
- ✅ Score > 0.4

**v1.1 (Roadmap)**
- 🔲 Export PDF
- 🔲 Dashboard analytics
- 🔲 Custom training data
- 🔲 Multi-language

---

## 🤝 Support

**Questions/Bugs?**
```
1. Vérifier Troubleshooting section
2. Relancer Streamlit
3. Tester avec test_bo5_complete.py
4. Vérifier logs terminal
```

---

**Bon reporting! 🚀**
