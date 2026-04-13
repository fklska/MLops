from app.api.schemas.schema import FilmRequest, FilmResponse
from app.core.crud import create_db_film, get_db_films
from app.core.db import Session
from fastapi import APIRouter

router = APIRouter(prefix="/films", tags=["films"])


@router.get("/")
async def get_films(session: Session) -> FilmResponse:
    films = await get_db_films(session)
    return {"films": films}


@router.post("/")
async def create_film(session: Session, request: FilmRequest) -> FilmResponse:
    film = await create_db_film(session, request)
    return {"films": [film]}
