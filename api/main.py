"""
FastAPI сервис для инференса модели классификации тональности.
Эндпоинты:
- POST /predict: предсказание тональности отзыва
- GET /health: проверка работоспособности
"""
import os
import torch
import torch.nn.functional as F
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Конфигурация
MODEL_PATH = "models/bert/saved_model"

# Инициализация приложения
app = FastAPI(
    title="IMDB Sentiment API",
    description="API для определения тональности отзывов (positive/negative)",
    version="1.0.0"
)

# Глобальные объекты модели и токенизатора
tokenizer = None
model = None
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class ReviewRequest(BaseModel):
    """Модель запроса"""
    text: str = Field(..., min_length=1, max_length=5000, example="This movie was amazing!")

class SentimentResponse(BaseModel):
    """Модель ответа"""
    sentiment: str = Field(..., description="positive или negative")
    confidence: dict = Field(..., description="вероятности [negative, positive]")

class HealthResponse(BaseModel):
    """Ответ на health check"""
    status: str
    model_loaded: bool
    device: str

@app.on_event("startup")
async def load_model():
    """Загрузка модели при старте сервера"""
    global tokenizer, model
    logger.info(f"Загрузка модели из {MODEL_PATH}")
    try:
        tokenizer = DistilBertTokenizer.from_pretrained(MODEL_PATH)
        model = DistilBertForSequenceClassification.from_pretrained(MODEL_PATH)
        model.to(device)
        model.eval()
        logger.info(f"Модель загружена на устройство: {device}")
    except Exception as e:
        logger.error(f"Ошибка загрузки модели: {e}")
        raise

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Проверка работоспособности сервиса"""
    return HealthResponse(
        status="ok",
        model_loaded=model is not None,
        device=str(device)
    )

@app.post("/predict", response_model=SentimentResponse)
async def predict(request: ReviewRequest):
    """Предсказание тональности отзыва"""
    if model is None or tokenizer is None:
        raise HTTPException(status_code=503, detail="Модель не загружена")

    # Токенизация
    inputs = tokenizer(
        request.text,
        truncation=True,
        padding=True,
        max_length=256,
        return_tensors="pt"
    ).to(device)

    # Инференс
    with torch.no_grad():
        outputs = model(**inputs)
        probs = F.softmax(outputs.logits, dim=-1)
        pred_class = torch.argmax(probs, dim=-1).item()

    sentiment = "positive" if pred_class == 1 else "negative"
    confidence = {
        "negative": float(probs[0][0]),
        "positive": float(probs[0][1])
    }

    logger.info(f"Prediction: {sentiment} (conf: {confidence})")
    return SentimentResponse(sentiment=sentiment, confidence=confidence)

@app.get("/")
async def root():
    """Корневой эндпоинт"""
    return {
        "message": "IMDB Sentiment API",
        "docs": "/docs",
        "health": "/health"
    }