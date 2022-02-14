import mock
import pytest
from fastapi_mvc.commands import RunUvicorn


@pytest.mark.parametrize(
    "host, port, package_name",
    [
        ("127.0.0.1", "8000", "test_app"),
        ("localhost", "1234", "foobar"),
    ]
)
@mock.patch("fastapi_mvc.commands.run_uvicorn.ShellUtils.run_shell")
def test_execute(run_mock, host, port, package_name):
    command = RunUvicorn(host=host, port=port, package_name=package_name)
    command.execute()

    run_mock.assert_called_once_with(
        cmd=[
            "poetry",
            "run",
            "uvicorn",
            "--host",
            host,
            "--port",
            port,
            "--reload",
            "{0:s}.app.asgi:application".format(package_name),
        ]
    )
