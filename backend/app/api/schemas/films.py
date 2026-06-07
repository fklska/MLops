from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from .reviews import Review


class FilmBase(BaseModel):
    title: str
    year: int
    description: str


class FilmRequest(FilmBase):
    pass


class FilmUpdate(BaseModel):
    title: Optional[str] = None
    year: Optional[int] = None
    description: Optional[str] = None


class Film(FilmBase):
    id: int
    reviews: Optional[List[Review]] = None

    model_config = ConfigDict(from_attributes=True)


class NewFilm(FilmBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class NewFilmResponse(BaseModel):
    films: List[NewFilm]
    details: Optional[str] = None


class FilmResponse(BaseModel):
    films: List[Film]
    details: Optional[str] = None
