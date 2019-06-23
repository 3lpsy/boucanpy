from tests.integration.client import client

from bountydns.db.factories import factory
from bountydns.core.security import create_bearer_token
from bountydns.core import SUPER_SCOPES


def test_status():
    user = factory("SuperUserFactory").create()

    token = create_bearer_token(data={"sub": user.id, "scopes": SUPER_SCOPES})
    bearer = "Bearer " + token
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
