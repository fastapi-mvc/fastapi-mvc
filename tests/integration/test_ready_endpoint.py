from fastapi.testclient import TestClient
from fastapi_mvc_template.app.asgi import get_app


app = TestClient(get_app())


def test_ready():
    response = app.get("/api/ready")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
