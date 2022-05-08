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
parser = mock.Mock()
parser.package_name = "test_app"
parser.folder_name = "test-app"
parser.project_root = "/path/to/project"


@mock.patch("fastapi_mvc.cli.run.Borg")
def test_run_help(borg_mock, cli_runner):
    result = cli_runner.invoke(run, ["--help"])
    assert result.exit_code == 0
    borg_mock.assert_not_called()


@mock.patch("fastapi_mvc.cli.run.Borg")
def test_run_invalid_options(borg_mock, cli_runner):
    result = cli_runner.invoke(run, ["--not_exists"])
    assert result.exit_code == 2
    borg_mock.assert_not_called()


@mock.patch("fastapi_mvc.cli.run.RunShell")
@mock.patch("fastapi_mvc.cli.run.Borg")
def test_run_default_values(borg_mock, shell_mock, cli_runner):
    borg_mock.return_value.parser = parser
    borg_mock.return_value.poetry_path = "/path/to/bin/poetry"

    result = cli_runner.invoke(run, [])
    assert result.exit_code == 0

    borg_mock.assert_called_once()
    borg_mock.return_value.require_project.assert_called_once()

    shell_mock.assert_has_calls(
        [
            mock.call(
                cmd=[
                    "/path/to/bin/poetry",
                    "install",
                    "--no-interaction",
                ],
                check=True,
                cwd="/path/to/project",
            ),
            mock.call(
                cmd=[
                    "/path/to/bin/poetry",
                    "run",
                    "uvicorn",
                    "--factory",
                    "--host",
                    "127.0.0.1",
                    "--port",
                    "8000",
                    "--reload",
                    "test_app.app:get_application",
                ],
                cwd="/path/to/project",
            ),
        ]
    )

    borg_mock.return_value.enqueue.assert_has_calls(shell_mock.return_value)
    borg_mock.return_value.execute.assert_called_once()


@pytest.mark.parametrize(
    "args, expected",
    [
        (
            ["--host", "10.20.30.40", "--port", "1234"],
            {
                "cmd": [
                    "/path/to/bin/poetry",
                    "run",
                    "uvicorn",
                    "--factory",
                    "--host",
                    "10.20.30.40",
                    "--port",
                    "1234",
                    "--reload",
                    "test_app.app:get_application",
                ],
                "cwd": "/path/to/project",
            },
        ),
        (
            ["--host", "192.168.0.10", "-p", "9001"],
            {
                "cmd": [
                    "/path/to/bin/poetry",
                    "run",
                    "uvicorn",
                    "--factory",
                    "--host",
                    "192.168.0.10",
                    "--port",
                    "9001",
                    "--reload",
                    "test_app.app:get_application",
                ],
                "cwd": "/path/to/project",
            },
        ),
        (
            ["--host", "192.168.0.10", "-p", "9001", "--skip-install"],
            {
                "cmd": [
                    "/path/to/bin/poetry",
                    "run",
                    "uvicorn",
                    "--factory",
                    "--host",
                    "192.168.0.10",
                    "--port",
                    "9001",
                    "--reload",
                    "test_app.app:get_application",
                ],
                "cwd": "/path/to/project",
            },
        ),
    ],
)
@mock.patch("fastapi_mvc.cli.run.RunShell")
@mock.patch("fastapi_mvc.cli.run.Borg")
def test_run_with_options(borg_mock, shell_mock, cli_runner, args, expected):
    borg_mock.return_value.parser = parser
    borg_mock.return_value.poetry_path = "/path/to/bin/poetry"

    result = cli_runner.invoke(run, args)
    assert result.exit_code == 0

    borg_mock.assert_called_once()
    borg_mock.return_value.require_project.assert_called_once()

    if "--skip-install" in args or "-I" in args:
        calls = []
    else:
        calls = [
            mock.call(
                cmd=[
                    "/path/to/bin/poetry",
                    "install",
                    "--no-interaction",
                ],
                check=True,
                cwd="/path/to/project",
            )
        ]

    calls.append(mock.call(**expected))

    shell_mock.assert_has_calls(calls)
    borg_mock.return_value.enqueue.assert_has_calls(shell_mock.return_value)
    borg_mock.return_value.execute.assert_called_once()
