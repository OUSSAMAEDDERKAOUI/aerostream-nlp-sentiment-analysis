
import streamlit as st



st.set_page_config(page_title="AeroStream - Dashboard Sentiment Analyse", layout="wide")

st.title(" AeroStream - Analyse des avis clients des compagnies aériennes")
st.markdown("""
Bienvenue sur le **dashboard AeroStream**. Ce système intelligent permet de classifier automatiquement les avis clients 
relatifs aux services des compagnies aériennes et d'analyser le niveau de satisfaction des utilisateurs en temps réel.
""")

st.header(" Contexte du projet")
st.markdown("""
AeroStream souhaite développer un système capable de :

- Collecter et prétraiter les avis clients.
- Analyser automatiquement le sentiment et la satisfaction.
- Générer des indicateurs de performance par compagnie aérienne.
- Visualiser les résultats via un tableau de bord interactif.
""")

st.header(" Objectifs")
st.markdown("""
Le dashboard a pour objectif de :

1. Classifier automatiquement les avis clients.
2. Mesurer les indicateurs de satisfaction et de performance.
3. Fournir des visualisations interactives pour faciliter la prise de décision.
""")

st.header(" Pipeline Batch")
st.markdown("""
- **Chargement des données** : Importation du dataset US Airlines depuis Hugging Face.
- **Analyse exploratoire (EDA)** : Répartition des classes, distributions et statistiques principales.
- **Nettoyage et normalisation des données** : Suppression des doublons, nettoyage du texte et homogénéisation.
- **Génération des embeddings** : Utilisation de Sentence Transformers (`intfloat/e5-large-v2`).
- **Stockage des embeddings et métadonnées** : Collections ChromaDB pour train et test.
- **Entraînement des modèles** : Récupération des embeddings pour l'apprentissage.
- **Évaluation et sauvegarde** : Conserver le meilleur modèle pour la prédiction future.
- **Déploiement** : Mise à disposition via une API REST.
""")

st.header(" Pipeline Streaming")
st.markdown("""
- **Récupération des données en micro-batch** : Collecte des avis via l’API.
- **Prétraitement des avis** : Nettoyage pour la prédiction des sentiments.
- **Stockage des résultats** : Base PostgreSQL.
- **Agrégation des données** : 
  - Volume de tweets par compagnie  
  - Répartition des sentiments  
  - Taux de satisfaction par compagnie  
  - Causes principales de tweets négatifs
- **Visualisation interactive** : KPI principaux intégrés dans le dashboard :
  - Nombre total de tweets  
  - Nombre de compagnies aériennes  
  - Pourcentage de tweets négatifs
- **Automatisation** : Pipeline orchestré via DAG Airflow exécuté toutes les minutes.
""")

st.info(" Utilisez le menu à gauche pour naviguer entre les pages du dashboard : métriques des modèles, streaming des données et visualisations.")
