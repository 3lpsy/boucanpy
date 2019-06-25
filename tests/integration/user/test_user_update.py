from bountydns.db.factories import factory
from bountydns.db.models import model

from bountydns.core.security import create_bearer_token
from bountydns.core import SUPER_SCOPES, NORMAL_SCOPES
import sys


def test_superuser_can_update_user(client, session):
    auth = factory("SuperUserFactory", session=session).create()
    target = factory("UserFactory", session=session).create(email="target@test.com")

    token = create_bearer_token(data={"sub": auth.id, "scopes": SUPER_SCOPES})
    bearer = "Bearer " + str(token)

    data = {"email": "test222@test.com"}

    response = client.put(
        f"/api/v1/user/{str(target.id)}",
        json=data,
        headers={"Content-Type": "application/json", "Authorization": bearer},
    )
    assert response.status_code == 200
    assert response.json()["user"]["email"] == data["email"]


def test_email_must_not_already_exist_or_failure(client, session):
    auth = factory("SuperUserFactory", session=session).create()
    existing = factory("UserFactory", session=session).create(email="existing@test.com")
    target = factory("UserFactory", session=session).create(email="target2@test.com")

    token = create_bearer_token(data={"sub": auth.id, "scopes": SUPER_SCOPES})
    bearer = "Bearer " + str(token)

    data = {"email": existing.email}

    response = client.put(
        f"/api/v1/user/{str(target.id)}",
        json=data,
        headers={"Content-Type": "application/json", "Authorization": bearer},
    )
    assert response.status_code == 422
