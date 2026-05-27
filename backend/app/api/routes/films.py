from app.api.schemas.films import FilmRequest, FilmResponse, FilmUpdate, NewFilmResponse
from app.core.db import Session
from app.crud.films import (
    create_db_film,
    delete_db_film,
    get_db_film_by_id,
    get_db_films,
    replace_db_film,
    update_db_film,
)
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/films", tags=["films"])


@router.get("/")
async def get_films(session: Session) -> FilmResponse:
    films = await get_db_films(session)
    return FilmResponse(films=films)


@router.post("/")
async def create_film(session: Session, request: FilmRequest) -> NewFilmResponse:
    film = await create_db_film(session, request)
    return NewFilmResponse(films=[film])


@router.get("/{film_id}")
async def get_film(film_id: int, session: Session) -> FilmResponse:
    film = await get_db_film_by_id(session, film_id)
    if film:
        return FilmResponse(films=[film])

    raise HTTPException(status_code=404, detail="Нет такого фильма")


@router.put("/{film_id}")
async def replace_film(film_id: int, session: Session, request: FilmRequest) -> FilmResponse:
    film = await replace_db_film(session, film_id, request)
    if film:
        return FilmResponse(films=[film], details="Заменено")

    raise HTTPException(status_code=404, detail="Нет такого фильма")


@router.patch("/{film_id}")
async def edit_film(film_id: int, session: Session, request: FilmUpdate) -> FilmResponse:
    film = await update_db_film(session, film_id, request)
    if film:
        return FilmResponse(films=[film], details="Обновлено")

    raise HTTPException(status_code=404, detail="Нет такого фильма")


@router.delete("/{film_id}")
async def delete_film(film_id: int, session: Session) -> FilmResponse:
    result = await delete_db_film(session, film_id)

    if result > 0:
        return FilmResponse(films=[], details=f"Удалено {result}")

    raise HTTPException(status_code=404, detail="Нет такого фильма")
