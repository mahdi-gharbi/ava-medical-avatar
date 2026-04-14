# DOCUMENTATION TECHNIQUE - 8 AMÉLIORATIONS BO5

## Vue d'Ensemble

```
┌─────────────────────────────────────────────────────────────────┐
│                   PIPELINE D'ANALYSE AMÉLIORÉ                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  1. Conversation Input                                           │
│           ↓                                                       │
│  2. Parse Conversation (existing)                               │
│           ↓                                                       │
│  3. NOUVELLES EXTRACTIONS (8 fonctions parallèles)             │
│     ├─ detect_language()                                        │
│     ├─ detect_medical_specialty()                               │
│     ├─ detect_engagement()                                      │
│     ├─ extract_detected_needs()                                 │
│     ├─ classify_client_typology()                               │
│     ├─ extract_proposed_product()                               │
│     ├─ improve_visit_score()                                    │
│     └─ [All existing features]                                  │
│           ↓                                                       │
│  4. Combine Results → Rich Report                              │
│           ↓                                                       │
│  5. Export (JSON, PDF, CRM)                                     │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Fichier: `ai_backend/rag/query/query_bo5_medical.py`

### Nouvelles Fonctions Implémentées

#### 1. `detect_language(text: str) -> str`
```python
def detect_language(text: str) -> str:
    """
    Détecte la langue du texte.
    
    Args:
        text: Texte à analyser
        
    Returns:
        "FRANÇAIS" | "ANGLAIS" | "ARABE" | "MIXTE"
        
    Algorithm:
        - Compte occurrences mots-clés français/anglais
        - Détecte caractères arabes (U+0600-U+06FF)
        - Retourne langue dominante
        
    Complexity: O(n) où n = taille du texte
    """
```

**Cas d'Erreur Gérés:**
- Texte vide → "FRANÇAIS" (défaut)
- Mélange plusieurs langues → "MIXTE"
- Caractères arabes > 20 avec autre langue → "MIXTE"

---

#### 2. `detect_medical_specialty(dialogue: str) -> str`
```python
def detect_medical_specialty(dialogue: str) -> str:
    """
    Détecte la spécialité médicale du dialogue.
    
    Args:
        dialogue: Conversation complète
        
    Returns:
        Nom de la spécialité détectée
        
    Specialties (11):
        - Cardiologie: "cardiaque", "cœur", "hypertension"
        - Dermatologie: "peau", "acné", "eczéma"
        - Gastroentérologie: "gastro", "intestin", "digestion"
        - Rhumatologie: "arthrose", "articulation"
        - Pneumologie: "poumon", "respiration", "asthme"
        - Neurologie: "cerveau", "nerf", "migraine"
        - Immunologie: "immunitaire", "infection", "grippe"
        - Endocrinologie: "glucose", "diabète", "thyroïde"
        - Antibiothérapie: "antibiotique", "infection"
        - Sommeil: "sommeil", "insomnie", "mélatonine"
        - Vitalité: "fatigue", "énergie", "CoQ10"
        
    Default: "Médecine Générale"
    """
```

**Algorithmie:**
- Dictionnaire de keywords par spécialité
- Compte matches pour chaque spécialité
- Retourne celle avec score max

---

#### 3. `detect_engagement(dialogue: str) -> dict`
```python
def detect_engagement(dialogue: str) -> dict:
    """
    Détecte si l'engagement est obtenu et son score.
    
    Returns:
        {
            "obtained": bool,           # L'engagement est-il obtenu?
            "score": float,             # 0.0 à 1.0
            "indicators": [str]         # Max 5 indicateurs trouvés
        }
        
    Algorithm:
        score = positive_count / (positive_count + negative_count)
        obtained = score > 0.6
        
    Positive Keywords:
        "d'accord", "oui", "ok", "excellent", "intéressé", 
        "je vais", "on peut", "très bien", "je prends"
        
    Negative Keywords:
        "non", "pas intéressé", "trop cher", "plus tard",
        "pas besoin", "doute", "inquiet", "pas sûr"
    """
```

---

#### 4. `extract_detected_needs(dialogue: str) -> list`
```python
def extract_detected_needs(dialogue: str) -> list:
    """
    Extrait les besoins/symptômes détectés.
    
    Returns:
        ["Fatigue", "Insomnie", "Grippe", ...]
        
    Needs Dictionary (10 catégories):
        - Fatigue: "fatigue", "asthénie", "épuisé"
        - Insomnie: "insomnie", "sommeil", "dormir"
        - Grippe: "grippe", "fièvre", "toux", "rhume"
        - Allergies: "allergie", "allergique", "urticaire"
        - Arthrose: "arthrose", "douleur articulaire"
        - Digestion: "digestion", "intestinal", "reflux"
        - Stress: "stress", "anxieux", "nervosité"
        - Douleur: "douleur", "mal", "souffre"
        - Infection: "infection", "bacterial", "virale"
        - Immunité: "immunitaire", "défense"
    """
```

---

#### 5. `classify_client_typology(dialogue: str) -> dict`
```python
def classify_client_typology(dialogue: str) -> dict:
    """
    Classifie le client en 4 typologies.
    
    Returns:
        {
            "primary": str,           # Type principal
            "confidence": float,      # 0.0 à 1.0
            "all_types": {
                "Promouvant": int,    # Score brut
                "Facilitant": int,
                "Contrôlant": int,
                "Analysant": int
            }
        }
        
    Typologies:
    
    1. PROMOUVANT (Orgueilleux)
       Keywords: "meilleur", "référence", "excellence", "leader"
       Motivation: Être le meilleur et la référence
       
    2. FACILITANT (Naïf)
       Keywords: "sécurité", "confort", "facile", "contact"
       Motivation: Sécurité, confort, contact chaleureux
       
    3. CONTRÔLANT (Préjugés)
       Keywords: "technique", "test", "contrôle", "vérifier"
       Motivation: Teste le vendeur, aspects techniques
       
    4. ANALYSANT (Cherche les preuves)
       Keywords: "étude", "preuve", "scientifique", "données"
       Motivation: Recul sur produit, études scientifiques
    
    Confidence = score_primary / sum(all_scores)
    """
```

---

#### 6. `extract_proposed_product(dialogue: str, context_docs: list) -> str`
```python
def extract_proposed_product(dialogue: str, context_docs: list = None) -> str:
    """
    Extrait le produit proposé.
    
    Priority:
        1. Du contexte RAG (si pertinent)
        2. De la conversation directement
        
    Returns:
        "Crème dermatologique pour acné" ou "Non spécifié"
        
    Keywords:
        "produit", "formule", "crème", "comprimé", "gélule",
        "traitement", "médicament", "complément", "antibiotique"
    """
```

---

#### 7. `improve_visit_score(dialogue: str, objections_count: int, engagement_score: float, sentiment: float) -> float`
```python
def improve_visit_score(dialogue: str, objections_count: int = 0, 
                       engagement_score: float = 0.5, sentiment: float = 0) -> float:
    """
    Calcule un score de visite amélioré (0-100).
    
    Formula:
        score = 50  # Base
        score += 15 if sentiment > 0.5
        score -= 15 if sentiment < -0.5
        score += 20 if engagement > 0.7
        score += 10 if engagement > 0.5
        score -= 15 if engagement < 0.3
        score -= min(objections * 3, 20)  # Max -20
        score += 10 if dialogue_length > 300
        score += 15 if dialogue_length > 500
        score += min(question_count * 2, 15)  # +2 par question, max +15
        return clamp(score, 0, 100)
        
    Factors:
        ✓ Base: 50 (neutre)
        ✓ Sentiment: +/-15
        ✓ Engagement: +10 à +20 ou -15
        ✓ Objections: -3 par objection
        ✓ Longueur dialogue: +10 ou +15
        ✓ Questions posées: +2 par question
    """
```

---

#### 8. Modification: `analyze_conversation()`
```python
def analyze_conversation(dialogue: str, ...) -> dict:
    """
    Pipeline complet (MODIFIÉ).
    
    Changes:
        - Appelle les 8 nouvelles fonctions
        - Ajoute résultats au rapport
        - Ajoute timestamp du rapport
        
    Returns (ancien):
        {
            "type": str,
            "analysis": str,
            "objections": list,
            "sources": list,
            ...
        }
        
    Returns (NOUVEAU - Ajouts):
        {
            # ... ancien ...
            "detected_language": str,
            "medical_specialty": str,
            "engagement": dict,
            "detected_needs": list,
            "client_typology": dict,
            "proposed_product": str,
            "visit_score": float,
            "report_date": str (ISO)
        }
    """
```

---

## Fichier: `backend/models/Report.js`

### Schéma MongoDB - 7 Nouveaux Champs

```javascript
// NOUVEAUX CHAMPS AJOUTÉS
detected_language: {
    type: String,
    // Values: "FRANÇAIS", "ANGLAIS", "ARABE", "MIXTE"
    default: "FRANÇAIS"
},

medical_specialty: {
    type: String,
    // Values: "Cardiologie", "Dermatologie", etc.
    default: "Médecine Générale"
},

detected_needs: {
    type: [String],
    // Examples: ["Fatigue", "Grippe", "Allergie"]
    default: []
},

client_typology: {
    type: {
        primary: String,          // "Analysant" | "Contrôlant" | ...
        confidence: Number,       // 0 à 1
        all_types: {
            Promouvant: Number,
            Facilitant: Number,
            Contrôlant: Number,
            Analysant: Number
        }
    },
    default: null
},

engagement: {
    type: {
        obtained: Boolean,        // true/false
        score: Number,           // 0 à 1
        indicators: [String]     // ["✅ d'accord", "❌ trop cher"]
    },
    default: null
},

proposed_product: {
    type: String,
    // Example: "Crème dermatologique pour acné"
    default: null
},

report_date: {
    type: Date,
    // ISO timestamp
    default: Date.now
}
```

### Index Recommandés
```javascript
// Améliorer performances queries
db.reports.createIndex({ detected_language: 1 });
db.reports.createIndex({ medical_specialty: 1 });
db.reports.createIndex({ "client_typology.primary": 1 });
db.reports.createIndex({ "engagement.obtained": 1 });
```

---

## Fichier: `frontendstreamlit/pages/5_BO5_reporting.py`

### Modifications Fonction `save_report_to_crm()`

```python
# SIGNATURE MODIFIÉE (7 paramètres ajoutés)
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
    detected_language=None,         # String
    medical_specialty=None,         # String
    engagement=None,                # dict
    detected_needs=None,            # list
    client_typology=None,           # dict
    proposed_product=None,          # String
    report_date=None                # String (ISO)
):
    """Envoie les données enrichies à MongoDB via API Node.js"""
    
    payload = {
        # ... existants ...
        # 🔥 NOUVEAUX CHAMPS
        "detected_language": detected_language or "FRANÇAIS",
        "medical_specialty": medical_specialty or "Médecine Générale",
        "engagement": engagement or {"obtained": False, "score": 0},
        "detected_needs": detected_needs or [],
        "client_typology": client_typology or {},
        "proposed_product": proposed_product or "Non spécifié",
        "report_date": report_date or datetime.now().isoformat()
    }
    # ... envoyer à MongoDB ...
```

### Nouvelles Sections UI

#### 1. Métriques Principales (st.metric)
```python
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("🌐 Langue Détectée", result.get("detected_language"))
with col2:
    st.metric("👨‍⚕️ Spécialité", result.get("medical_specialty"))
with col3:
    st.metric("⭐ Score de Visite", f"{visit_score:.0f}/100")
```

#### 2. Section Engagement
```python
engagement = result.get("engagement", {})
col1, col2 = st.columns(2)
with col1:
    engagement_status = "✅ OUI" if engagement.get("obtained") else "❌ NON"
    st.metric("💼 Engagement Obtenu", engagement_status)
with col2:
    st.metric("📊 Score", f"{engagement.get('score', 0):.0%}")
```

#### 3. Section Besoins
```python
detected_needs = result.get("detected_needs", [])
if detected_needs:
    st.markdown("**🏥 Besoins Détectés:**")
    for need in detected_needs:
        st.write(f"  • {need}")
```

#### 4. Section Profil Client
```python
client_typology = result.get("client_typology", {})
st.write(f"**Type Principal:** {client_typology.get('primary')}")
st.write(f"**Confiance:** {client_typology.get('confidence', 0):.0%}")
```

#### 5. Section Produit
```python
proposed_product = result.get("proposed_product", "Non spécifié")
st.markdown(f"**💊 Produit Proposé:** {proposed_product}")
```

---

## Intégration Complète

### Flow Complet (Depuis Utilisateur)

```
1. USER ENTERS CONVERSATION
   ↓
2. Streamlit: 5_BO5_reporting.py
   ↓
3. Python: query_bo5_medical.analyze_conversation()
   ├─ Appelle 8 nouvelles fonctions
   ├─ Enrichit le rapport
   ↓
4. Retourne rapport avec 8 nouveaux champs
   ↓
5. Streamlit: Affiche UI enrichie
   ├─ Métriques
   ├─ Gauge chart
   ├─ Expanders
   ↓
6. User clicks "Sauvegarder dans CRM"
   ↓
7. save_report_to_crm() avec 7 params additionnels
   ↓
8. POST http://localhost:5000/api/reports
   ↓
9. Node.js Express API
   ↓
10. MongoDB: Report.save()
    ├─ 13 champs existants
    ├─ 7 champs nouveaux
    ↓
11. Rapport sauvegardé avec données enrichies
```

---

## Tests

### Test Léger (Logique)
- Fichier: `test_new_features_light.py`
- Pas de dépendances ML
- Résultats: ✓ TOUS LES TESTS PASSENT

### Test Complet (Avec Modèles)
- Fichier: `test_new_features.py`
- Charge les modèles Sentence Transformer
- Temps: ~60 secondes

---

## Performance

### Complexité Temps
- `detect_language()`: O(n) - parcourt texte
- `detect_medical_specialty()`: O(n*m) - n=mots, m=keywords
- `detect_engagement()`: O(n*k) - k=patterns
- `classify_client_typology()`: O(n*k) - k=keywords
- `extract_proposed_product()`: O(n*p) - p=patterns
- `improve_visit_score()`: O(n) - compte questions
- **Total**: O(n) où n = taille du texte

### Utilisation Mémoire
- Minimal: Dictionnaires et listes réutilisés
- Pas d'allocation de modèles supplémentaires
- Compatible avec Streamlit caching

---

## Gestion Erreurs

### Edge Cases Gérés
- ✓ Texte vide → valeurs par défaut
- ✓ Pas de spécialité match → "Médecine Générale"
- ✓ Pas de besoins → liste vide
- ✓ Context vide → extraction de dialogue
- ✓ Engagement score 0 → "Non obtenu"

### Logs Debug
```python
print(f"[DEBUG] Language detected: {language}")
print(f"[DEBUG] Specialty: {specialty}")
print(f"[DEBUG] Score: {visit_score:.1f}")
```

---

## Compatibilité

- ✓ Rétrocompatible avec anciennes données
- ✓ Champs nouveaux optionnels
- ✓ Valeurs par défaut appropriées
- ✓ Pas de breaking changes

---

## Roadmap Futur

- [ ] Fine-tuning des classifieurs avec données réelles
- [ ] Dashboard CRM enrichi
- [ ] Export Excel/CSV avec nuevas columnas
- [ ] Alertes intelligentes
- [ ] Prédictions ML avancées

---

*Documentation Technique - Confidentiel - Avril 2026*
