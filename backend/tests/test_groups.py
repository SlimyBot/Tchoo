from fastapi.testclient import TestClient
import pytest

from .utils.testing_auth import get_token_for
from .utils.testing_database import app

client = TestClient(app)


@pytest.fixture
def testing_users_auth_headers():
    token = get_token_for("Group.man@gmail.com")
    return {"Authorization": "Bearer " + token}


def test_create_group(testing_users_auth_headers):
    res = client.post("/api/groups/create_group?group_name=test", headers=testing_users_auth_headers)
    assert res.status_code == 200, res.text


def test_read_user_groups(testing_users_auth_headers):
    res = client.get("/api/groups/get_user_groups/3", headers=testing_users_auth_headers)
    assert res.status_code == 200, res.text


def test_read_groups(testing_users_auth_headers):
    res = client.get("/api/groups/get_groups", headers=testing_users_auth_headers)
    assert res.status_code == 200, res.text


def test_read_group(testing_users_auth_headers):
    res = client.get("/api/groups/1", headers=testing_users_auth_headers)
    assert res.status_code == 200, res.text


def test_update_group(testing_users_auth_headers):
    res = client.put("/api/groups/update_group/1?name=test", headers=testing_users_auth_headers)
    assert res.status_code == 200, res.text


def test_delete_group(testing_users_auth_headers):
    res = client.delete("/api/groups/delete_group/1", headers=testing_users_auth_headers)
    assert res.status_code == 200, res.text


def test_add_member(testing_users_auth_headers):
    res = client.post("/api/groups/add_member/2?member_id=2", headers=testing_users_auth_headers)
    assert res.status_code == 200, res.text


def test_remove_member(testing_users_auth_headers):
    res = client.delete("/api/groups/remove_member/2?member_id=2", headers=testing_users_auth_headers)
    assert res.status_code == 200, res.text


def test_read_group_invalid(testing_users_auth_headers):
    res = client.get("/api/groups/read_group_route?5", headers=testing_users_auth_headers)
    assert res.status_code != 200, res.text


def test_update_group_invalid(testing_users_auth_headers):
    res = client.put("/api/groups/update_group/5?group_name=test", headers=testing_users_auth_headers)
    assert res.status_code != 200, res.text


def test_delete_group_invalid(testing_users_auth_headers):
    res = client.delete("/api/groups/delete_group?group_id=5", headers=testing_users_auth_headers)
    assert res.status_code != 200, res.text


def test_add_member_invalid(testing_users_auth_headers):
    res = client.post("/api/groups/add_member/5?member_id=10", headers=testing_users_auth_headers)
    assert res.status_code != 200, res.text
