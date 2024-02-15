import re

import pytest
from fastapi.testclient import TestClient

from sae_backend.model.database.operations import get_user
from tests.utils.testing_data import get_ressource

from .utils.testing_auth import get_token_for
from .utils.testing_database import TestingSessionLocal, app

JWT_REGEX = re.compile(r"^([a-zA-Z0-9_=]+)\.([a-zA-Z0-9_=]+)\.([a-zA-Z0-9_\-\+\/=]*)")

client = TestClient(app)


@pytest.fixture
def testing_users_auth_headers():
    token = get_token_for("login_test@gmail.com")
    return {"Authorization": "Bearer " + token}


@pytest.fixture
def teacher_auth_headers():
    token = get_token_for("prof@univ-cotedazur.fr")
    return {"Authorization": "Bearer " + token}


@pytest.fixture
def student_auth_headers():
    token = get_token_for("coco@univ-cotedazur.fr")
    return {"Authorization": "Bearer " + token}


def test_get_user_valid(testing_users_auth_headers):
    res = client.get("/api/users/me", headers=testing_users_auth_headers)

    assert res.status_code == 200, res.text


def test_get_user_info_invalid():
    res = client.get("/api/users/me")

    assert res.status_code != 200, res.text


def test_change_user_info_valid(testing_users_auth_headers):
    res = client.post(
        "/api/users/me",
        json={"name": "BetterTester"},
        headers=testing_users_auth_headers,
    )
    data = res.json()

    assert data["name"] == "BetterTester", data["name"]
    assert data["surname"] == "TheTester", data["surname"]

    with TestingSessionLocal() as db:
        user = get_user(db, "login_test@gmail.com")

    assert user is not None

    assert user.name == "BetterTester", user.name  # type: ignore
    assert user.surname == "TheTester", user.surname  # type: ignore


def test_teacher_on_teacher_only(teacher_auth_headers):
    res = client.get("/api/question/read_surveys", headers=teacher_auth_headers)
    assert res.status_code == 200, res.text


def test_student_on_teacher_only(student_auth_headers):
    res = client.get("/api/question/read_surveys", headers=student_auth_headers)
    assert res.status_code == 403, res.text


def test_teacher_on_student_and_teacher(teacher_auth_headers):
    res = client.get("/api/users/me", headers=teacher_auth_headers)
    assert res.status_code == 200, res.text


def test_student_on_student_and_teacher(student_auth_headers):
    res = client.get("/api/users/me", headers=student_auth_headers)
    assert res.status_code == 200, res.text


def test_get_user_by_id(teacher_auth_headers):
    initial_user_id = get_ressource("initial_user_id")
    res = client.get(f"/api/users/get_user/{initial_user_id}", headers=teacher_auth_headers)
    assert res.status_code == 200, res.text


def test_get_user_by_id_not_found(teacher_auth_headers):
    res = client.get(f"/api/users/get_user/{-9676}", headers=teacher_auth_headers)
    assert res.status_code == 404, res.text


def test_get_user_by_email(teacher_auth_headers):
    res = client.get("/api/users/get_user_by_email/login_test@gmail.com", headers=teacher_auth_headers)
    assert res.status_code == 200, res.text


def test_get_user_by_email_not_found(teacher_auth_headers):
    res = client.get("/api/users/get_user_by_email/joe-sep@gmail.com", headers=teacher_auth_headers)
    assert res.status_code == 404, res.text
