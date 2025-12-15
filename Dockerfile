# Image de base officielle Airflow 
FROM apache/airflow:2.9.0-python3.10

USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    git \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

COPY requirements.txt /requirements.txt

RUN pip install --no-cache-dir -r /requirements.txt


COPY --chown=airflow:root ./src /opt/airflow/src
COPY --chown=airflow:root ./dashboard /opt/airflow/dashboard

# Configuration du PYTHONPATH pour que Python trouve vos modules 'src'
ENV PYTHONPATH="${PYTHONPATH}:/opt/airflow"