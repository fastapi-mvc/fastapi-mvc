import pytest
from fastapi.testclient import TestClient
from fastapi_mvc_template.app.asgi import get_app


@pytest.fixture
def app():
    app = get_app()
    yield TestClient(app)
