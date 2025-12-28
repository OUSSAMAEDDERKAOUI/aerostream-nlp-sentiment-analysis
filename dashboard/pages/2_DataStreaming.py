
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from streamlit_autorefresh import st_autorefresh
import plotly.express as px


DB_USER = "airflow"
DB_PASSWORD = "airflow"
DB_HOST = "postgres"  
DB_PORT = "5432"
DB_NAME = "streaming_db"

engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")


st.title("Dashboard Sentiment Analyse - Avis Clients Airlines")


st_autorefresh(interval=60*1000, key="data_refresh")


@st.cache_data(ttl=60)
def load_data():
    query = "SELECT * FROM tweets;"
    df = pd.read_sql(query, engine)
    return df

df = load_data()




st.subheader("Indicateurs clés")
total_tweets = len(df)
total_companies = df['airline'].nunique()
negative_percentage = round(len(df[df['sentiment']=='negative']) / total_tweets * 100, 2)

col1, col2, col3 = st.columns(3)
col1.metric("Nombre total de tweets", total_tweets)
col2.metric("Nombre de compagnies aériennes", total_companies)
col3.metric("Pourcentage de tweets négatifs", f"{negative_percentage}%")


st.subheader("Aperçu des données")
st.dataframe(df.head())



#
st.subheader("Répartition des sentiments par compagnie")
sentiment_by_airline = df.groupby(['airline', 'sentiment']).size().reset_index(name='count')
st.dataframe(sentiment_by_airline.head())



col1, col2 = st.columns(2)

with col1:

    
    fig1 = px.bar(sentiment_by_airline,
                  x='airline',
                  y='count',
                  color='sentiment',
                  barmode='group',
                  title="Répartition des sentiments par compagnie")
    st.plotly_chart(fig1)

with col2:
    tweets_count = df['airline'].value_counts().reset_index()
    tweets_count.columns = ['airline', 'count']
    
    fig2 = px.bar(tweets_count,
                  x='airline',
                  y='count',
                  text='count',
                  color='count',
                  color_continuous_scale='Blues',
                  title="Volume de tweets par compagnie")
    fig2.update_layout(xaxis_title="Compagnie aérienne", yaxis_title="Nombre de tweets")
    st.plotly_chart(fig2)


col3, col4 = st.columns(2)

with col3:
    st.subheader("Principales causes des tweets négatifs")
    if 'negativereason' in df.columns:
        top_reasons = df[df['sentiment']=='negative']['negativereason'].value_counts().head(10)
        st.bar_chart(top_reasons)
    else:
        st.info("La colonne 'negativereason' n'existe pas dans la table.")

with col4:
    selected_airline = st.selectbox(
        "Sélectionner une compagnie",
        ["Toutes"] + df['airline'].unique().tolist()
    )

    sentiment_by_airline = df.groupby(['airline', 'sentiment']).size().reset_index(name='count')

    if selected_airline != "Toutes":
        data_pie = sentiment_by_airline[sentiment_by_airline['airline'] == selected_airline]
        fig4 = px.pie(data_pie, names='sentiment', values='count',
                      title=f"Répartition des sentiments pour {selected_airline}")
    else:
        total_sentiment = df['sentiment'].value_counts().reset_index()
        total_sentiment.columns = ['sentiment', 'count']
        fig4 = px.pie(total_sentiment, names='sentiment', values='count',
                      title="Répartition globale des sentiments")

    st.plotly_chart(fig4)
