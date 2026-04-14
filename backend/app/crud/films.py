from app.api.schemas.films import FilmRequest, FilmUpdate
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from ..core.db import Session
from ..core.models import Films


async def get_db_films(session: Session):
    result = await session.execute(select(Films).options(selectinload(Films.reviews)))
    return result.scalars().all()


async def create_db_film(session: Session, film: FilmRequest):
    new_film = Films(**film.model_dump())
    session.add(new_film)
    await session.commit()
    await session.refresh(new_film)
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
