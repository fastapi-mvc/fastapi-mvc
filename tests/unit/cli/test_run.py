import os

import mock
import pytest
from fastapi_mvc.cli.run import run


DATA_DIR = os.path.abspath(
    os.path.join(
        os.path.abspath(__file__),
        "../../data",
    )
)


def test_run_help(cli_runner):
    result = cli_runner.invoke(run, ["--help"])
    assert result.exit_code == 0


def test_run_invalid_options(cli_runner):
    result = cli_runner.invoke(run, ["--not_exists"])
    assert result.exit_code == 2


@mock.patch("fastapi_mvc.cli.run.RunShell")
@mock.patch("fastapi_mvc.cli.run.Borg")
def test_run_default_values(borg_mock, shell_mock, cli_runner):
    borg_mock.return_value.parser.package_name = "test_app"

    result = cli_runner.invoke(run, [])
    assert result.exit_code == 0

    borg_mock.assert_called_once()
    borg_mock.return_value.require_installed.assert_called_once()

    shell_mock.assert_called_once_with(
        cmd=[
            "poetry",
            "run",
            "uvicorn",
            "--host",
            "127.0.0.1",
            "--port",
            "8000",
            "--reload",
            "test_app.app.asgi:application",
        ]
    )

    borg_mock.return_value.enqueue_command.assert_called_once_with(
        shell_mock.return_value
    )
    borg_mock.return_value.execute.assert_called_once()


@pytest.mark.parametrize(
    "args, expected",
    [
        (
            ["--host", "10.20.30.40", "--port", "1234"],
            {
                "cmd": [
                    "poetry",
                    "run",
                    "uvicorn",
                    "--host",
                    "10.20.30.40",
                    "--port",
                    "1234",
                    "--reload",
                    "test_app.app.asgi:application",
                ]
            }
        ),
        (
            ["--host", "192.168.0.10", "-p", "9001"],
            {
                "cmd": [
                    "poetry",
                    "run",
                    "uvicorn",
                    "--host",
                    "192.168.0.10",
                    "--port",
                    "9001",
                    "--reload",
                    "test_app.app.asgi:application",
                ]
            }
        )
    ]
)
@mock.patch("fastapi_mvc.cli.run.RunShell")
@mock.patch("fastapi_mvc.cli.run.Borg")
def test_run_with_options(borg_mock, shell_mock, cli_runner, args, expected):
    borg_mock.return_value.parser.package_name = "test_app"

    result = cli_runner.invoke(run, args)
    assert result.exit_code == 0

    borg_mock.assert_called_once()
    shell_mock.assert_called_once_with(**expected)

    borg_mock.return_value.enqueue_command.assert_called_once_with(
        shell_mock.return_value
    )
    borg_mock.return_value.execute.assert_called_once()
