import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, roc_curve, roc_auc_score

metrics_df=pd.read_csv("/opt/airflow/data/streamlit_df/metrics_logreg.csv")
cm_df=pd.read_csv("/opt/airflow/data/streamlit_df/cm_logreg.csv",index_col=0)
report_df = pd.read_csv("/opt/airflow/data/streamlit_df/report_logreg.csv", index_col=0)

st.title("📊 Évaluation du modèle")
st.write("""
Cette page présente les principales métriques de performance du modèle, incluant :
- Accuracy
- Precision
- Recall
- F1-score
- AUC

Vous pouvez également visualiser la matrice de confusion et la courbe ROC pour analyser la performance du modèle.
""")







st.subheader("📊 Métriques du modèle")

model = metrics_df["Model"][0]
accuracy = metrics_df["Accuracy"][0]
f1_score = metrics_df["F1_score"][0]
accuracy_gap=metrics_df["Gap"][0]


for idx, row in metrics_df.iterrows():
    st.write(f"### {row['Model']}")  
    col1, col2, col3 = st.columns(3)
    col1.metric("Accuracy", f"{row['Accuracy']:.2%}")
    col2.metric("F1_score", f"{row['F1_score']:.2%}")
    col3.metric("Accuracy Gap", f"{row['Gap']:.2%}")
    st.markdown("---")


st.subheader("📄 Rapport de classification")
st.dataframe(report_df.style.format("{:.2f}"))



st.subheader(" Matrice de confusion - Heatmap")

cm_numeric = cm_df.apply(pd.to_numeric, errors='coerce')


fig, ax = plt.subplots(figsize=(6,5))
sns.heatmap(cm_numeric, annot=True, fmt="d", cmap="Reds", 
            xticklabels=cm_df.columns, yticklabels=cm_df.index, ax=ax)
ax.set_xlabel("Predicted")
ax.set_ylabel("Actual")
st.pyplot(fig)



# st.dataframe(cm_df)
