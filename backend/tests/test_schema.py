import pytest
from app.api.schemas.films import (
    FilmBase,
    FilmResponse,
    FilmUpdate,
    NewFilm,
    NewFilmResponse,
)
from app.api.schemas.reviews import (
    Review,
    ReviewResponse,
    ReviewUpdate,
)
from pydantic import ValidationError


class TestFilmBase:
    def test_valid(self):
        data = {"title": "Inception", "year": 2010, "description": "A dream within a dream"}
        obj = FilmBase(**data)
        assert obj.year == 2010

    def test_missing_title(self):
        data = {"year": 2010, "description": "desc"}
        with pytest.raises(ValidationError):
            FilmBase(**data)

    def test_missing_year(self):
        data = {"title": "Inception", "description": "desc"}
        with pytest.raises(ValidationError):
            FilmBase(**data)

    def test_missing_description(self):
        data = {"title": "Inception", "year": 2010}
        with pytest.raises(ValidationError):
            FilmBase(**data)

    def test_year_as_string(self):
        data = {"title": "Inception", "year": "2010", "description": "desc"}
        obj = FilmBase(**data)
        assert isinstance(obj.year, int)


class TestFilmUpdate:
    def test_empty_update(self):
        obj = FilmUpdate()
        assert obj.title is None

    def test_partial_update(self):
        obj = FilmUpdate(title="New Title")
        assert obj.title == "New Title"


class TestNewFilm:
    def test_from_orm(self):
        orm_obj = type("ORM", (), {"id": 10, "title": "New", "year": 2023, "description": "desc"})()
        obj = NewFilm.model_validate(orm_obj)
        assert obj.id == 10


class TestNewFilmResponse:
    def test_valid(self):
        films = [{"id": 1, "title": "Film", "year": 2020, "description": "desc"}]
        resp = NewFilmResponse(films=films)
        assert len(resp.films) == 1


class TestFilmResponse:
    def test_valid(self):
        films = [{"id": 1, "title": "Test", "year": 2020, "description": "desc"}]
        resp = FilmResponse(films=films)
        assert resp.films[0].id == 1


class TestReviewUpdate:
    def test_empty(self):
        obj = ReviewUpdate()
        assert obj.title is None

    def test_partial(self):
        obj = ReviewUpdate(title="Updated title")
        assert obj.title == "Updated title"


class TestReview:
    def test_from_orm(self):
        orm = type(
            "ORM",
            (),
            {
                "id": 1,
                "title": "Title",
                "description": "Desc",
                "film_id": 1,
                "status": "published",
                "label_id": 2,
                "label": "positive",
                "probability": 0.95,
            },
        )()
        rev = Review.model_validate(orm)
        assert rev.id == 1
        assert rev.label == "positive"


class TestReviewResponse:
    def test_valid(self):
        reviews = [{"id": 1, "title": "T", "description": "D", "film_id": 1, "status": "ok"}]
        resp = ReviewResponse(reviews=reviews)
        assert resp.reviews[0].id == 1
