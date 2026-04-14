---
tags:
- sentence-transformers
- sentence-similarity
- feature-extraction
- dense
- generated_from_trainer
- dataset_size:300
- loss:TripletLoss
base_model: sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
widget:
- source_sentence: 'REP: Bonjour docteur, je suis du laboratoire VITAL. Est-ce que
    je peux prendre 2 minutes ?

    DOCTOR: Bonjour, oui rapidement.

    REP: Je voulais vous présenter VITALPRESS 10mg (Cardiology). Points clés : Once-daily
    dosing et BP control.

    DOCTOR: Quelle est l’efficacité clinique par rapport aux guidelines ?

    REP: C’est une remarque fréquente. Je peux partager les éléments de comparaison
    et le dossier CNAM si besoin.

    DOCTOR: Vous pouvez me laisser des échantillons ?

    REP: Oui, je peux vous déposer des échantillons lors de la prochaine visite.

    DOCTOR: Très bien, envoyez-moi les informations.

    REP: Parfait. Prochaine étape : Share dosing guidelines. Merci docteur.'
  sentences:
  - 'REP: Bonjour docteur, je suis du laboratoire VITAL. Est-ce que je peux prendre
    2 minutes ?

    DOCTOR: Bonjour, je suis un peu pressé(e).

    REP: Je voulais vous présenter DERMAVITAL Cream (Dermatology). Points clés : Fast
    absorption et Skin relief.

    DOCTOR: Côté sécurité, qu’est-ce que je dois surveiller ?

    REP: Le profil de sécurité est bien documenté, avec des effets indésirables généralement
    légers.

    DOCTOR: Quelles preuves d’efficacité avez-vous ?

    REP: Nous avons des données cliniques montrant une amélioration significative
    selon les recommandations.

    DOCTOR: Très bien, envoyez-moi les informations.

    REP: Parfait. Prochaine étape : Share dosing guidelines. Merci docteur.'
  - 'REP: Bonjour docteur, je suis du laboratoire VITAL. Est-ce que je peux prendre
    2 minutes ?

    DOCTOR: Bonjour, allez-y.

    REP: Je voulais vous présenter CARDIOVITAL 5mg (Cardiology). Points clés : Cardio
    protection et Tolerability.

    DOCTOR: Quelle est la différence clinique par rapport aux alternatives ?

    REP: Les résultats cliniques sont alignés avec les guidelines, et la tolérance
    est bonne.

    DOCTOR: Est-ce que le produit est disponible en stock chez les grossistes ?

    REP: D’accord. On peut démarrer sur un petit nombre de patients et évaluer votre
    retour.

    DOCTOR: Vous pouvez me laisser des échantillons ?

    DOCTOR: Très bien, envoyez-moi les informations.

    REP: Parfait. Prochaine étape : Provide samples. Merci docteur.'
  - 'REP: Bonjour docteur, je suis du laboratoire VITAL. Est-ce que je peux prendre
    2 minutes ?

    DOCTOR: Bonjour, je suis un peu pressé(e).

    REP: Je voulais vous présenter GLUCOVITAL XR (Diabetes). Points clés : Glycemic
    control et Extended release.

    DOCTOR: Quelle est la différence clinique par rapport aux alternatives ?

    REP: Les résultats cliniques sont alignés avec les guidelines, et la tolérance
    est bonne.

    DOCTOR: Je suis inquiet(e) concernant les effets secondaires.

    REP: Je comprends. Je peux vous envoyer une synthèse, et on regarde ensemble l’impact
    pratique.

    DOCTOR: D’accord, on peut planifier une autre visite.

    REP: Parfait. Prochaine étape : Provide samples. Merci docteur.'
- source_sentence: 'REP: Bonjour docteur, je suis du laboratoire VITAL. Est-ce que
    je peux prendre 2 minutes ?

    DOCTOR: Bonjour, allez-y.

    REP: Je voulais vous présenter CARDIOVITAL 5mg (Cardiology). Points clés : Cardio
    protection et Tolerability.

    DOCTOR: Et au niveau des effets secondaires ?

    REP: Le profil de sécurité est bien documenté, avec des effets indésirables généralement
    légers.

    DOCTOR: Quelles preuves d’efficacité avez-vous ?

    REP: Nous avons des données cliniques montrant une amélioration significative
    selon les recommandations.

    DOCTOR: J’utilise déjà un produit concurrent, pourquoi changer ?

    REP: C’est une remarque fréquente. Je peux partager les éléments de comparaison
    et le dossier CNAM si besoin.

    DOCTOR: Très bien, envoyez-moi les informations.

    REP: Parfait. Prochaine étape : Share dosing guidelines. Merci docteur.'
  sentences:
  - 'REP: Bonjour docteur, je suis du laboratoire VITAL. Est-ce que je peux prendre
    2 minutes ?

    DOCTOR: Bonjour, je suis un peu pressé(e).

    REP: Je voulais vous présenter VITALPRESS 10mg (Cardiology). Points clés : BP
    control et Once-daily dosing.

    DOCTOR: Côté sécurité, qu’est-ce que je dois surveiller ?

    REP: La tolérance est bonne, et nous recommandons de suivre les précautions usuelles.

    DOCTOR: J’utilise déjà un produit concurrent, pourquoi changer ?

    REP: D’accord. On peut démarrer sur un petit nombre de patients et évaluer votre
    retour.

    DOCTOR: Quelles preuves d’efficacité avez-vous ?

    REP: Les résultats cliniques sont alignés avec les guidelines, et la tolérance
    est bonne.

    DOCTOR: Très bien, envoyez-moi les informations.

    REP: Parfait. Prochaine étape : Schedule follow-up visit. Merci docteur.'
  - 'REP: Bonjour docteur, je suis du laboratoire VITAL. Est-ce que je peux prendre
    2 minutes ?

    DOCTOR: Bonjour, allez-y.

    REP: Je voulais vous présenter VITALPRESS 10mg (Cardiology). Points clés : Once-daily
    dosing et BP control.

    DOCTOR: Quelles preuves d’efficacité avez-vous ?

    REP: Les résultats cliniques sont alignés avec les guidelines, et la tolérance
    est bonne.

    DOCTOR: Quelle est l’efficacité clinique par rapport aux guidelines ?

    REP: C’est une remarque fréquente. Je peux partager les éléments de comparaison
    et le dossier CNAM si besoin.

    DOCTOR: D’accord, on peut planifier une autre visite.

    REP: Parfait. Prochaine étape : Schedule follow-up visit. Merci docteur.'
  - 'REP: Bonjour docteur, je suis du laboratoire VITAL. Est-ce que je peux prendre
    2 minutes ?

    DOCTOR: Bonjour, allez-y.

    REP: Je voulais vous présenter CARDIOVITAL 5mg (Cardiology). Points clés : Cardio
    protection et Tolerability.

    DOCTOR: Côté sécurité, qu’est-ce que je dois surveiller ?

    REP: La tolérance est bonne, et nous recommandons de suivre les précautions usuelles.

    DOCTOR: Est-ce que c’est remboursé par la CNAM ?

    REP: Je comprends. Je peux vous envoyer une synthèse, et on regarde ensemble l’impact
    pratique.

    DOCTOR: Quelle est la différence clinique par rapport aux alternatives ?

    REP: Les résultats cliniques sont alignés avec les guidelines, et la tolérance
    est bonne.

    DOCTOR: Vous pouvez me laisser des échantillons ?

    REP: Oui, je peux vous déposer des échantillons lors de la prochaine visite.

    DOCTOR: Très bien, envoyez-moi les informations.

    REP: Parfait. Prochaine étape : Schedule follow-up visit. Merci docteur.'
- source_sentence: 'REP: Bonjour docteur, je suis du laboratoire VITAL. Est-ce que
    je peux prendre 2 minutes ?

    DOCTOR: Bonjour, allez-y.

    REP: Je voulais vous présenter CARDIOVITAL 5mg (Cardiology). Points clés : Tolerability
    et Cardio protection.

    DOCTOR: Quelle est la différence clinique par rapport aux alternatives ?

    REP: Les résultats cliniques sont alignés avec les guidelines, et la tolérance
    est bonne.

    DOCTOR: J’utilise déjà un produit concurrent, pourquoi changer ?

    REP: Je comprends. Je peux vous envoyer une synthèse, et on regarde ensemble l’impact
    pratique.

    DOCTOR: Côté sécurité, qu’est-ce que je dois surveiller ?

    REP: La tolérance est bonne, et nous recommandons de suivre les précautions usuelles.

    DOCTOR: Très bien, envoyez-moi les informations.

    REP: Parfait. Prochaine étape : Send clinical study summary. Merci docteur.'
  sentences:
  - 'REP: Bonjour docteur, je suis du laboratoire VITAL. Est-ce que je peux prendre
    2 minutes ?

    DOCTOR: Bonjour, allez-y.

    REP: Je voulais vous présenter GLUCOVITAL XR (Diabetes). Points clés : Extended
    release et Glycemic control.

    DOCTOR: Côté sécurité, qu’est-ce que je dois surveiller ?

    REP: Le profil de sécurité est bien documenté, avec des effets indésirables généralement
    légers.

    DOCTOR: J’utilise déjà un produit concurrent, pourquoi changer ?

    REP: D’accord. On peut démarrer sur un petit nombre de patients et évaluer votre
    retour.

    DOCTOR: Ok, je vais y réfléchir.

    REP: Parfait. Prochaine étape : Send CNAM reimbursement document. Merci docteur.'
  - 'REP: Bonjour docteur, je suis du laboratoire VITAL. Est-ce que je peux prendre
    2 minutes ?

    DOCTOR: Bonjour, oui rapidement.

    REP: Je voulais vous présenter VITACEF 500mg (Antibiotic). Points clés : Broad
    spectrum et Rapid response.

    DOCTOR: Est-ce que le produit est disponible en stock chez les grossistes ?

    REP: C’est une remarque fréquente. Je peux partager les éléments de comparaison
    et le dossier CNAM si besoin.

    DOCTOR: Côté sécurité, qu’est-ce que je dois surveiller ?

    REP: La tolérance est bonne, et nous recommandons de suivre les précautions usuelles.

    DOCTOR: Quelle est la différence clinique par rapport aux alternatives ?

    REP: Les résultats cliniques sont alignés avec les guidelines, et la tolérance
    est bonne.

    DOCTOR: Très bien, envoyez-moi les informations.

    REP: Parfait. Prochaine étape : Send clinical study summary. Merci docteur.'
  - 'REP: Bonjour docteur, je suis du laboratoire VITAL. Est-ce que je peux prendre
    2 minutes ?

    DOCTOR: Bonjour, oui rapidement.

    REP: Je voulais vous présenter GLUCOVITAL XR (Diabetes). Points clés : Glycemic
    control et Extended release.

    DOCTOR: Quelle est la différence clinique par rapport aux alternatives ?

    REP: Les résultats cliniques sont alignés avec les guidelines, et la tolérance
    est bonne.

    DOCTOR: Je suis inquiet(e) concernant les effets secondaires.

    REP: Je comprends. Je peux vous envoyer une synthèse, et on regarde ensemble l’impact
    pratique.

    DOCTOR: D’accord, on peut planifier une autre visite.

    REP: Parfait. Prochaine étape : Send clinical study summary. Merci docteur.'
- source_sentence: 'REP: Bonjour docteur, je suis du laboratoire VITAL. Est-ce que
    je peux prendre 2 minutes ?

    DOCTOR: Bonjour, allez-y.

    REP: Je voulais vous présenter VITALPRESS 10mg (Cardiology). Points clés : Once-daily
    dosing et BP control.

    DOCTOR: Je suis inquiet(e) concernant les effets secondaires.

    REP: Je comprends. Je peux vous envoyer une synthèse, et on regarde ensemble l’impact
    pratique.

    DOCTOR: Côté sécurité, qu’est-ce que je dois surveiller ?

    REP: La tolérance est bonne, et nous recommandons de suivre les précautions usuelles.

    DOCTOR: Vous pouvez me laisser des échantillons ?

    DOCTOR: Ok, je vais y réfléchir.

    REP: Parfait. Prochaine étape : Send CNAM reimbursement document. Merci docteur.'
  sentences:
  - 'REP: Bonjour docteur, je suis du laboratoire VITAL. Est-ce que je peux prendre
    2 minutes ?

    DOCTOR: Bonjour, je suis un peu pressé(e).

    REP: Je voulais vous présenter DERMAVITAL Cream (Dermatology). Points clés : Skin
    relief et Fast absorption.

    DOCTOR: Côté sécurité, qu’est-ce que je dois surveiller ?

    REP: La tolérance est bonne, et nous recommandons de suivre les précautions usuelles.

    DOCTOR: Quelle est l’efficacité clinique par rapport aux guidelines ?

    REP: Je comprends. Je peux vous envoyer une synthèse, et on regarde ensemble l’impact
    pratique.

    DOCTOR: D’accord, on peut planifier une autre visite.

    REP: Parfait. Prochaine étape : Connect with medical information team. Merci docteur.'
  - 'REP: Bonjour docteur, je suis du laboratoire VITAL. Est-ce que je peux prendre
    2 minutes ?

    DOCTOR: Bonjour, allez-y.

    REP: Je voulais vous présenter DERMAVITAL Cream (Dermatology). Points clés : Fast
    absorption et Skin relief.

    DOCTOR: Quelles preuves d’efficacité avez-vous ?

    REP: Nous avons des données cliniques montrant une amélioration significative
    selon les recommandations.

    DOCTOR: Côté sécurité, qu’est-ce que je dois surveiller ?

    REP: Le profil de sécurité est bien documenté, avec des effets indésirables généralement
    légers.

    DOCTOR: Je suis inquiet(e) concernant les effets secondaires.

    REP: Je comprends. Je peux vous envoyer une synthèse, et on regarde ensemble l’impact
    pratique.

    DOCTOR: Vous avez une étude à me partager ?

    REP: Oui bien sûr, je vous l’envoie aujourd’hui.

    DOCTOR: Ok, je vais y réfléchir.

    REP: Parfait. Prochaine étape : Schedule follow-up visit. Merci docteur.'
  - 'REP: Bonjour docteur, je suis du laboratoire VITAL. Est-ce que je peux prendre
    2 minutes ?

    DOCTOR: Bonjour, allez-y.

    REP: Je voulais vous présenter GLUCOVITAL XR (Diabetes). Points clés : Extended
    release et Glycemic control.

    DOCTOR: Côté sécurité, qu’est-ce que je dois surveiller ?

    REP: Le profil de sécurité est bien documenté, avec des effets indésirables généralement
    légers.

    DOCTOR: J’utilise déjà un produit concurrent, pourquoi changer ?

    REP: D’accord. On peut démarrer sur un petit nombre de patients et évaluer votre
    retour.

    DOCTOR: Ok, je vais y réfléchir.

    REP: Parfait. Prochaine étape : Send CNAM reimbursement document. Merci docteur.'
- source_sentence: 'REP: Bonjour docteur, je suis du laboratoire VITAL. Est-ce que
    je peux prendre 2 minutes ?

    DOCTOR: Bonjour, oui rapidement.

    REP: Je voulais vous présenter VITALPRESS 10mg (Cardiology). Points clés : BP
    control et Once-daily dosing.

    DOCTOR: Est-ce que le produit est disponible en stock chez les grossistes ?

    REP: Je comprends. Je peux vous envoyer une synthèse, et on regarde ensemble l’impact
    pratique.

    DOCTOR: Quelle est la différence clinique par rapport aux alternatives ?

    REP: Les résultats cliniques sont alignés avec les guidelines, et la tolérance
    est bonne.

    DOCTOR: Vous pouvez me laisser des échantillons ?

    REP: Oui, je peux vous déposer des échantillons lors de la prochaine visite.

    DOCTOR: Ok, je vais y réfléchir.

    REP: Parfait. Prochaine étape : Share dosing guidelines. Merci docteur.'
  sentences:
  - 'REP: Bonjour docteur, je suis du laboratoire VITAL. Est-ce que je peux prendre
    2 minutes ?

    DOCTOR: Bonjour, je suis un peu pressé(e).

    REP: Je voulais vous présenter CARDIOVITAL 5mg (Cardiology). Points clés : Cardio
    protection et Tolerability.

    DOCTOR: Quelle est l’efficacité clinique par rapport aux guidelines ?

    REP: C’est une remarque fréquente. Je peux partager les éléments de comparaison
    et le dossier CNAM si besoin.

    DOCTOR: Quelle est la différence clinique par rapport aux alternatives ?

    REP: Nous avons des données cliniques montrant une amélioration significative
    selon les recommandations.

    DOCTOR: Très bien, envoyez-moi les informations.

    REP: Parfait. Prochaine étape : Share dosing guidelines. Merci docteur.'
  - 'REP: Bonjour docteur, je suis du laboratoire VITAL. Est-ce que je peux prendre
    2 minutes ?

    DOCTOR: Bonjour, oui rapidement.

    REP: Je voulais vous présenter CARDIOVITAL 5mg (Cardiology). Points clés : Cardio
    protection et Tolerability.

    DOCTOR: Est-ce que le produit est disponible en stock chez les grossistes ?

    REP: Je comprends. Je peux vous envoyer une synthèse, et on regarde ensemble l’impact
    pratique.

    DOCTOR: Vous pouvez me laisser des échantillons ?

    REP: Oui, je peux vous déposer des échantillons lors de la prochaine visite.

    DOCTOR: Très bien, envoyez-moi les informations.

    REP: Parfait. Prochaine étape : Send clinical study summary. Merci docteur.'
  - 'REP: Bonjour docteur, je suis du laboratoire VITAL. Est-ce que je peux prendre
    2 minutes ?

    DOCTOR: Bonjour, allez-y.

    REP: Je voulais vous présenter CARDIOVITAL 5mg (Cardiology). Points clés : Cardio
    protection et Tolerability.

    DOCTOR: Et au niveau des effets secondaires ?

    REP: Le profil de sécurité est bien documenté, avec des effets indésirables généralement
    légers.

    DOCTOR: Quelles preuves d’efficacité avez-vous ?

    REP: Nous avons des données cliniques montrant une amélioration significative
    selon les recommandations.

    DOCTOR: J’utilise déjà un produit concurrent, pourquoi changer ?

    REP: C’est une remarque fréquente. Je peux partager les éléments de comparaison
    et le dossier CNAM si besoin.

    DOCTOR: Très bien, envoyez-moi les informations.

    REP: Parfait. Prochaine étape : Share dosing guidelines. Merci docteur.'
pipeline_tag: sentence-similarity
library_name: sentence-transformers
---

# SentenceTransformer based on sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2

This is a [sentence-transformers](https://www.SBERT.net) model finetuned from [sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2). It maps sentences & paragraphs to a 384-dimensional dense vector space and can be used for semantic textual similarity, semantic search, paraphrase mining, text classification, clustering, and more.

## Model Details

### Model Description
- **Model Type:** Sentence Transformer
- **Base model:** [sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2) <!-- at revision e8f8c211226b894fcb81acc59f3b34ba3efd5f42 -->
- **Maximum Sequence Length:** 128 tokens
- **Output Dimensionality:** 384 dimensions
- **Similarity Function:** Cosine Similarity
<!-- - **Training Dataset:** Unknown -->
<!-- - **Language:** Unknown -->
<!-- - **License:** Unknown -->

### Model Sources

- **Documentation:** [Sentence Transformers Documentation](https://sbert.net)
- **Repository:** [Sentence Transformers on GitHub](https://github.com/huggingface/sentence-transformers)
- **Hugging Face:** [Sentence Transformers on Hugging Face](https://huggingface.co/models?library=sentence-transformers)

### Full Model Architecture

```
SentenceTransformer(
  (0): Transformer({'max_seq_length': 128, 'do_lower_case': False, 'architecture': 'BertModel'})
  (1): Pooling({'word_embedding_dimension': 384, 'pooling_mode_cls_token': False, 'pooling_mode_mean_tokens': True, 'pooling_mode_max_tokens': False, 'pooling_mode_mean_sqrt_len_tokens': False, 'pooling_mode_weightedmean_tokens': False, 'pooling_mode_lasttoken': False, 'include_prompt': True})
)
```

## Usage

### Direct Usage (Sentence Transformers)

First install the Sentence Transformers library:

```bash
pip install -U sentence-transformers
```

Then you can load this model and run inference.
```python
from sentence_transformers import SentenceTransformer

# Download from the 🤗 Hub
model = SentenceTransformer("sentence_transformers_model_id")
# Run inference
sentences = [
    'REP: Bonjour docteur, je suis du laboratoire VITAL. Est-ce que je peux prendre 2 minutes ?\nDOCTOR: Bonjour, oui rapidement.\nREP: Je voulais vous présenter VITALPRESS 10mg (Cardiology). Points clés : BP control et Once-daily dosing.\nDOCTOR: Est-ce que le produit est disponible en stock chez les grossistes ?\nREP: Je comprends. Je peux vous envoyer une synthèse, et on regarde ensemble l’impact pratique.\nDOCTOR: Quelle est la différence clinique par rapport aux alternatives ?\nREP: Les résultats cliniques sont alignés avec les guidelines, et la tolérance est bonne.\nDOCTOR: Vous pouvez me laisser des échantillons ?\nREP: Oui, je peux vous déposer des échantillons lors de la prochaine visite.\nDOCTOR: Ok, je vais y réfléchir.\nREP: Parfait. Prochaine étape : Share dosing guidelines. Merci docteur.',
    'REP: Bonjour docteur, je suis du laboratoire VITAL. Est-ce que je peux prendre 2 minutes ?\nDOCTOR: Bonjour, oui rapidement.\nREP: Je voulais vous présenter CARDIOVITAL 5mg (Cardiology). Points clés : Cardio protection et Tolerability.\nDOCTOR: Est-ce que le produit est disponible en stock chez les grossistes ?\nREP: Je comprends. Je peux vous envoyer une synthèse, et on regarde ensemble l’impact pratique.\nDOCTOR: Vous pouvez me laisser des échantillons ?\nREP: Oui, je peux vous déposer des échantillons lors de la prochaine visite.\nDOCTOR: Très bien, envoyez-moi les informations.\nREP: Parfait. Prochaine étape : Send clinical study summary. Merci docteur.',
    'REP: Bonjour docteur, je suis du laboratoire VITAL. Est-ce que je peux prendre 2 minutes ?\nDOCTOR: Bonjour, allez-y.\nREP: Je voulais vous présenter CARDIOVITAL 5mg (Cardiology). Points clés : Cardio protection et Tolerability.\nDOCTOR: Et au niveau des effets secondaires ?\nREP: Le profil de sécurité est bien documenté, avec des effets indésirables généralement légers.\nDOCTOR: Quelles preuves d’efficacité avez-vous ?\nREP: Nous avons des données cliniques montrant une amélioration significative selon les recommandations.\nDOCTOR: J’utilise déjà un produit concurrent, pourquoi changer ?\nREP: C’est une remarque fréquente. Je peux partager les éléments de comparaison et le dossier CNAM si besoin.\nDOCTOR: Très bien, envoyez-moi les informations.\nREP: Parfait. Prochaine étape : Share dosing guidelines. Merci docteur.',
]
embeddings = model.encode(sentences)
print(embeddings.shape)
# [3, 384]

# Get the similarity scores for the embeddings
similarities = model.similarity(embeddings, embeddings)
print(similarities)
# tensor([[1.0000, 0.8540, 0.8218],
#         [0.8540, 1.0000, 0.9838],
#         [0.8218, 0.9838, 1.0000]])
```

<!--
### Direct Usage (Transformers)

<details><summary>Click to see the direct usage in Transformers</summary>

</details>
-->

<!--
### Downstream Usage (Sentence Transformers)

You can finetune this model on your own dataset.

<details><summary>Click to expand</summary>

</details>
-->

<!--
### Out-of-Scope Use

*List how the model may foreseeably be misused and address what users ought not to do with the model.*
-->

<!--
## Bias, Risks and Limitations

*What are the known or foreseeable issues stemming from this model? You could also flag here known failure cases or weaknesses of the model.*
-->

<!--
### Recommendations

*What are recommendations with respect to the foreseeable issues? For example, filtering explicit content.*
-->

## Training Details

### Training Dataset

#### Unnamed Dataset

* Size: 300 training samples
* Columns: <code>sentence_0</code>, <code>sentence_1</code>, and <code>sentence_2</code>
* Approximate statistics based on the first 300 samples:
  |         | sentence_0                                                                           | sentence_1                                                                           | sentence_2                                                                           |
  |:--------|:-------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------|
  | type    | string                                                                               | string                                                                               | string                                                                               |
  | details | <ul><li>min: 128 tokens</li><li>mean: 128.0 tokens</li><li>max: 128 tokens</li></ul> | <ul><li>min: 128 tokens</li><li>mean: 128.0 tokens</li><li>max: 128 tokens</li></ul> | <ul><li>min: 128 tokens</li><li>mean: 128.0 tokens</li><li>max: 128 tokens</li></ul> |
* Samples:
  | sentence_0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | sentence_1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | sentence_2                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
  |:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
  | <code>REP: Bonjour docteur, je suis du laboratoire VITAL. Est-ce que je peux prendre 2 minutes ?<br>DOCTOR: Bonjour, allez-y.<br>REP: Je voulais vous présenter GLUCOVITAL XR (Diabetes). Points clés : Glycemic control et Extended release.<br>DOCTOR: Quelle est la différence clinique par rapport aux alternatives ?<br>REP: Nous avons des données cliniques montrant une amélioration significative selon les recommandations.<br>DOCTOR: Je suis inquiet(e) concernant les effets secondaires.<br>REP: D’accord. On peut démarrer sur un petit nombre de patients et évaluer votre retour.<br>DOCTOR: D’accord, on peut planifier une autre visite.<br>REP: Parfait. Prochaine étape : Connect with medical information team. Merci docteur.</code>                                                                                                                                                             | <code>REP: Bonjour docteur, je suis du laboratoire VITAL. Est-ce que je peux prendre 2 minutes ?<br>DOCTOR: Bonjour, oui rapidement.<br>REP: Je voulais vous présenter GLUCOVITAL XR (Diabetes). Points clés : Extended release et Glycemic control.<br>DOCTOR: Je suis inquiet(e) concernant les effets secondaires.<br>REP: C’est une remarque fréquente. Je peux partager les éléments de comparaison et le dossier CNAM si besoin.<br>DOCTOR: Vous pouvez me laisser des échantillons ?<br>DOCTOR: Très bien, envoyez-moi les informations.<br>REP: Parfait. Prochaine étape : Connect with medical information team. Merci docteur.</code>                                                                                                                                                                                                                               | <code>REP: Bonjour docteur, je suis du laboratoire VITAL. Est-ce que je peux prendre 2 minutes ?<br>DOCTOR: Bonjour, oui rapidement.<br>REP: Je voulais vous présenter VITALPRESS 10mg (Cardiology). Points clés : BP control et Once-daily dosing.<br>DOCTOR: Est-ce que le produit est disponible en stock chez les grossistes ?<br>REP: Je comprends. Je peux vous envoyer une synthèse, et on regarde ensemble l’impact pratique.<br>DOCTOR: Quelle est la différence clinique par rapport aux alternatives ?<br>REP: Les résultats cliniques sont alignés avec les guidelines, et la tolérance est bonne.<br>DOCTOR: Vous pouvez me laisser des échantillons ?<br>REP: Oui, je peux vous déposer des échantillons lors de la prochaine visite.<br>DOCTOR: Ok, je vais y réfléchir.<br>REP: Parfait. Prochaine étape : Share dosing guidelines. Merci docteur.</code> |
  | <code>REP: Bonjour docteur, je suis du laboratoire VITAL. Est-ce que je peux prendre 2 minutes ?<br>DOCTOR: Bonjour, je suis un peu pressé(e).<br>REP: Je voulais vous présenter DERMAVITAL Cream (Dermatology). Points clés : Fast absorption et Skin relief.<br>DOCTOR: Côté sécurité, qu’est-ce que je dois surveiller ?<br>REP: Le profil de sécurité est bien documenté, avec des effets indésirables généralement légers.<br>DOCTOR: Quelle est l’efficacité clinique par rapport aux guidelines ?<br>REP: Je comprends. Je peux vous envoyer une synthèse, et on regarde ensemble l’impact pratique.<br>DOCTOR: Quelles preuves d’efficacité avez-vous ?<br>REP: Nous avons des données cliniques montrant une amélioration significative selon les recommandations.<br>DOCTOR: D’accord, on peut planifier une autre visite.<br>REP: Parfait. Prochaine étape : Schedule follow-up visit. Merci docteur.</code> | <code>REP: Bonjour docteur, je suis du laboratoire VITAL. Est-ce que je peux prendre 2 minutes ?<br>DOCTOR: Bonjour, allez-y.<br>REP: Je voulais vous présenter GLUCOVITAL XR (Diabetes). Points clés : Extended release et Glycemic control.<br>DOCTOR: Et au niveau des effets secondaires ?<br>REP: Le profil de sécurité est bien documenté, avec des effets indésirables généralement légers.<br>DOCTOR: Quelle est la différence clinique par rapport aux alternatives ?<br>REP: Nous avons des données cliniques montrant une amélioration significative selon les recommandations.<br>DOCTOR: Quelle est l’efficacité clinique par rapport aux guidelines ?<br>REP: D’accord. On peut démarrer sur un petit nombre de patients et évaluer votre retour.<br>DOCTOR: Ok, je vais y réfléchir.<br>REP: Parfait. Prochaine étape : Provide samples. Merci docteur.</code> | <code>REP: Bonjour docteur, je suis du laboratoire VITAL. Est-ce que je peux prendre 2 minutes ?<br>DOCTOR: Bonjour, allez-y.<br>REP: Je voulais vous présenter DERMAVITAL Cream (Dermatology). Points clés : Fast absorption et Skin relief.<br>DOCTOR: Je suis inquiet(e) concernant les effets secondaires.<br>REP: Je comprends. Je peux vous envoyer une synthèse, et on regarde ensemble l’impact pratique.<br>DOCTOR: Quelles preuves d’efficacité avez-vous ?<br>DOCTOR: D’accord, on peut planifier une autre visite.<br>REP: Parfait. Prochaine étape : Connect with medical information team. Merci docteur.</code>                                                                                                                                                                                                                                            |
  | <code>REP: Bonjour docteur, je suis du laboratoire VITAL. Est-ce que je peux prendre 2 minutes ?<br>DOCTOR: Bonjour, je suis un peu pressé(e).<br>REP: Je voulais vous présenter GLUCOVITAL XR (Diabetes). Points clés : Glycemic control et Extended release.<br>DOCTOR: Je suis inquiet(e) concernant les effets secondaires.<br>REP: Je comprends. Je peux vous envoyer une synthèse, et on regarde ensemble l’impact pratique.<br>DOCTOR: Quelles preuves d’efficacité avez-vous ?<br>REP: Nous avons des données cliniques montrant une amélioration significative selon les recommandations.<br>DOCTOR: Ok, je vais y réfléchir.<br>REP: Parfait. Prochaine étape : Send clinical study summary. Merci docteur.</code>                                                                                                                                                                                            | <code>REP: Bonjour docteur, je suis du laboratoire VITAL. Est-ce que je peux prendre 2 minutes ?<br>DOCTOR: Bonjour, allez-y.<br>REP: Je voulais vous présenter VITACEF 500mg (Antibiotic). Points clés : Rapid response et Broad spectrum.<br>DOCTOR: Je suis inquiet(e) concernant les effets secondaires.<br>REP: C’est une remarque fréquente. Je peux partager les éléments de comparaison et le dossier CNAM si besoin.<br>DOCTOR: Ok, je vais y réfléchir.<br>REP: Parfait. Prochaine étape : Schedule follow-up visit. Merci docteur.</code>                                                                                                                                                                                                                                                                                                                          | <code>REP: Bonjour docteur, je suis du laboratoire VITAL. Est-ce que je peux prendre 2 minutes ?<br>DOCTOR: Bonjour, je suis un peu pressé(e).<br>REP: Je voulais vous présenter GLUCOVITAL XR (Diabetes). Points clés : Glycemic control et Extended release.<br>DOCTOR: Le prix est un peu élevé par rapport aux alternatives.<br>REP: C’est une remarque fréquente. Je peux partager les éléments de comparaison et le dossier CNAM si besoin.<br>DOCTOR: Côté sécurité, qu’est-ce que je dois surveiller ?<br>REP: La tolérance est bonne, et nous recommandons de suivre les précautions usuelles.<br>DOCTOR: Ok, je vais y réfléchir.<br>REP: Parfait. Prochaine étape : Send clinical study summary. Merci docteur.</code>                                                                                                                                         |
* Loss: [<code>TripletLoss</code>](https://sbert.net/docs/package_reference/sentence_transformer/losses.html#tripletloss) with these parameters:
  ```json
  {
      "distance_metric": "TripletDistanceMetric.EUCLIDEAN",
      "triplet_margin": 5
  }
  ```

### Training Hyperparameters
#### Non-Default Hyperparameters

- `per_device_train_batch_size`: 16
- `per_device_eval_batch_size`: 16
- `multi_dataset_batch_sampler`: round_robin

#### All Hyperparameters
<details><summary>Click to expand</summary>

- `per_device_train_batch_size`: 16
- `num_train_epochs`: 3
- `max_steps`: -1
- `learning_rate`: 5e-05
- `lr_scheduler_type`: linear
- `lr_scheduler_kwargs`: None
- `warmup_steps`: 0
- `optim`: adamw_torch_fused
- `optim_args`: None
- `weight_decay`: 0.0
- `adam_beta1`: 0.9
- `adam_beta2`: 0.999
- `adam_epsilon`: 1e-08
- `optim_target_modules`: None
- `gradient_accumulation_steps`: 1
- `average_tokens_across_devices`: True
- `max_grad_norm`: 1
- `label_smoothing_factor`: 0.0
- `bf16`: False
- `fp16`: False
- `bf16_full_eval`: False
- `fp16_full_eval`: False
- `tf32`: None
- `gradient_checkpointing`: False
- `gradient_checkpointing_kwargs`: None
- `torch_compile`: False
- `torch_compile_backend`: None
- `torch_compile_mode`: None
- `use_liger_kernel`: False
- `liger_kernel_config`: None
- `use_cache`: False
- `neftune_noise_alpha`: None
- `torch_empty_cache_steps`: None
- `auto_find_batch_size`: False
- `log_on_each_node`: True
- `logging_nan_inf_filter`: True
- `include_num_input_tokens_seen`: no
- `log_level`: passive
- `log_level_replica`: warning
- `disable_tqdm`: False
- `project`: huggingface
- `trackio_space_id`: trackio
- `eval_strategy`: no
- `per_device_eval_batch_size`: 16
- `prediction_loss_only`: True
- `eval_on_start`: False
- `eval_do_concat_batches`: True
- `eval_use_gather_object`: False
- `eval_accumulation_steps`: None
- `include_for_metrics`: []
- `batch_eval_metrics`: False
- `save_only_model`: False
- `save_on_each_node`: False
- `enable_jit_checkpoint`: False
- `push_to_hub`: False
- `hub_private_repo`: None
- `hub_model_id`: None
- `hub_strategy`: every_save
- `hub_always_push`: False
- `hub_revision`: None
- `load_best_model_at_end`: False
- `ignore_data_skip`: False
- `restore_callback_states_from_checkpoint`: False
- `full_determinism`: False
- `seed`: 42
- `data_seed`: None
- `use_cpu`: False
- `accelerator_config`: {'split_batches': False, 'dispatch_batches': None, 'even_batches': True, 'use_seedable_sampler': True, 'non_blocking': False, 'gradient_accumulation_kwargs': None}
- `parallelism_config`: None
- `dataloader_drop_last`: False
- `dataloader_num_workers`: 0
- `dataloader_pin_memory`: True
- `dataloader_persistent_workers`: False
- `dataloader_prefetch_factor`: None
- `remove_unused_columns`: True
- `label_names`: None
- `train_sampling_strategy`: random
- `length_column_name`: length
- `ddp_find_unused_parameters`: None
- `ddp_bucket_cap_mb`: None
- `ddp_broadcast_buffers`: False
- `ddp_backend`: None
- `ddp_timeout`: 1800
- `fsdp`: []
- `fsdp_config`: {'min_num_params': 0, 'xla': False, 'xla_fsdp_v2': False, 'xla_fsdp_grad_ckpt': False}
- `deepspeed`: None
- `debug`: []
- `skip_memory_metrics`: True
- `do_predict`: False
- `resume_from_checkpoint`: None
- `warmup_ratio`: None
- `local_rank`: -1
- `prompts`: None
- `batch_sampler`: batch_sampler
- `multi_dataset_batch_sampler`: round_robin
- `router_mapping`: {}
- `learning_rate_mapping`: {}

</details>

### Framework Versions
- Python: 3.13.2
- Sentence Transformers: 5.3.0
- Transformers: 5.5.0
- PyTorch: 2.11.0+cpu
- Accelerate: 1.13.0
- Datasets: 4.8.4
- Tokenizers: 0.22.2

## Citation

### BibTeX

#### Sentence Transformers
```bibtex
@inproceedings{reimers-2019-sentence-bert,
    title = "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks",
    author = "Reimers, Nils and Gurevych, Iryna",
    booktitle = "Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing",
    month = "11",
    year = "2019",
    publisher = "Association for Computational Linguistics",
    url = "https://arxiv.org/abs/1908.10084",
}
```

#### TripletLoss
```bibtex
@misc{hermans2017defense,
    title={In Defense of the Triplet Loss for Person Re-Identification},
    author={Alexander Hermans and Lucas Beyer and Bastian Leibe},
    year={2017},
    eprint={1703.07737},
    archivePrefix={arXiv},
    primaryClass={cs.CV}
}
```

<!--
## Glossary

*Clearly define terms in order to be accessible across audiences.*
-->

<!--
## Model Card Authors

*Lists the people who create the model card, providing recognition and accountability for the detailed work that goes into its construction.*
-->

<!--
## Model Card Contact

*Provides a way for people who have updates to the Model Card, suggestions, or questions, to contact the Model Card authors.*
-->