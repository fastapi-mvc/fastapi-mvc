import mock
import pytest
from fastapi_mvc.commands import RunUvicorn


@pytest.mark.parametrize(
    "host, port",
    [
        ("127.0.0.1", "8000"),
        ("localhost", "1234"),
    ]
)
@mock.patch("fastapi_mvc.commands.run_uvicorn.IniParser")
@mock.patch("fastapi_mvc.commands.run_uvicorn.ShellUtils.run_shell")
def test_execute(run_mock, ini_mock, host, port):
    ini_mock.return_value.package_name = "foobar"

    command = RunUvicorn(host=host, port=port)
    command.execute()

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
