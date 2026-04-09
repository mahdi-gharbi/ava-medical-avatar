# 🚀 COMMANDES DE LANCEMENT - BO5 PROJECT

**Date:** 9 Avril 2026  
**Projet:** AVA BO5 Reporting avec Groq LLM + Chroma

---

## 📋 Table of Contents
1. Setup initial
2. Lancer l'application
3. Tester le système
4. Commandes utiles
5. Troubleshooting

---

## 1️⃣ SETUP INITIAL (UNE SEULE FOIS)

### A) Activer l'environnement virtuel

#### Sur Windows (PowerShell):
```powershell
# Aller au répertoire du projet
cd c:\Users\Lenovo\Desktop\AVA

# Activer venv
.\venv\Scripts\Activate.ps1
```

**Vérifier activation:**
```powershell
# Vous devez voir (venv) au début de votre prompt
(venv) PS C:\Users\Lenovo\Desktop\AVA>
```

#### Sur Windows (CMD):
```cmd
cd c:\Users\Lenovo\Desktop\AVA
venv\Scripts\activate.bat
```

#### Sur Mac/Linux:
```bash
cd ~/Desktop/AVA
source venv/bin/activate
```

### B) Installer les dépendances (si pas fait)
```bash
pip install -r requirements.txt
```

**Output attendu:**
```
Successfully installed groq==X.X.X chromadb==X.X.X streamlit==X.X.X ...
```

### C) Vérifier l'installation
```bash
python -c "import groq, chromadb, streamlit; print('✅ All imports OK')"
```

---

## 2️⃣ LANCER L'APPLICATION (NORMAL)

### Option A: Lancer Streamlit Frontend (RECOMMANDÉ)

```bash
# Depuis la racine du projet
streamlit run frontendstreamlit/app.py
```

**Output attendu:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501

  For better performance, install Pyarrow: pip install pyarrow
```

**Alors:**
1. ✅ Streamlit ouvre automatiquement à `http://localhost:8501`
2. ✅ Naviguez à **"BO5 reporting"** dans sidebar
3. ✅ Sélectionnez un exemple (Cardiologie, Rhumatologie, etc.)
4. ✅ Cliquez "🚀 Générer Rapport avec IA"

### Option B: Lancer Backend API (optionnel, pour BO1-BO4)

```bash
# Terminal 2: Lancer FastAPI backend
python ai_backend/app.py
```

**Output attendu:**
```
INFO:     Started server process [XXXX]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://127.0.0.1:8000
```

---

## 3️⃣ TESTER LE SYSTÈME

### Test 1: Test suite complet (3 conversations)

```bash
# Terminal: Activate venv + run test
cd c:\Users\Lenovo\Desktop\AVA
.\venv\Scripts\Activate.ps1
python test_bo5_complete.py
```

**Output attendu:**
```
================================================================================
🚀 TEST BO5 REPORTING - SUITE COMPLÈTE
================================================================================

🧪 TEST: 🏥 Cardiologie
✅ ANALYSE COMPLÉTÉE

📊 STATISTIQUES:
   Total Exchanges: 15
   Objections Found: 5
   Délégué Messages: 8
   Médecin Messages: 7

✅ Sauvegardé: C:\Users\Lenovo\Desktop\AVA\rapports_archives\rapport_20260409_XXXXXX.json

🧪 TEST: 🩺 Dermatologie
✅ ANALYSE COMPLÉTÉE
...
```

### Test 2: Diagnostic Chroma DB

```bash
python diagnostic_chroma.py
```

**Vérifie:**
- ✅ Collections Chroma (products, bo5_data, etc.)
- ✅ Nombre documents (should be 617)
- ✅ Retrieval scores
- ✅ Data files présents

### Test 3: Amélioration Scores

```bash
python test_improvements.py
```

**Test 5 requêtes différentes:**
- 💊 Cardiologie
- 💰 Prix/Remboursement
- 🛡️ Sécurité
- 📊 Rapport/Objections
- 🩺 Dermatologie

---

## 4️⃣ COMMANDES UTILES

### Arrêter Streamlit
```powershell
# Dans la terminal Streamlit: Ctrl+C
^C
```

### Réindexer Chroma DB (si données changent)

```bash
# Reset complet
python ai_backend/rag/ingest/ingest.py

# Ou ajouter BO6 dataset spécifiquement
python index_bo6.py
```

### Lister les rapports sauvegardés

```powershell
# Sur Windows
dir rapports_archives\

# Ou en Python
python -c "from pathlib import Path; print(list(Path('rapports_archives').glob('*.json')))"
```

### Vider les rapports (ATTENTION!)

```powershell
# Sur Windows
Remove-Item rapports_archives\*

# Sur Mac/Linux
rm rapports_archives/*
```

### Checker les logs

```bash
# Les logs sont affichés dans la terminal où Streamlit tourne
# Pour export dans fichier:

# Lancer avec logs
streamlit run frontendstreamlit/app.py > logs.txt 2>&1
```

### Vérifier la clé Groq

```bash
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('✅ GROQ_API_KEY:', os.getenv('GROQ_API_KEY')[:20]+'...')"
```

### Vérifier Chroma DB

```bash
python -c "import chromadb; c = chromadb.PersistentClient(path='ai_backend/rag/chroma_db'); cols = c.list_collections(); print(f'✅ {len(cols)} collections, {sum(c.get_collection(col.name).count() for col in cols)} docs total')"
```

---

## 5️⃣ WORKFLOW COMPLET (Pas à pas)

### Démarrage du Matin

```powershell
# 1. Ouvrir PowerShell
# 2. Aller au répertoire
cd c:\Users\Lenovo\Desktop\AVA

# 3. Activer venv
.\venv\Scripts\Activate.ps1

# 4. Lancer Streamlit
streamlit run frontendstreamlit/app.py

# 5. ✅ Naviguer à http://localhost:8501

# 6. Aller à BO5 reporting dans sidebar

# 7. Choisir exemple + Générer Rapport
```

### Si Vous Avez une Conversation Personnalisée

```
1. Copy-paste la conversation dans "Dialogue complet"
2. Ajustez les paramètres (Nombre sources: 5-10)
3. Cliquez "🚀 Générer Rapport avec IA"
4. Exportez JSON ou Sauvegardez
```

### Pour Déboguer

```powershell
# Terminal 1: Lancer tests
python test_bo5_complete.py

# Terminal 2: Lancer diagnostic
python diagnostic_chroma.py

# Terminal 3: Lancer Streamlit
streamlit run frontendstreamlit/app.py

# Comparer résultats
```

---

## 📊 ARCHITECTURE SERVICES

```
┌─────────────────────────────────────────────────────────────────┐
│                     STREAMLIT FRONTEND                          │
│                  (Port 8501)                                    │
│              http://localhost:8501                              │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                    PYTHON MODULES                               │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ rag_service.py (retrieve_context, generate_response)   │   │
│  │ query_bo5_medical.py (analyze_conversation, etc.)      │   │
│  └─────────────────────────────────────────────────────────┘   │
└───────────────────────────┬─────────────────────────────────────┘
                            │
              ┌─────────────┴──────────────┐
              ↓                            ↓
    ┌──────────────────┐         ┌──────────────────┐
    │  CHROMA DB       │         │  GROQ API        │
    │  (Local)         │         │  (Cloud)         │
    │  Port: Local FS  │         │  Port: 443       │
    │  617 docs        │         │  llama-3.3-70b   │
    └──────────────────┘         └──────────────────┘
```

---

## 🔗 URLs IMPORTANTES

| Service | URL | Port | Status |
|---------|-----|------|--------|
| Streamlit | http://localhost:8501 | 8501 | ✅ Main App |
| Backend API | http://localhost:8000 | 8000 | ⏸️ Optional |
| Groq Cloud | https://console.groq.com | 443 | ✅ LLM |
| Local Chroma | `ai_backend/rag/chroma_db/` | Local FS | ✅ DB |

---

## 🎯 COMMANDES À GARDER À PORTÉE

### Raccourci PowerShell (créer)

Créer fichier `launch.ps1`:
```powershell
# Fichier: c:\Users\Lenovo\Desktop\AVA\launch.ps1

# Activate venv
.\venv\Scripts\Activate.ps1

# Launch Streamlit
streamlit run frontendstreamlit/app.py
```

**Utilisation:**
```powershell
cd c:\Users\Lenovo\Desktop\AVA
.\launch.ps1
```

---

## ⚠️ PROBLÈMES COURANTS & SOLUTIONS

### Problème 1: "Command 'streamlit' not found"
```bash
# Solution: Réinstaller streamlit
pip install streamlit --upgrade

# Ou utiliser python -m
python -m streamlit run frontendstreamlit/app.py
```

### Problème 2: "ModuleNotFoundError: No module named 'groq'"
```bash
# Solution: Réinstaller requirements
pip install -r requirements.txt

# Ou installer directement
pip install groq chromadb streamlit
```

### Problème 3: "GROQ_API_KEY not found"
```bash
# Vérifier .env existe et a la clé
cat .env  # MAC/Linux
type .env  # Windows (cmd)

# Ou check dans code
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('GROQ_API_KEY'))"
```

### Problème 4: Chroma DB vide
```bash
# Réindexer
python ai_backend/rag/ingest/ingest.py
python index_bo6.py

# Vérifier
python diagnostic_chroma.py
```

### Problème 5: "Connection refused" (port 8501)
```bash
# Port déjà utilisé, tuer le process
# Windows:
netstat -ano | findstr :8501
taskkill /PID XXXX /F

# Ou utiliser autre port
streamlit run frontendstreamlit/app.py --server.port 8502
```

---

## 📝 CHECKLIST DE LANCEMENT

**Avant de lancer:**
- [ ] `cd c:\Users\Lenovo\Desktop\AVA` ✅
- [ ] `.\venv\Scripts\Activate.ps1` ✅ (venv actif)
- [ ] `.env` fichier existe et a `GROQ_API_KEY` ✅
- [ ] `ai_backend/rag/chroma_db/` existe ✅
- [ ] Port 8501 libre ✅

**Au lancement:**
- [ ] `streamlit run frontendstreamlit/app.py` ✅
- [ ] Navigateur ouvre automatiquement ✅
- [ ] Pas d'erreurs rouges en terminal ✅

**Vérifier BO5:**
- [ ] Aller à "BO5 reporting" ✅
- [ ] Sélectionner exemple ✅
- [ ] Cliquer "🚀 Générer Rapport" ✅
- [ ] Voir résultats en 3-5 sec ✅

---

## 🎬 SCÉNARIOS D'UTILISATION

### Scénario 1: Test Quick (5 min)
```bash
# 1. Activate
.\venv\Scripts\Activate.ps1

# 2. Run test
python test_bo5_complete.py

# 3. Check results
dir rapports_archives\
```

### Scénario 2: Interactive Play (15 min)
```bash
# 1. Activate
.\venv\Scripts\Activate.ps1

# 2. Launch Streamlit
streamlit run frontendstreamlit/app.py

# 3. Try 3-4 examples manually
#    (Cardiologie, Rhumatologie, Gastro)

# 4. Export JSON rapports
```

### Scénario 3: Full Development (30+ min)
```bash
# Terminal 1: Tests
python test_bo5_complete.py
python diagnostic_chroma.py
python test_improvements.py

# Terminal 2: Streamlit Frontend
streamlit run frontendstreamlit/app.py

# Terminal 3: Manual testing
python -i query_bo5_medical.py  # Interactive mode
```

---

## 📂 FICHIERS IMPORTANTS

```
c:\Users\Lenovo\Desktop\AVA\
├── .env                                    # ⚠️ GROQ_API_KEY ici!
├── requirements.txt                        # Dependencies
├── frontendstreamlit/
│   ├── app.py                              # 🚀 LANCER ÇA
│   └── pages/5_BO5_reporting.py            # BO5 module
├── ai_backend/
│   ├── services/rag_service.py
│   ├── rag/query/query_bo5_medical.py
│   └── rag/chroma_db/                      # Data
├── rapports_archives/                      # 📄 Rapports sauvegardés
├── test_bo5_complete.py                    # 🧪 Test
├── diagnostic_chroma.py                    # 🔍 Diagnostic
└── launch.ps1                              # 🎬 Raccourci (créer)
```

---

## ✅ QUICK REFERENCE

```bash
# Activate venv
.\venv\Scripts\Activate.ps1

# Launch app
streamlit run frontendstreamlit/app.py

# Run tests
python test_bo5_complete.py

# Diagnose
python diagnostic_chroma.py

# Stop (Ctrl+C)
^C
```

---

**Besoin d'aide?** Relancez avec debug:
```bash
streamlit run frontendstreamlit/app.py --logger.level=debug
```

**Document créé:** 9 Avril 2026  
**Statut:** ✅ READY TO LAUNCH
