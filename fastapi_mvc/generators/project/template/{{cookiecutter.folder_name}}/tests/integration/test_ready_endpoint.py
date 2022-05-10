from fastapi.testclient import TestClient
from {{cookiecutter.package_name}}.app import get_application
from {{cookiecutter.package_name}}.config import settings


app = get_application()


def test_ready():
    settings.USE_REDIS = False

    with TestClient(app) as client:
        response = client.get("/api/ready")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


def test_ready_invalid():
    with TestClient(app) as client:
        response = client.get("/api/ready/123")
        assert response.status_code == 404
{%- if cookiecutter.redis == "yes" %}


def test_ready_invalid_with_redis():
    settings.USE_REDIS = True

    with TestClient(app) as client:
        response = client.get("/api/ready")
        assert response.status_code == 502
        assert response.json() == {
            "error": {
                "code": 502,
                "message": "Could not connect to Redis",
                "status": "BAD_GATEWAY",
            }
        }
{% endif %}