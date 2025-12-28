from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
from sqlalchemy import create_engine,MetaData,Table,Column,Integer,String,TIMESTAMP
from sqlalchemy.dialects.postgresql import insert


PRODUCER_API_URL = "http://producer_api:8000/batch"
PROCESSING_API_URL = "http://processing_api:8002/predict"



POSTGRES_CONFIG = "postgresql+psycopg2://airflow:airflow@postgres:5432/streaming_db"



DEFAULT_ARGS = {
    "owner": "aerostream",
    "retries": 4,
    "retry_delay": timedelta(seconds=30),
}


def fetch_tweets(**context):

    response = requests.get(
        PRODUCER_API_URL,
        params={"batch_size": 20},
        timeout=10
    )
    response.raise_for_status()

    tweets = response.json()
    context["ti"].xcom_push(key="tweets", value=tweets)


def process_tweets(**context):

    tweets = context["ti"].xcom_pull(key="tweets")
    texts = [t["text"] for t in tweets]

    response = requests.post(
        PROCESSING_API_URL,
        json={"texts": texts},
        timeout=20
    )
    response.raise_for_status()

    predictions = response.json()["results"]

    processed = []
    for tweet, pred in zip(tweets, predictions):
        processed.append({
            "airline": tweet["airline"],
            "text": pred["text"],
            "sentiment":pred["sentiment"],
            "negativereason": tweet["negativereason"],
            "tweet_created": tweet["tweet_created"]
        })

    print(processed)
    context["ti"].xcom_push(key="processed", value=processed)


def store_to_postgres(**context):

    data = context["ti"].xcom_pull(key="processed")

    if not data:
        return
    
    engine=create_engine(POSTGRES_CONFIG)
    metadata=MetaData()


    tweets=Table(
        "tweets",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("airline", String),
        Column("text", String),
        Column("sentiment", String),
        Column("negativereason", String),
        Column("tweet_created", TIMESTAMP),
    )

    metadata.create_all(engine)


    rows=[
        {
            "airline": row["airline"],
            "text": row["text"],
            "sentiment": row["sentiment"],
            "negativereason": row["negativereason"],
            "tweet_created": row["tweet_created"]
        }
        for row in data
    ]

    with engine.begin() as conn:
        conn.execute(tweets.insert(),rows)



with DAG(
    dag_id="aerostream_streaming_pipeline",
    description="Micro-batch streaming ingestion pipeline",
    start_date=datetime(2025, 1, 1),
    schedule_interval="*/1 * * * *",  
    catchup=False,
    default_args=DEFAULT_ARGS,
    tags=["streaming", "airflow", "nlp"]
) as dag:

    fetch_task = PythonOperator(
        task_id="fetch_tweets",
        python_callable=fetch_tweets
    )

    process_task = PythonOperator(
        task_id="process_tweets",
        python_callable=process_tweets
    )

    store_task = PythonOperator(
        task_id="store_to_postgres",
        python_callable=store_to_postgres
    )

    fetch_task >> process_task >> store_task
