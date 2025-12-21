#  AeroStream : Système de Classification d'Avis Clients

AeroStream est un projet de bout en bout visant à développer un système intelligent capable de classifier automatiquement les avis clients des compagnies aériennes américaines. Le système analyse le niveau de satisfaction à partir de données textuelles et visualise les résultats en temps réel.

##  Sommaire
* [Objectifs du Projet](#-objectifs-du-projet)
* [Architecture et Méthodologie](#%EF%B8%8F-architecture-et-m%C3%A9thodologie)
* [Technologies Utilisées](#%EF%B8%8F-technologies-utilis%C3%A9es)
* [Installation et Lancement](#-installation-et-lancement)

---

##  Objectifs du Projet
Développer une solution de classification automatique en temps réel permettant de :
* **Collecter et prétraiter** les avis clients issus des réseaux sociaux.
* **Analyser automatiquement** le sentiment et le niveau de satisfaction.
* **Générer des indicateurs** de performance (KPI) par compagnie aérienne.
* **Visualiser les résultats** via un tableau de bord interactif.

---

##  Architecture et Méthodologie
Le projet suit une méthodologie rigoureuse divisée en deux flux principaux :



### 1. Phase Batch (Entraînement)
* **Source de données** : Importation du dataset US Airlines depuis Hugging Face (`7Xan7der7/usairlinesentiment`).
* **Prétraitement** : Nettoyage du texte (suppression des URLs, mentions, ponctuation) et normalisation en minuscules.
* **Extraction de caractéristiques** : Utilisation de **Sentence Transformers** (`intfloat/e5-large-v2`) pour générer des embeddings.
* **Stockage Vectoriel** : Enregistrement des vecteurs et métadonnées dans **ChromaDB** (collections d'entraînement et de test).
* **Modélisation** : Entraînement de modèles de classification (LSTM, RNN) et déploiement via une API REST.

### 2. Phase Streaming (Production)
* **Orchestration** : Utilisation d'**Apache Airflow** pour exécuter le pipeline chaque minute.
* **Ingestion** : Récupération des avis en micro-batch via l'API.
* **Traitement & Stockage** : Prédiction des sentiments et stockage des résultats dans une base **PostgreSQL**.
* **Visualisation** : Dashboard **Streamlit** affichant le volume de tweets, la répartition des sentiments et les causes principales d'insatisfaction.

---

##  Technologies Utilisées

| Composant | Technologie |
| :--- | :--- |
| **NLP / IA** | Hugging Face, Sentence-Transformers, TensorFlow/Keras |
| **Vector DB** | ChromaDB |
| **Relationnelle DB** | PostgreSQL |
| **Orchestration** | Apache Airflow |
| **Dashboard** | Streamlit & Plotly |
| **Langage** | Python (Pandas, SQLAlchemy) |

---

##  Installation et Lancement

### 1. Prérequis
* Docker & Docker Compose
* Python 3.9+

### 2. Lancement des services
```bash
# Lancer PostgreSQL et Airflow via Docker
docker-compose up -d

# Lancer le Dashboard Streamlit
streamlit run streamlit_dashboard.py
