from typing import List

from pydantic import BaseModel, ConfigDict


class ReviewBase(BaseModel):
    title: str
    description: str
    film_id: int


class ReviewRequest(ReviewBase):
    pass


class Review(ReviewBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ReviewResponse(BaseModel):
    reviews: List[Review]


class FilmBase(BaseModel):
    title: str
    year: int
    description: str


class FilmRequest(FilmBase):
    pass


class Film(FilmBase):
    id: int
    reviews: List[Review]

    model_config = ConfigDict(from_attributes=True)


class FilmResponse(BaseModel):
    films: List[Film]
