from fastapi_mvc_template.config import settings


def test_app_config(app):
    assert app.app.title == settings.PROJECT_NAME
    assert app.app.version == settings.VERSION


def test_read_docs(app):
    response = app.get("/")
    assert response.status_code == 200


def test_not_found(app):
    response = app.get("/some/none/existing/path")
    assert response.status_code == 404
