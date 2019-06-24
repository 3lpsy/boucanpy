from bountydns.db.factories import factory
from bountydns.core.security import create_bearer_token
from bountydns.core import SUPER_SCOPES, NORMAL_SCOPES
import sys


def test_superuser_can_create_user(client, session):
    auth = factory("SuperUserFactory", session=session).create()

    token = create_bearer_token(data={"sub": auth.id, "scopes": SUPER_SCOPES})
    bearer = "Bearer " + str(token)
    data = {
        "email": "test@test.com",
        "password": "Password123",
        "password_confirm": "Password123",
    }
    response = client.post(
        "/api/v1/user",
        json=data,
        headers={"Content-Type": "application/json", "Authorization": bearer},
    )
    assert response.status_code == 200
    assert response.json()["user"]["email"] == data["email"]


def test_mismatching_passwords_causes_failure(client, session):
    auth = factory("SuperUserFactory", session=session).create()

    token = create_bearer_token(data={"sub": auth.id, "scopes": SUPER_SCOPES})
    bearer = "Bearer " + str(token)
    data = {
        "email": "test@test.com",
        "password": "Password",
        "password_confirm": "Password123",
    }
    response = client.post(
        "/api/v1/user",
        json=data,
        headers={"Content-Type": "application/json", "Authorization": bearer},
    )
    assert response.status_code == 422


def test_short_password_causes_failure(client, session):
    auth = factory("SuperUserFactory", session=session).create()

    token = create_bearer_token(data={"sub": auth.id, "scopes": SUPER_SCOPES})
    bearer = "Bearer " + str(token)
    data = {"email": "a@a.com", "password": "pass2", "password_confirm": "pass2"}
    response = client.post(
        "/api/v1/user",
        json=data,
        headers={"Content-Type": "application/json", "Authorization": bearer},
    )
    assert response.status_code == 422


def test_common_or_bad_password_causes_failure(client, session):
    # TODO
    pass


def test_short_email_causes_failure(client, session):
    auth = factory("SuperUserFactory", session=session).create()

    token = create_bearer_token(data={"sub": auth.id, "scopes": SUPER_SCOPES})
    bearer = "Bearer " + str(token)
    data = {
        "email": "a@a.com",
        "password": "Password123",
        "password_confirm": "Password123",
    }
    response = client.post(
        "/api/v1/user",
        json=data,
        headers={"Content-Type": "application/json", "Authorization": bearer},
    )
    assert response.status_code == 422


def test_username_is_not_valid_email_format_causes_failure(client, session):
    auth = factory("SuperUserFactory", session=session).create()

    token = create_bearer_token(data={"sub": auth.id, "scopes": SUPER_SCOPES})
    bearer = "Bearer " + str(token)
    data = {
        "email": "testtest",
        "password": "Password123",
        "password_confirm": "Password123",
    }
    response = client.post(
        "/api/v1/user",
        json=data,
        headers={"Content-Type": "application/json", "Authorization": bearer},
    )
    assert response.status_code == 422


def test_regular_user_cannot_create_user(client, session):
    auth = factory("UserFactory", session=session).create()

    token = create_bearer_token(data={"sub": auth.id, "scopes": NORMAL_SCOPES})
    bearer = "Bearer " + str(token)
    data = {
        "email": "test@test.com",
        "password": "Password123",
        "password_confirm": "Password123",
    }
    response = client.post(
        "/api/v1/user",
        json=data,
        headers={"Content-Type": "application/json", "Authorization": bearer},
    )
    assert response.status_code == 403


def test_unauthed_user_cannot_create_user(client, session):
    bearer = "Bearer "
    data = {
        "email": "test@test.com",
        "password": "Password123",
        "password_confirm": "Password123",
    }
    response = client.post(
        "/api/v1/user",
        json=data,
        headers={"Content-Type": "application/json", "Authorization": bearer},
    )
    assert response.status_code == 403
