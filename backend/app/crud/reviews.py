from app.api.schemas.reviews import ReviewRequest, ReviewUpdate
from app.crud.films import get_db_film_by_id
from fastapi import HTTPException
from sqlalchemy import select

from ..core.db import Session
from ..core.models import Reviews


async def get_db_reviews(session: Session):
    result = await session.execute(select(Reviews))
    return result.scalars().all()


async def create_db_reviews(session: Session, review: ReviewRequest):
    film = await get_db_film_by_id(session, review.film_id)
    if not film:
        raise HTTPException(404, "Нет такого фильма")

    exist = await get_review_by_title(session, review.title, review.film_id)
    if exist:
        raise HTTPException(400, "Ревью с таким названием уже существует")

    new_review = Reviews(**review.model_dump())
    session.add(new_review)
    await session.commit()
    await session.refresh(new_review)
    return new_review


async def get_review_by_id(session: Session, review_id: int):
    return await session.get(Reviews, review_id)


async def get_review_by_title(session: Session, review_title: int, film_id: int):
    result = await session.execute(select(Reviews).where(Reviews.film_id == film_id, Reviews.title == review_title))
    return result.scalar_one_or_none()


async def replace_db_review(session: Session, review_id: int, review_in: ReviewRequest):
    db_review = await get_review_by_id(session, review_id)
    if db_review:

        update_data = review_in.model_dump()
        for key, value in update_data.items():
            setattr(db_review, key, value)

        await session.commit()
        await session.refresh(db_review)
    return db_review


async def update_db_review(session: Session, review_id: int, review_in: ReviewUpdate):
    db_review = await get_review_by_id(session, review_id)

    if db_review:
        update_data = review_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_review, key, value)

        await session.commit()
        await session.refresh(db_review)

    return db_review


async def delete_db_review(session: Session, review_id: int):
    db_review = await get_review_by_id(session, review_id)
    if db_review:
        await session.delete(db_review)
        await session.commit()
    return db_review
