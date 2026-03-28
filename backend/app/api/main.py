from app.api.routes import bert_views, reviews
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(reviews.router)
api_router.include_router(bert_views.router)
