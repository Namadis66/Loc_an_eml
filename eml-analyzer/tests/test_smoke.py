from fastapi.testclient import TestClient

from app.main import app


def test_health_cases_endpoint() -> None:
    client = TestClient(app)
    response = client.get('/cases')
    assert response.status_code == 200
    assert isinstance(response.json(), list)
