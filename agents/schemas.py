from typing import List, Optional
from pydantic import BaseModel, Field

class Movie(BaseModel):
    title: str = Field(description="Название фильма")
    year: Optional[str] = Field(default=None, description="Год выхода, если указан")

class MovieList(BaseModel):
    movies: List[Movie] = Field(description="Список найденных фильмов-новинок")

class ReviewAnalysis(BaseModel):
    movie_title: str = Field(description="Название фильма")
    review_summary: str = Field(description="Краткое содержание рецензии")
    pros: List[str] = Field(default_factory=list, description="Что понравилось (плюсы)")
    cons: List[str] = Field(default_factory=list, description="Что не понравилось (минусы)")
    rating: Optional[float] = Field(default=None, description="Оценка, если есть (от 1 до 10)")
    source_url: str = Field(description="Ссылка на рецензию")