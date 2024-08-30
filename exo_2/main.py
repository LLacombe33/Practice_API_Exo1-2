from fastapi import FastAPI, File, UploadFile, HTTPException
from typing import List
import pandas as pd
import io
import joblib

app = FastAPI()

model = joblib.load("logistic_regression_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")


@app.post("/predict-text/")
async def predict_sentiment_text(text: str):
    text_vector = vectorizer.transform([text])
    prediction = model.predict(text_vector)
    sentiment = "Positive" if prediction[0] == 1 else "Negative"
    return {"text": text, "sentiment": sentiment}


@app.post("/predict-file/")
async def predict_sentiment_file(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")

    content = await file.read()
    df = pd.read_csv(io.StringIO(content.decode('utf-8')))

    if 'text' not in df.columns:
        raise HTTPException(status_code=400, detail="CSV must contain a 'text' column")

    texts = df['text'].tolist()
    text_vectors = vectorizer.transform(texts)
    predictions = model.predict(text_vectors)
    sentiments = ["Positive" if pred == 1 else "Negative" for pred in predictions]

    df['sentiment'] = sentiments
    return df.to_dict(orient='records')
