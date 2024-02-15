from fastapi.testclient import TestClient
import pytest

from .utils.testing_auth import get_token_for
from .utils.testing_database import app


client = TestClient(app)


@pytest.fixture
def testing_users_auth_headers():
    token = get_token_for("Question.man@gmail.com")
    return {"Authorization": "Bearer " + token}


"""

Test Vrai dans des cas normaux d'utilisation
le test est vrai si le code de retour est 200

"""


def test_create_survey(testing_users_auth_headers):
    res = client.post(
        "/api/question/create_survey",
        json={"title": "test", "subject": "test"},
        headers=testing_users_auth_headers,
    )
    assert res.status_code == 200, res.text


def test_read_surveys(testing_users_auth_headers):
    res = client.get("/api/question/read_surveys", headers=testing_users_auth_headers)
    assert res.status_code == 200, res.text


def test_get_survey_info(testing_users_auth_headers):
    res = client.get("/api/question/get_survey_info/1", headers=testing_users_auth_headers)
    assert res.status_code == 200, res.text


def test_read_survey(testing_users_auth_headers):
    res = client.get("/api/question/read_survey/1", headers=testing_users_auth_headers)
    assert res.status_code == 200, res.text


def test_update_survey(testing_users_auth_headers):
    res = client.put(
        "/api/question/update_survey",
        json={"survey_id": 0, "title": "surv1", "subject": "test"},
        headers=testing_users_auth_headers,
    )
    assert res.status_code == 200, res.text


def test_delete_survey(testing_users_auth_headers):
    res = client.delete("/api/question/delete_survey?survey_id=4", headers=testing_users_auth_headers)
    assert res.status_code == 200, res.text


def test_add_question_to_survey(testing_users_auth_headers):
    res = client.post(
        "/api/question/link_question?survey_id=5&question_id=2",
        headers=testing_users_auth_headers,
    )
    assert res.status_code == 200, res.text


def test_remove_question_from_survey(testing_users_auth_headers):
    res = client.delete(
        "/api/question/unlink_question?survey_id=5&question_id=4",
        headers=testing_users_auth_headers,
    )
    assert res.status_code == 200, res.text


def test_create_question(testing_users_auth_headers):
    res = client.post(
        "/api/question/create_question",
        json={"type": "multiple_answers", "text": "test", "media": "test"},
        headers=testing_users_auth_headers,
    )
    assert res.status_code == 200, res.text


def test_read_questions_bank(testing_users_auth_headers):
    res = client.get("/api/question/read_questions_bank", headers=testing_users_auth_headers)
    assert res.status_code == 200, res.text


def test_read_question(testing_users_auth_headers):
    res = client.get("/api/question/read_question/1", headers=testing_users_auth_headers)
    assert res.status_code == 200, res.text


def test_update_question(testing_users_auth_headers):
    res = client.put(
        "/api/question/update_question",
        json={"question_id": 1, "text": "test", "media": "test", "type": "open"},
        headers=testing_users_auth_headers,
    )
    assert res.status_code == 200, res.text


def test_delete_question(testing_users_auth_headers):
    res = client.delete(
        "/api/question/delete_question?id_question=3",
        headers=testing_users_auth_headers,
    )
    assert res.status_code == 200, res.text


def test_create_answer(testing_users_auth_headers):
    res = client.post(
        "/api/question/create_answer",
        json={"question_id": 1, "text": "test", "is_good_answer": True},
        headers=testing_users_auth_headers,
    )
    assert res.status_code == 200, res.text


def test_update_answer(testing_users_auth_headers):
    res = client.put(
        "/api/question/update_answer",
        json={"id_answer": 1, "text": "test", "is_good_answer": True},
        headers=testing_users_auth_headers,
    )
    assert res.status_code == 200, res.text


def test_delete_answer(testing_users_auth_headers):
    res = client.delete("/api/question/delete_answer?answer_id=8", headers=testing_users_auth_headers)
    assert res.status_code == 200, res.text


"""

Test Faux dans des cas de non-connexion de l'utilisateur
le test est faux si le code de retour est 401

"""


def test_create_survey_false(testing_users_auth_headers):
    res = client.post(
        "/api/question/create_survey",
        json={"title": "test", "subject": "test"},
    )
    assert res.status_code == 401, res.text


def test_read_surveys_false(testing_users_auth_headers):
    res = client.get("/api/question/read_surveys")
    assert res.status_code == 401, res.text


def test_get_survey_info_false(testing_users_auth_headers):
    res = client.get("/api/question/get_survey_info/1")
    assert res.status_code == 401, res.text


def test_read_survey_false(testing_users_auth_headers):
    res = client.get("/api/question/read_survey/1")
    assert res.status_code == 401, res.text


def test_update_survey_false(testing_users_auth_headers):
    res = client.put(
        "/api/question/update_survey",
        json={"survey_id": 0, "survey": {"title": "surv1", "subject": "test"}},
    )
    assert res.status_code == 401, res.text


def test_delete_survey_false(testing_users_auth_headers):
    res = client.delete("/api/question/delete_survey?survey_id=4")
    assert res.status_code == 401, res.text


def test_add_question_to_survey_false(testing_users_auth_headers):
    res = client.post(
        "/api/question/link_question",
        json={"survey_id": 1, "question_id": 1},
    )
    assert res.status_code == 401, res.text


def test_remove_question_from_survey_false(testing_users_auth_headers):
    res = client.delete(
        "/api/question/unlink_question?survey_id=2,question_id=2",
    )
    assert res.status_code == 401, res.text


def test_create_question_false(testing_users_auth_headers):
    res = client.post(
        "/api/question/create_question",
        json={"is_multiple": True, "text": "test", "status": "test", "media": "test"},
    )
    assert res.status_code == 401, res.text


def test_read_questions_bank_false(testing_users_auth_headers):
    res = client.get("/api/question/read_questions_bank")
    assert res.status_code == 401, res.text


def test_read_question_false(testing_users_auth_headers):
    res = client.get("/api/question/read_question/1")
    assert res.status_code == 401, res.text


def test_update_question_false(testing_users_auth_headers):
    res = client.put(
        "/api/question/update_question",
        json={"question_id": 1, "text": "test", "media": "test", "status": "test"},
    )
    assert res.status_code == 401, res.text


def test_delete_question_false(testing_users_auth_headers):
    res = client.delete("/api/question/delete_question?id_question=3")
    assert res.status_code == 401, res.text


def test_create_answer_false(testing_users_auth_headers):
    res = client.post(
        "/api/question/create_answer",
        json={"id_question": 1, "text": "test", "is_good_answer": True},
    )
    assert res.status_code == 401, res.text


def test_update_answer_false(testing_users_auth_headers):
    res = client.put(
        "/api/question/update_answer",
        json={"id_answer": 1, "text": "test", "is_good_answer": True},
    )
    assert res.status_code == 401, res.text


def test_delete_answer_false(testing_users_auth_headers):
    res = client.delete("/api/question/delete_answer?answer_id=8")
    assert res.status_code == 401, res.text


"""

Test Faux dans des cas ou il n'y a pas assez d'arguments
le test est faux si le code de retour est 422

"""


def test_create_survey_false2(testing_users_auth_headers):
    res = client.post(
        "/api/question/create_survey",
        json={"title": "test"},
        headers=testing_users_auth_headers,
    )
    assert res.status_code == 422, res.text


def test_get_survey_info_false2(testing_users_auth_headers):
    res = client.get("/api/question/get_survey_info/", headers=testing_users_auth_headers)
    assert res.status_code == 404, res.text


def test_read_survey_false2(testing_users_auth_headers):
    res = client.get("/api/question/read_survey", headers=testing_users_auth_headers)
    assert res.status_code == 404, res.text


def test_update_survey_false2(testing_users_auth_headers):
    res = client.put(
        "/api/question/update_survey",
        json={
            "survey_id": 0,
            "survey": {
                "title": "surv1",
            },
        },
        headers=testing_users_auth_headers,
    )
    assert res.status_code == 422, res.text


def test_delete_survey_false2(testing_users_auth_headers):
    res = client.delete("/api/question/delete_survey", headers=testing_users_auth_headers)
    assert res.status_code == 422, res.text


def test_add_question_to_survey_false2(testing_users_auth_headers):
    res = client.post(
        "/api/question/link_question",
        json={"survey_id": 1},
        headers=testing_users_auth_headers,
    )
    assert res.status_code == 422, res.text


def test_remove_question_from_survey_false2(testing_users_auth_headers):
    res = client.delete(
        "/api/question/unlink_question?survey_id= 2",
        headers=testing_users_auth_headers,
    )
    assert res.status_code == 422, res.text


def test_create_question_false2(testing_users_auth_headers):
    res = client.post(
        "/api/question/create_question",
        json={"is_multiple": True, "text": "test", "status": "test"},
        headers=testing_users_auth_headers,
    )
    assert res.status_code == 422, res.text


def test_update_question_false2(testing_users_auth_headers):
    res = client.put(
        "/api/question/update_question",
        json={"question_id": 1, "text": "test"},
        headers=testing_users_auth_headers,
    )
    assert res.status_code == 422, res.text


def test_delete_question_false2(testing_users_auth_headers):
    res = client.delete("/api/question/delete_question", headers=testing_users_auth_headers)
    assert res.status_code == 422, res.text


def test_create_answer_false2(testing_users_auth_headers):
    res = client.post(
        "/api/question/create_answer",
        json={"id_question": 1, "text": "test"},
        headers=testing_users_auth_headers,
    )
    assert res.status_code == 422, res.text


def test_update_answer_false2(testing_users_auth_headers):
    res = client.put(
        "/api/question/update_answer",
        json={"id_answer": 1, "text": "test"},
        headers=testing_users_auth_headers,
    )
    assert res.status_code == 422, res.text


# test


def test_delete_answer_false2(testing_users_auth_headers):
    res = client.delete("/api/question/delete_answer", headers=testing_users_auth_headers)
    assert res.status_code == 422, res.text
