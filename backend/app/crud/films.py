from app.api.schemas.films import FilmRequest, FilmUpdate
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from ..core.db import Session
from ..core.models import Films


async def get_db_films(session: Session):
    result = await session.execute(select(Films).options(selectinload(Films.reviews)))
    films = result.scalars().all()
    session.expunge_all()
    return films


async def create_db_film(session: Session, film: FilmRequest):
    film_exists = (await session.execute(select(Films).where(Films.title == film.title))).scalar_one_or_none()
    if film_exists:
        raise HTTPException(400, "Фильм с таким названием уже существует")

    new_film = Films(**film.model_dump())
    session.add(new_film)
    await session.commit()
    return new_film


async def get_db_film_by_id(session: Session, film_id: int):
    return await session.get(Films, film_id, options=[selectinload(Films.reviews)])


async def replace_db_film(session: Session, film_id: int, film_in: FilmRequest):
    db_film = await get_db_film_by_id(session, film_id)
    if db_film:

        update_data = film_in.model_dump()
        for key, value in update_data.items():
            setattr(db_film, key, value)

        await session.commit()
        await session.refresh(db_film)

    return db_film


async def update_db_film(session: Session, film_id: int, film_in: FilmUpdate):
    db_film = await get_db_film_by_id(session, film_id)

    if db_film:
        update_data = film_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_film, key, value)

        await session.commit()
        await session.refresh(db_film)

    return db_film


async def delete_db_film(session: Session, film_in: int):
    db_film = await get_db_film_by_id(session, film_in)
    if db_film:
        await session.delete(db_film)
        await session.commit()
    return db_film
