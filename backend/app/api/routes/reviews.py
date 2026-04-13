from app.api.schemas.schema import ReviewRequest, ReviewResponse
from app.core.crud import create_db_reviews, get_db_reviews
from app.core.db import Session
from fastapi import APIRouter

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.get("/")
async def get_reviews(session: Session) -> ReviewResponse:
    reviews = await get_db_reviews(session)
    return {"reviews": reviews}


@router.post("/")
async def create_review(session: Session, request: ReviewRequest) -> ReviewResponse:
    review = await create_db_reviews(session, request)
    return {"reviews": [review]}


@router.get("/{review_id}")
async def get_review(review_id: int, session: Session) -> ReviewResponse:
    pass


@router.put("/{review_id}")
async def replace_review(review_id: int, session: Session) -> ReviewResponse:
    pass


@router.patch("/{review_id}")
async def edit_review(review_id: int, session: Session) -> ReviewResponse:
    pass


@router.delete("/{review_id}")
async def delete_review(review_id: int, session: Session) -> ReviewResponse:
    pass
