import os
from unittest import mock
from subprocess import CalledProcessError

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


@mock.patch("fastapi_mvc.cli.run.run_shell")
def test_run_invalid_options(shell_mock, cli_runner):
    result = cli_runner.invoke(run, ["--not_exists"])
    assert result.exit_code == 2
    shell_mock.assert_not_called()


@mock.patch("fastapi_mvc.cli.run.run_shell")
def test_run_default_values(shell_mock, monkeypatch, cli_runner):
    # Change working directory to fake project. It is easier to fake fastapi-mvc project,
    # rather than mocking ctx injected to command via @click.pass_context decorator.
    monkeypatch.chdir(DATA_DIR)

    result = cli_runner.invoke(run, [])
    assert result.exit_code == 0

    shell_mock.assert_called_once_with(
        cmd=[
            run.poetry_path,
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
        check=True,
    )


@pytest.mark.parametrize(
    "args, expected",
    [
        (
            ["--host", "10.20.30.40", "--port", "1234"],
            {
                "cmd": [
                    run.poetry_path,
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
                "check": True,
            },
        ),
        (
            ["--host", "192.168.0.10", "-p", "9001"],
            {
                "cmd": [
                    run.poetry_path,
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
                "check": True,
            },
        ),
        (
            ["--host", "192.168.0.10", "-p", "9001", "--install"],
            {
                "cmd": [
                    run.poetry_path,
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
                "check": True,
            },
        ),
    ],
)
@mock.patch("fastapi_mvc.cli.run.run_shell")
def test_run_with_options(shell_mock, monkeypatch, cli_runner, args, expected):
    # Change working directory to fake project. It is easier to fake fastapi-mvc project,
    # rather than mocking ctx injected to command via @click.pass_context decorator.
    monkeypatch.chdir(DATA_DIR)

    result = cli_runner.invoke(run, args)
    assert result.exit_code == 0

    calls = []

    if "--install" in args or "-i" in args:
        calls.append(
            mock.call(
                cmd=[
                    run.poetry_path,
                    "install",
                    "--no-interaction",
                ],
                check=True,
            )
        )

    calls.append(mock.call(**expected))
    shell_mock.assert_has_calls(calls)


def test_run_not_in_project(cli_runner):
    result = cli_runner.invoke(run, [])
    assert result.exit_code == 1
    msg = "Not a fastapi-mvc project. Try 'fastapi-mvc new --help' for details how to create one."
    assert msg in result.output


@mock.patch("fastapi_mvc.cli.run.run_shell", side_effect=CalledProcessError(1, []))
def test_run_exception(shell_mock, monkeypatch,cli_runner):
    # Change working directory to fake project. It is easier to fake fastapi-mvc project,
    # rather than mocking ctx injected to command via @click.pass_context decorator.
    monkeypatch.chdir(DATA_DIR)

    result = cli_runner.invoke(run, [])
    assert result.exit_code == 0
    assert "Run 'make install` to install the project." in result.output
    shell_mock.assert_called_once_with(
        cmd=[
            run.poetry_path,
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
        check=True,
    )
