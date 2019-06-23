from tests.integration.client import client


def test_status():
    response = client.get("/api/v1/status")
    assert response.status_code == 200
