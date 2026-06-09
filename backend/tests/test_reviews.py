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


@pytest.fixture
def mock_celery_send_task():
    with patch("app.api.routes.reviews.celery_client.send_task") as mock:
        yield mock


def test_get_reviews_success(mock_session):
    mock_reviews = [
        {
            "id": 1,
            "title": "Great film",
            "description": "Awesome",
            "film_id": 1,
            "status": "new",
            "label": None,
            "label_id": None,
            "probability": None,
        }
    ]
    with patch("app.api.routes.reviews.get_db_reviews", AsyncMock(return_value=mock_reviews)):
        response = client.get(f"{PREFIX}/reviews/")
        assert response.status_code == 200
        assert response.json() == {"reviews": mock_reviews, "details": None}


def test_get_review_by_id_found(mock_session):
    review = {
        "id": 1,
        "title": "Nice",
        "description": "Loved it",
        "film_id": 1,
        "status": "new",
        "label": None,
        "label_id": None,
        "probability": None,
    }
    with patch("app.api.routes.reviews.get_review_by_id", AsyncMock(return_value=review)):
        response = client.get(f"{PREFIX}/reviews/1")
        assert response.status_code == 200
        assert response.json() == {"reviews": [review], "details": None}


def test_get_review_by_id_not_found(mock_session):
    with patch("app.api.routes.reviews.get_review_by_id", AsyncMock(return_value=None)):
        response = client.get(f"{PREFIX}/reviews/99")
        assert response.status_code == 404
        assert response.json()["detail"] == "Нет такого отзыва"


def test_update_review_success(mock_session):
    update_data = {"description": "Updated description"}
    updated_review = {
        "id": 1,
        "title": "Old",
        "description": "Updated description",
        "film_id": 1,
        "status": "new",
        "label": None,
        "label_id": None,
        "probability": None,
    }
    with patch("app.api.routes.reviews.update_db_review", AsyncMock(return_value=updated_review)):
        response = client.patch(f"{PREFIX}/reviews/1", json=update_data)
        assert response.status_code == 200
        assert response.json() == {"reviews": [updated_review], "details": "Обновлено"}


def test_update_review_not_found(mock_session):
    update_data = {"description": "Updated description"}
    with patch("app.api.routes.reviews.update_db_review", AsyncMock(return_value=None)):
        response = client.patch(f"{PREFIX}/reviews/99", json=update_data)
        assert response.status_code == 404
        assert response.json()["detail"] == "Нет такого отзыва"


def test_delete_review_success(mock_session):
    deleted_review = {
        "id": 1,
        "title": "To delete",
        "description": "desc",
        "film_id": 1,
        "status": "new",
        "label": None,
        "label_id": None,
        "probability": None,
    }
    with patch("app.api.routes.reviews.delete_db_review", AsyncMock(return_value=deleted_review)):
        response = client.delete(f"{PREFIX}/reviews/1")
        assert response.status_code == 200
        assert response.json() == {"reviews": [deleted_review], "details": "Удалено"}


def test_delete_review_not_found(mock_session):
    with patch("app.api.routes.reviews.delete_db_review", AsyncMock(return_value=None)):
        response = client.delete(f"{PREFIX}/reviews/99")
        assert response.status_code == 404
        assert response.json()["detail"] == "Нет такого отзыва"
