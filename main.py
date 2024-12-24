from fastapi import FastAPI
from fastapi.responses import FileResponse
import pickle
from pydantic import BaseModel
import os

# Charger le modèle et le vectorizer
with open("final_model.pkl", "rb") as f:
    model = pickle.load(f)
with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

app = FastAPI()

class TextInput(BaseModel):
    text: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}

@app.get("/favicon.ico")
def get_favicon():
    return FileResponse(os.path.join(os.getcwd(), "favicon.ico"))

@app.post("/predict")
def predict_age_group(input: TextInput):
    text_cleaned = input.text
    text_vectorized = vectorizer.transform([text_cleaned])
    prediction = model.predict(text_vectorized)
    return {"age_group": prediction[0]}
