from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


# The health route answers without a token or database call
def test_health_is_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
