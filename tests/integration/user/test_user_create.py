from bountydns.db.factories import factory
from bountydns.core.security import create_bearer_token
from bountydns.core import SUPER_SCOPES, NORMAL_SCOPES
import sys


def test_superuser_can_create_user(client, session):
    f = factory("SuperUserFactory")
    user = f.create()

    token = create_bearer_token(data={"sub": user.id, "scopes": SUPER_SCOPES})
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


def test_regular_user_cannot_create_user(client, session):
    f = factory("UserFactory")
    user = f.create()

    token = create_bearer_token(data={"sub": user.id, "scopes": NORMAL_SCOPES})
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
