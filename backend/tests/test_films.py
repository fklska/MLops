from unittest.mock import AsyncMock, patch

import pytest
from app.core.config import settings
from app.core.db import Session
from app.main import app
from fastapi.testclient import TestClient

PREFIX = settings.API_V1_STR


class MockAsyncSession:
    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass


client = TestClient(app)


@pytest.fixture
def mock_session():
    return MockAsyncSession()


@pytest.fixture(autouse=True)
def override_dependency(mock_session):
    app.dependency_overrides[Session] = lambda: mock_session
    yield
    app.dependency_overrides.clear()


def test_get_films_success(mock_session):
    mock_films = [{"id": 1, "title": "Test", "year": 2024, "description": "Desc", "reviews": None}]
    with patch("app.api.routes.films.get_db_films", AsyncMock(return_value=mock_films)):
        response = client.get(f"{PREFIX}/films/")
        assert response.status_code == 200
        assert response.json() == {"films": mock_films, "details": None}


def test_create_film_success(mock_session):
    film_data = {"title": "New Film", "year": 2024, "description": "A new film"}
    created_film = {"id": 2, "title": "New Film", "year": 2024, "description": "A new film"}  # без reviews
    with patch("app.api.routes.films.create_db_film", AsyncMock(return_value=created_film)):
        response = client.post(f"{PREFIX}/films/", json=film_data)
        assert response.status_code == 200
        assert response.json() == {"films": [created_film], "details": None}


def test_get_film_by_id_found(mock_session):
    film = {"id": 1, "title": "Test", "year": 2024, "description": "Desc", "reviews": None}
    with patch("app.api.routes.films.get_db_film_by_id", AsyncMock(return_value=film)):
        response = client.get(f"{PREFIX}/films/1")
        assert response.status_code == 200
        assert response.json() == {"films": [film], "details": None}


def test_get_film_by_id_not_found(mock_session):
    with patch("app.api.routes.films.get_db_film_by_id", AsyncMock(return_value=None)):
        response = client.get(f"{PREFIX}/films/99")
        assert response.status_code == 404
        assert response.json()["detail"] == "Нет такого фильма"


def test_replace_film_success(mock_session):
    film_data = {"title": "Replaced", "year": 2024, "description": "Replaced desc"}
    replaced_film = {"id": 1, "title": "Replaced", "year": 2024, "description": "Replaced desc", "reviews": None}
    with patch("app.api.routes.films.replace_db_film", AsyncMock(return_value=replaced_film)):
        response = client.put(f"{PREFIX}/films/1", json=film_data)
        assert response.status_code == 200
        assert response.json() == {"films": [replaced_film], "details": "Заменено"}


def test_replace_film_not_found(mock_session):
    film_data = {"title": "Replaced", "year": 2024, "description": "Replaced desc"}
    with patch("app.api.routes.films.replace_db_film", AsyncMock(return_value=None)):
        response = client.put(f"{PREFIX}/films/99", json=film_data)
        assert response.status_code == 404
        assert response.json()["detail"] == "Нет такого фильма"


def test_update_film_success(mock_session):
    update_data = {"title": "Updated"}
    updated_film = {"id": 1, "title": "Updated", "year": 2024, "description": "Desc", "reviews": None}
    with patch("app.api.routes.films.update_db_film", AsyncMock(return_value=updated_film)):
        response = client.patch(f"{PREFIX}/films/1", json=update_data)
        assert response.status_code == 200
        assert response.json() == {"films": [updated_film], "details": "Обновлено"}


def test_update_film_not_found(mock_session):
    update_data = {"title": "Updated"}
    with patch("app.api.routes.films.update_db_film", AsyncMock(return_value=None)):
        response = client.patch(f"{PREFIX}/films/99", json=update_data)
        assert response.status_code == 404
        assert response.json()["detail"] == "Нет такого фильма"


def test_delete_film_success(mock_session):
    deleted_film = {"id": 1, "title": "Test", "year": 2024, "description": "Desc", "reviews": None}
    with patch("app.api.routes.films.delete_db_film", AsyncMock(return_value=deleted_film)):
        response = client.delete(f"{PREFIX}/films/1")
        assert response.status_code == 200
        assert response.json() == {"films": [deleted_film], "details": "Удалено"}


def test_delete_film_not_found(mock_session):
    with patch("app.api.routes.films.delete_db_film", AsyncMock(return_value=None)):
        response = client.delete(f"{PREFIX}/films/99")
        assert response.status_code == 404
        assert response.json()["detail"] == "Нет такого фильма"
