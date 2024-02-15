from fastapi.testclient import TestClient
import pytest

from .utils.testing_auth import get_token_for
from .utils.testing_data import get_ressource

from .utils.testing_database import app

client = TestClient(app)


@pytest.fixture
def testing_user_auth_headers():
    token = get_token_for("session.man@gmail.com")
    return {"Authorization": "Bearer " + token}


def test_create_session_template_valid(testing_user_auth_headers):
    testing_session_survey_id = get_ressource("testing_session_survey_id")

    res = client.post(
        "/api/sessions/template/new",
        json={
            "survey_id": testing_session_survey_id,
            "name": "Test Template",
            "type": "piloted",
            "authorised_group_id": None,
            "show_answers": False,
        },
        headers=testing_user_auth_headers,
    )
    data = res.json()

    assert res.status_code == 200, res.text
    assert "id" in data, data
    assert data["survey_id"] == testing_session_survey_id, data["survey_id"]


def test_create_session_template_with_group(testing_user_auth_headers):
    testing_session_survey_id = get_ressource("testing_session_survey_id")
    auth_group_id = get_ressource("auth_group_id")

    res = client.post(
        "/api/sessions/template/new",
        json={
            "survey_id": testing_session_survey_id,
            "name": "Test Template but better",
            "type": "piloted",
            "authorised_group_id": auth_group_id,
            "show_answers": False,
        },
        headers=testing_user_auth_headers,
    )
    data = res.json()

    assert res.status_code == 200, res.text
    assert data["authorised_group_id"] == auth_group_id, data["authorised_group_id"]


def test_create_session_template_invalid_survey(testing_user_auth_headers):
    res = client.post(
        "/api/sessions/template/new",
        json={
            "survey_id": -8956,
            "name": "Test Template",
            "type": "auto_timer",
            "authorised_group_id": None,
            "show_answers": True,
        },
        headers=testing_user_auth_headers,
    )

    assert res.status_code == 403, res.text


def test_create_session_template_missing_fields(testing_user_auth_headers):
    testing_session_survey_id = get_ressource("testing_session_survey_id")

    res = client.post(
        "/api/sessions/template/new",
        json={"survey_id": testing_session_survey_id},
        headers=testing_user_auth_headers,
    )

    assert res.status_code == 422, res.text


def test_get_session_template_valid(testing_user_auth_headers):
    testing_session_template_id = get_ressource("testing_session_template_id")

    res = client.get(
        f"/api/sessions/template/{testing_session_template_id}",
        headers=testing_user_auth_headers,
    )
    data = res.json()

    assert res.status_code == 200, res.text
    assert "id" in data, data
    assert data["id"] == testing_session_template_id, data["id"]


def test_get_session_template_invalid(testing_user_auth_headers):
    res = client.get(
        "/api/sessions/template/-562",
        headers=testing_user_auth_headers,
    )
    data = res.json()

    assert res.status_code == 404, res.text
    assert data["detail"] == "Session template not found", data["details"]


def test_get_all_session_templates(testing_user_auth_headers):
    res = client.get(
        "/api/sessions/template/all",
        headers=testing_user_auth_headers,
    )
    data = res.json()

    for template in data:
        assert template["id"] > 0, template["id"]


def test_edit_session_template_valid(testing_user_auth_headers):
    testing_session_template_edit_id = get_ressource("testing_session_template_edit_id")

    res = client.put(
        f"/api/sessions/template/update/{testing_session_template_edit_id}",
        headers=testing_user_auth_headers,
        json={"name": "New name"},
    )
    data = res.json()

    assert res.status_code == 200, res.text

    assert data["name"] != "editme", data["name"]
    assert data["name"] == "New name", data["name"]

    res = client.put(
        f"/api/sessions/template/update/{testing_session_template_edit_id}",
        headers=testing_user_auth_headers,
        json={"type": "piloted"},
    )
    data = res.json()

    assert res.status_code == 200, res.text
    assert data["type"] == "piloted", data["type"]


def test_edit_session_template_invalid_wrong_id(testing_user_auth_headers):
    res = client.put(
        "/api/sessions/template/update/-85",
        headers=testing_user_auth_headers,
        json={"name": "New name"},
    )

    assert res.status_code == 403, res.text


def test_edit_session_template_invalid_validation(testing_user_auth_headers):
    res = client.put(
        "/api/sessions/template/update/-85",
        headers=testing_user_auth_headers,
        json={"type": "stupid type"},
    )

    assert res.status_code == 422, res.text


def test_delete_session_template_valid(testing_user_auth_headers):
    testing_session_template_delete_id = get_ressource("testing_session_template_delete_id")

    res = client.delete(
        f"/api/sessions/template/delete/{testing_session_template_delete_id}", headers=testing_user_auth_headers
    )

    data = res.json()

    assert res.status_code == 200, res.text
    assert data == "OK"


def test_delete_session_template_invalid(testing_user_auth_headers):
    res = client.delete("/api/sessions/template/delete/-856", headers=testing_user_auth_headers)

    assert res.status_code == 403, res.text


def test_start_survey_session_valid(testing_user_auth_headers):
    testing_session_template_id = get_ressource("testing_session_template_id")

    res = client.post(
        "/api/sessions/start",
        headers=testing_user_auth_headers,
        json={"session_template_id": testing_session_template_id},
    )

    data = res.json()

    assert res.status_code == 200, res.text
    assert "join_code" in data, data


def test_start_survey_session_invalid(testing_user_auth_headers):
    res = client.post("/api/sessions/start", headers=testing_user_auth_headers, json={"session_template_id": -56461})

    assert res.status_code == 404, res.text


def test_list_all_sessions(testing_user_auth_headers):
    started_session_join_code = get_ressource("started_session_join_code")

    res = client.get("/api/sessions/all", headers=testing_user_auth_headers)
    data = res.json()

    assert res.status_code == 200, res.text
    assert any(s["join_code"] == started_session_join_code for s in data)
