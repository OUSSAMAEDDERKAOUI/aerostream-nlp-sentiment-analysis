from fastapi import FastAPI, Request
import joblib as jb
import os
import re
import pandas as pd
from sentence_transformers import SentenceTransformer
from pathlib import Path


app = FastAPI()

MODEL_PATH = Path("models/LogisticRegression_model.joblib")

log_reg = jb.load(MODEL_PATH)


embedding_model =  SentenceTransformer('intfloat/e5-large-v2')

def clean_text(text):
    if text is None:
        return None

    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"#\w+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text if text else None

@app.post("/predict")
async def predict(request: Request):
   
    data = await request.json()
    texts = data.get("texts")

    df = pd.DataFrame(texts, columns=["text"])

    df["text"] = df["text"].apply(clean_text)

    if df.empty:
        return {"error": "No valid text after cleaning"}

    embeddings = embedding_model.encode(
        df["text"].tolist(),
        convert_to_numpy=True,
        normalize_embeddings=True
    )



    predictions = log_reg.predict(embeddings)

    results = []
    for text, pred in zip(df["text"], predictions):
        results.append({
            "text": text,
            "sentiment": str(pred)
        })

    return {
        "count": len(results),
        "results": results
    }
