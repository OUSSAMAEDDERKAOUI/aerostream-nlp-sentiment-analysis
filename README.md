<div align="center">

<h1>✈️ AeroStream</h1>
<h3>Real-Time NLP Sentiment Analysis Pipeline for Airline Customer Reviews</h3>

<p>
  <a href="#"><img src="https://img.shields.io/badge/Python-3.10%20%7C%203.11-3776AB?style=for-the-badge&logo=python&logoColor=white" /></a>
  <a href="#"><img src="https://img.shields.io/badge/PyTorch-2.x-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white" /></a>
  <a href="#"><img src="https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white" /></a>
  <a href="#"><img src="https://img.shields.io/badge/Apache%20Airflow-2.9.0-017CEE?style=for-the-badge&logo=apacheairflow&logoColor=white" /></a>
  <a href="#"><img src="https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" /></a>
  <a href="#"><img src="https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white" /></a>
  <a href="#"><img src="https://img.shields.io/badge/ChromaDB-1.3.7-FF6B35?style=for-the-badge" /></a>
  <a href="#"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" /></a>
</p>

<p>
  <strong>AeroStream</strong> is an end-to-end MLOps platform that combines a batch training pipeline with a live micro-batch streaming pipeline to automatically classify airline customer tweets into <code>positive</code>, <code>neutral</code>, and <code>negative</code> sentiments — all visualized in a real-time interactive dashboard.
</p>

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [Batch Pipeline](#-batch-pipeline)
- [Streaming Pipeline](#-streaming-pipeline)
- [API Reference](#-api-reference)
- [Dashboard](#-dashboard)
- [Model Performance](#-model-performance)
- [Configuration](#️-configuration)
- [Contributing](#-contributing)

---

## 🔍 Overview

AeroStream addresses the need to **automatically monitor airline brand sentiment** at scale. The system is split into two fully decoupled pipelines:

| Pipeline | Description |
|---|---|
| **Batch** | Offline training: loads the [US Airline Sentiment dataset](https://huggingface.co/datasets), cleans text, generates high-dimensional embeddings, stores them in ChromaDB, and trains multiple ML/DL classifiers. |
| **Streaming** | Online inference: an Airflow DAG polls a fake-tweet producer API every minute, routes tweets through a FastAPI inference endpoint, stores predictions in PostgreSQL, and updates a live Streamlit dashboard. |

**Key highlights:**
- State-of-the-art embeddings via `intfloat/e5-large-v2` (Sentence Transformers)
- Vector store powered by **ChromaDB** for efficient similarity retrieval
- Micro-batch streaming orchestrated by **Apache Airflow** (1-minute schedule)
- REST inference API serving a **Logistic Regression** model over dense embeddings
- Interactive dashboard with KPIs, sentiment breakdowns, and drill-downs per airline

---

## 🏗️ Architecture

### Full System Architecture

```mermaid
flowchart TD
    subgraph BATCH["🗂️ Batch Pipeline"]
        A[("🤗 HuggingFace\nUS Airline Dataset")] --> B[Load & EDA]
        B --> C[Text Cleaning\n& Normalization]
        C --> D["Sentence Transformers\nintfloat/e5-large-v2"]
        D --> E[("🗄️ ChromaDB\nVector Store")]
        E --> F["ML Training\nLogReg · SVC · KNN"]
        E --> G["DL Training\nCNN · PyTorch Classifier"]
        F --> H[("💾 Model Registry\n.joblib / .pt")]
        G --> H
    end

    subgraph STREAMING["⚡ Streaming Pipeline"]
        I["🐦 Fake Tweet\nProducer API\n(FastAPI :8000)"] -->|GET /batch| J
        J["⏱️ Airflow DAG\naerostream_streaming_pipeline\n(every 1 min)"] -->|POST /predict| K
        K["🧠 Inference API\n(FastAPI :8002)"] -->|Sentiment Labels| L
        L[("🐘 PostgreSQL\nstreaming_db.tweets")] --> M
        M["📊 Streamlit\nDashboard :8501"]
    end

    H -->|Loads Model| K
    E -.->|Embeddings| K
```

### Inference Flow

```mermaid
sequenceDiagram
    participant DAG as Airflow DAG
    participant PROD as Producer API
    participant INFER as Inference API
    participant DB as PostgreSQL
    participant DASH as Streamlit

    DAG->>PROD: GET /batch?batch_size=20
    PROD-->>DAG: 20 synthetic tweets (JSON)
    DAG->>INFER: POST /predict { texts: [...] }
    Note over INFER: clean text → embed (e5-large-v2)<br/>→ LogReg.predict()
    INFER-->>DAG: { results: [{text, sentiment}] }
    DAG->>DB: INSERT INTO tweets (...)
    DASH->>DB: SELECT * FROM tweets (every 60s)
    DASH-->>DASH: Re-render KPIs & charts
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Embeddings** | [Sentence Transformers `intfloat/e5-large-v2`](https://huggingface.co/intfloat/e5-large-v2) |
| **ML Models** | Scikit-learn (Logistic Regression, SVC, KNN) |
| **DL Models** | PyTorch (CNN, custom classifier) |
| **Vector Store** | ChromaDB 1.3.7 |
| **Inference API** | FastAPI + Uvicorn |
| **Tweet Producer** | FastAPI + Faker |
| **Orchestration** | Apache Airflow 2.9.0 |
| **Database** | PostgreSQL 13 (via SQLAlchemy) |
| **Dashboard** | Streamlit + Plotly + Seaborn |
| **Containerization** | Docker + Docker Compose |
| **Experimentation** | JupyterLab |

---

## 📁 Project Structure

```
aerostream-nlp-sentiment-analysis/
│
├── 📂 src/
│   ├── 📂 batch/               # Offline pipeline modules
│   │   ├── load_data.py        # Dataset loading from HuggingFace
│   │   ├── preprocess.py       # Text cleaning & normalization
│   │   ├── embeddings.py       # Sentence Transformer embedding generation
│   │   ├── train_model.py      # ML/DL model training
│   │   └── evaluate_model.py   # Metrics, confusion matrix, ROC
│   │
│   ├── 📂 streaming/           # Real-time inference services
│   │   ├── fastapi_tweet.py    # Producer API — generates synthetic tweets
│   │   └── api.py              # Inference API — predicts sentiment
│   │
│   └── 📂 utils/
│       ├── config.py           # Centralized configuration
│       ├── text_utils.py       # Shared text cleaning utilities
│       └── chroma_client.py    # ChromaDB connection helpers
│
├── 📂 airflow/
│   └── dags/
│       └── streaming_tweets_dag.py   # Airflow DAG (1-min micro-batch)
│
├── 📂 dashboard/               # Streamlit multi-page app
│   ├── streamlit_app.py        # Home / project overview
│   └── pages/
│       ├── 1_ModelMetrics.py   # Accuracy, F1, confusion matrix, ROC
│       ├── 2_DataStreaming.py  # Live KPIs, charts & sentiment breakdown
│       └── 03_A_Propos.py     # About page
│
├── 📂 notebooks/               # Step-by-step experimental notebooks
│   ├── 01_load_data.ipynb
│   ├── 02_eda.ipynb
│   ├── 03_text_cleaning.ipynb
│   ├── 04_embeddings.ipynb
│   ├── 05_model_ML_training.ipynb
│   ├── 06_LogisticRegression_GridSearch.ipynb
│   └── 07_model_DL_training.ipynb
│
├── 📂 models/                  # Persisted model artifacts
│   ├── LogisticRegression_model.joblib
│   ├── svc_model.joblib
│   ├── knn_model.joblib
│   ├── best_cnn_aerostream.pt
│   └── best_sentiment_classifier.pt
│
├── 📂 data/
│   ├── raw/                    # Original dataset
│   ├── processed/              # Cleaned CSV
│   ├── embeddings/             # Precomputed .npy vectors
│   ├── metadata/               # Train/test metadata CSVs
│   └── chroma_db/              # Persisted ChromaDB collections
│
├── Dockerfile                  # Airflow + src image
├── Dockerfile.api              # FastAPI services image
├── docker-compose.yml          # Full stack orchestration
├── requirements.txt            # Airflow/training deps
└── requirements-api.txt        # API-only deps
```

---

## 🚀 Quick Start

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) ≥ 24.x
- [Docker Compose](https://docs.docker.com/compose/) ≥ 2.x
- (Optional) NVIDIA GPU + [nvidia-container-toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html) for DL training

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/aerostream-nlp-sentiment-analysis.git
cd aerostream-nlp-sentiment-analysis
```

### 2. Configure environment variables

```bash
cp .env.example .env
# Edit .env with your credentials if needed
```

### 3. Launch the full stack

```bash
docker compose up --build
```

This starts:
| Service | URL |
|---|---|
| Airflow Webserver | http://localhost:8080 (admin / admin) |
| Producer API | http://localhost:8000/docs |
| Inference API | http://localhost:8002/docs |
| Streamlit Dashboard | http://localhost:8501 |
| JupyterLab | http://localhost:8888 (token: `admin`) |
| ChromaDB | http://localhost:8000 (internal) |

### 4. Run the batch pipeline (notebooks)

```bash
# Inside the running JupyterLab container at localhost:8888
# Open and run notebooks in order: 01 → 02 → ... → 07
```

### 5. Trigger the streaming DAG

Navigate to the Airflow UI → DAGs → `aerostream_streaming_pipeline` → Enable

The DAG runs automatically every minute, fetching tweets, running inference, and persisting results to PostgreSQL.

---

## 🗂️ Batch Pipeline

The batch pipeline follows a standard ML workflow, executed step-by-step through Jupyter notebooks:

```
Raw Data  →  EDA  →  Cleaning  →  Embeddings  →  ChromaDB  →  Training  →  Evaluation  →  Export
```

### Step-by-step

**1. Load Data (`01_load_data.ipynb`)**
```python
# Dataset: US Airline Sentiment — ~14,000 tweets
# Source: HuggingFace Datasets
from datasets import load_dataset
dataset = load_dataset("carblacac/twitter-sentiment-analysis")
```

**2. Text Cleaning (`03_text_cleaning.ipynb`)**
```python
import re

def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)   # remove URLs
    text = re.sub(r"@\w+", "", text)              # remove mentions
    text = re.sub(r"#\w+", "", text)              # remove hashtags
    text = re.sub(r"[^a-zA-Z\s]", "", text)       # keep letters only
    return re.sub(r"\s+", " ", text).strip()
```

**3. Generate Embeddings (`04_embeddings.ipynb`)**
```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("intfloat/e5-large-v2")
embeddings = model.encode(
    texts,
    convert_to_numpy=True,
    normalize_embeddings=True,  # unit vector for cosine similarity
    batch_size=64,
    show_progress_bar=True
)
# Shape: (N, 1024)
```

**4. Store in ChromaDB (`04_embeddings.ipynb`)**
```python
import chromadb

client = chromadb.PersistentClient(path="data/chroma_db")
collection = client.get_or_create_collection("train_embeddings")
collection.add(
    embeddings=embeddings.tolist(),
    documents=texts,
    ids=[str(i) for i in range(len(texts))]
)
```

**5. Train & Evaluate (`05_model_ML_training.ipynb` / `07_model_DL_training.ipynb`)**
```python
from sklearn.linear_model import LogisticRegression
import joblib

clf = LogisticRegression(max_iter=1000, C=1.0)
clf.fit(X_train, y_train)
joblib.dump(clf, "models/LogisticRegression_model.joblib")
```

---

## ⚡ Streaming Pipeline

The streaming system simulates a real-time airline social media monitoring service.

### Airflow DAG — `aerostream_streaming_pipeline`

| Task | Description |
|---|---|
| `fetch_tweets` | Calls `GET /batch?batch_size=20` on the Producer API |
| `process_tweets` | Sends raw tweet texts to `POST /predict` for sentiment labels |
| `store_to_postgres` | Inserts enriched records (airline, text, sentiment, reason, timestamp) into PostgreSQL |

**Schedule:** Every 1 minute (`*/1 * * * *`)  
**Retry policy:** 4 retries with a 30-second delay

```python
# Example processed record
{
    "airline": "United",
    "text": "united flight delayed 4 hours with no updates terrible communication",
    "sentiment": "negative",
    "negativereason": "Late Flight",
    "tweet_created": "2025-12-18T16:24:00+00:00"
}
```

---

## 📡 API Reference

### Producer API — `FastAPI :8000`

> Generates realistic synthetic airline tweets using weighted random sampling.

```http
GET /batch?batch_size=20
```

**Response:**
```json
[
  {
    "airline_sentiment_confidence": 0.872,
    "airline": "Delta",
    "negativereason": null,
    "tweet_created": "2025-12-18T16:24:00.123456+00:00",
    "text": "@Delta Great service today — flight was on time and crew was amazing! ✈️👏"
  }
]
```

---

### Inference API — `FastAPI :8002`

> Cleans text, generates e5-large-v2 embeddings on-the-fly, and returns sentiment predictions.

```http
POST /predict
Content-Type: application/json

{
  "texts": [
    "@united why are your fares three times more than other carriers???",
    "@Delta Smooth flight — love the new seats!"
  ]
}
```

**Response:**
```json
{
  "count": 2,
  "results": [
    { "text": "united why are your fares three times more than other carriers", "sentiment": "negative" },
    { "text": "delta smooth flight love the new seats", "sentiment": "positive" }
  ]
}
```

**Try it with `curl`:**
```bash
curl -X POST http://localhost:8002/predict \
  -H "Content-Type: application/json" \
  -d '{"texts": ["Great flight with Delta today!", "United lost my bags again."]}'
```

---

## 📊 Dashboard

The Streamlit dashboard (`localhost:8501`) has three pages:

### Page 1 — Model Metrics
- Accuracy, F1-Score, Accuracy Gap (train vs. test)
- Full classification report per class (positive / neutral / negative)
- Confusion matrix heatmap

### Page 2 — Live Data Streaming
Auto-refreshes every 60 seconds. Shows:

| KPI | Description |
|---|---|
| Total Tweets | Running count of processed tweets |
| Airlines Covered | Number of distinct airlines in the stream |
| % Negative Tweets | Share of negative sentiment in stream |

Charts:
- Sentiment distribution per airline (grouped bar)
- Tweet volume per airline (color-scaled bar)
- Top 10 causes of negative tweets (bar chart)
- Sentiment pie chart (global or per airline)

### Page 3 — About
Project context, objectives, and pipeline documentation.

---

## 📈 Model Performance

Models are trained on the **US Airline Sentiment** dataset (~14,000 tweets, 3 classes).

| Model | Accuracy | F1-Score (Macro) | Notes |
|---|---|---|---|
| Logistic Regression | **~85%** | **~83%** | Best speed/accuracy trade-off; used in production |
| SVC (RBF kernel) | ~84% | ~82% | Slower inference |
| KNN | ~78% | ~75% | Baseline |
| CNN (PyTorch) | ~86% | ~84% | Best accuracy |
| DL Classifier (PyTorch) | ~85% | ~83% | GPU-accelerated |

> All models operate on **1024-dimensional embeddings** from `intfloat/e5-large-v2`.

**Confusion Matrix (Logistic Regression):**
```
                Predicted
                neg   neu   pos
Actual  neg  [ 1872   84   41 ]
        neu  [  183  412   89 ]
        pos  [   52   62  387 ]
```

---

## ⚙️ Configuration

Key constants in `src/utils/config.py` and environment variables:

| Variable | Default | Description |
|---|---|---|
| `PRODUCER_API_URL` | `http://producer_api:8000/batch` | Fake tweet generator endpoint |
| `PROCESSING_API_URL` | `http://processing_api:8002/predict` | Inference endpoint |
| `POSTGRES_CONFIG` | `postgresql+psycopg2://airflow:airflow@postgres:5432/streaming_db` | PostgreSQL connection string |
| `MODEL_PATH` | `models/LogisticRegression_model.joblib` | Path to the production model |
| `EMBEDDING_MODEL` | `intfloat/e5-large-v2` | HuggingFace embedding model |

---

## 🧪 Running Tests & Notebooks Locally (without Docker)

```bash
# Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Linux/macOS

# Install dependencies
pip install -r requirements.txt

# Launch JupyterLab
jupyter lab --notebook-dir=notebooks/

# Start the inference API
uvicorn src.streaming.api:app --host 0.0.0.0 --port 8002 --reload

# Start the producer API
uvicorn src.streaming.fastapi_tweet:app --host 0.0.0.0 --port 8000 --reload

# Launch the dashboard (point it at a running PostgreSQL instance)
streamlit run dashboard/streamlit_app.py
```

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m "feat: add my feature"`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a Pull Request

Please follow [Conventional Commits](https://www.conventionalcommits.org/).

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <sub>Built with ❤️ using FastAPI · Apache Airflow · Sentence Transformers · ChromaDB · Streamlit · PyTorch</sub>
</div>
