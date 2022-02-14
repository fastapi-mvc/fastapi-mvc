import mock
import pytest
from fastapi_mvc.actions import RunDevelopmentServer


@pytest.fixture
def rds_obj():
    yield RunDevelopmentServer()


@pytest.mark.parametrize(
    "host, port",
    [
        ("127.0.0.1", "8000"),
        ("localhost", "1234"),
    ]
)
@mock.patch("fastapi_mvc.actions.run.IniParser")
@mock.patch("fastapi_mvc.actions.run.ShellUtils.run_shell")
def test_execute(run_mock, ini_mock, rds_obj, host, port):
    ini_mock.return_value.package_name = "foobar"

    rds_obj.execute(host=host, port=port)

    run_mock.assert_called_once_with(
        [
            "poetry",
            "run",
            "uvicorn",
            "--host",
            host,
            "--port",
            port,
            "--reload",
            "foobar.app.asgi:application",
        ]
    )