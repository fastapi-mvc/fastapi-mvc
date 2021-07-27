from fastapi_mvc_template.app.config.application import PROJECT_NAME, VERSION


def test_app_config(app):
    assert app.app.title == PROJECT_NAME
    assert app.app.version == VERSION


def test_read_main(app):
    response = app.get("/")
    assert response.status_code == 200


def test_not_found(app):
    response = app.get("/some/none/existing/path")
    assert response.status_code == 404
