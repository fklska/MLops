from app.api.schemas.reviews import ReviewRequest, ReviewResponse, ReviewUpdate
from app.core.db import Session
from app.crud.reviews import (
    create_db_reviews,
    delete_db_review,
    get_db_reviews,
    get_review_by_id,
    replace_db_review,
    update_db_review,
)
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.get("/")
async def get_reviews(session: Session) -> ReviewResponse:
    reviews = await get_db_reviews(session)
    return {"reviews": reviews}


@router.post("/")
async def create_review(session: Session, request: ReviewRequest) -> ReviewResponse:
    review = await create_db_reviews(session, request)
    # TODO Отправить отзыв в воркер
    return {"reviews": [review]}


@router.get("/{review_id}")
async def get_review(review_id: int, session: Session) -> ReviewResponse:
    review = await get_review_by_id(session, review_id)
    if review:
        return {"reviews": [review]}

    raise HTTPException(status_code=404, detail="Нет такого отзыва")


@router.put("/{review_id}")
async def replace_review(review_id: int, session: Session, request: ReviewRequest) -> ReviewResponse:
    review = await replace_db_review(session, review_id, request)
    if review:
        return {"reviews": [review], "details": "Заменено"}

    raise HTTPException(status_code=404, detail="Нет такого отзыва")


@router.patch("/{review_id}")
async def edit_review(review_id: int, session: Session, request: ReviewUpdate) -> ReviewResponse:
    review = await update_db_review(session, review_id, request)
    if review:
        return {"reviews": [review], "details": "Обновлено"}

    raise HTTPException(status_code=404, detail="Нет такого отзыва")


@router.delete("/{review_id}")
async def delete_review(review_id: int, session: Session) -> ReviewResponse:
    review = await delete_db_review(session, review_id)

    if review:
        return {"reviews": [review], "details": "Удалено"}

    raise HTTPException(status_code=404, detail="Нет такого отзыва")
