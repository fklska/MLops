from app.core.db import Session
from fastapi import APIRouter

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.get("/")
async def get_reviews(session: Session):
    pass


@router.post("/")
async def create_review(session: Session):
    pass


@router.put("/{review_id}")
async def replace_review(review_id: int, session: Session):
    pass


@router.patch("/{review_id}")
async def edit_review(review_id: int, session: Session):
    pass


@router.get("/{review_id}")
async def get_review(review_id: int, session: Session):
    pass


@router.delete("/{review_id}")
async def delete_review(review_id: int, session: Session):
    pass
