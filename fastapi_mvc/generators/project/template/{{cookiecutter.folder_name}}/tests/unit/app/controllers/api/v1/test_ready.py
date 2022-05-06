from {{cookiecutter.package_name}}.config import settings


def test_ready(app):
    settings.USE_REDIS = False
    response = app.get("/api/ready")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ready_invalid(app):
    response = app.get("/api/ready/123")
    assert response.status_code == 404
{%- if cookiecutter.redis == "yes" %}


def test_ready_invalid_with_redis(app):
    settings.USE_REDIS = True
    response = app.get("/api/ready")
    assert response.status_code == 502
    assert response.json() == {
        "error": {
            "code": 502,
            "message": "Could not connect to Redis",
            "status": "BAD_GATEWAY",
        }
    }
{% endif %}