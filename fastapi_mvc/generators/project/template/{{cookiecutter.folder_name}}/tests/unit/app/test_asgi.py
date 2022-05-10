import mock
from {{cookiecutter.package_name}}.config import settings
from {{cookiecutter.package_name}}.app.router import root_api_router
from {{cookiecutter.package_name}}.app.asgi import (
    get_application,
    on_startup,
    on_shutdown,
)
from {{cookiecutter.package_name}}.app.exceptions import (
    HTTPException,
    http_exception_handler,
)


@mock.patch("{{cookiecutter.package_name}}.app.asgi.FastAPI")
def test_get_app(mock_fastapi):
    mock_app = get_application()
    # check init kwargs
    mock_fastapi.assert_called_once_with(
        title=settings.PROJECT_NAME,
        debug=settings.DEBUG,
        version=settings.VERSION,
        docs_url=settings.DOCS_URL,
        on_startup=[on_startup],
        on_shutdown=[on_shutdown],
    )

    mock_app.include_router.assert_called_once_with(root_api_router)
    mock_app.add_exception_handler.assert_called_once_with(
        HTTPException, http_exception_handler
    )


def test_app_config(app):
    assert app.app.title == settings.PROJECT_NAME
    assert app.app.version == settings.VERSION
