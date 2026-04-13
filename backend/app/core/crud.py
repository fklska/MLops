from app.api.schemas.schema import FilmRequest, ReviewRequest
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from .db import Session
from .models import Films, Reviews


async def get_db_reviews(session: Session):
    result = await session.execute(select(Reviews))
    return result.scalars().all()


async def create_db_reviews(session: Session, review: ReviewRequest):
    new_review = Reviews(**review.model_dump())
    session.add(new_review)
    await session.commit()
    await session.refresh(new_review)
    return new_review


async def get_db_films(session: Session):
    result = await session.execute(select(Films).options(selectinload(Films.reviews)))
    return result.scalars().all()


async def create_db_film(session: Session, film: FilmRequest):
    new_film = Films(**film.model_dump())
    session.add(new_film)
    await session.commit()
    await session.refresh(new_film)
    return new_film
