import copy
from unittest import mock
from subprocess import CalledProcessError

import pytest
from fastapi_mvc.cli.run import run


class TestCliRunCommand:

    @pytest.fixture
    def patched_run(self):
        cmd = copy.deepcopy(run)
        with mock.patch("fastapi_mvc.cli.run.run_shell") as mck:
            cmd.run_shell = mck
            yield cmd
        del cmd

    def test_should_exit_zero_when_invoked_with_help(self, cli_runner):
        # given / when
        result = cli_runner.invoke(run, ["--help"])

        # then
        assert result.exit_code == 0

    def test_should_exit_error_when_invoked_with_invalid_option(self, cli_runner):
        # given / when
        result = cli_runner.invoke(run, ["--not_exists"])

        # then
        assert result.exit_code == 2

    def test_should_use_default_values_when_invoked_empty(self, patched_run, monkeypatch, fake_project, cli_runner):
        # given / when
        monkeypatch.chdir(fake_project["root"])
        monkeypatch.setenv("POETRY_BINARY", "/opt/poetry")
        result = cli_runner.invoke(patched_run, [])

        # then
        assert result.exit_code == 0
        patched_run.run_shell.assert_called_once_with(
            cmd=[
                "/opt/poetry",
                "run",
                "uvicorn",
                "--factory",
                "--host",
                "127.0.0.1",
                "--port",
                "8000",
                "--reload",
                f"{patched_run.project_data['package_name']}.app:get_application",
            ],
            check=True,
        )

    def test_should_call_run_shell_with_parsed_arguments(self, patched_run, monkeypatch, fake_project, cli_runner):
        # given / when
        monkeypatch.chdir(fake_project["root"])
        monkeypatch.setenv("POETRY_BINARY", "/opt/poetry")
        result = cli_runner.invoke(
            patched_run,
            ["--host", "10.20.30.40", "--port", "1234"],
        )

        # then
        assert result.exit_code == 0
        patched_run.run_shell.assert_called_once_with(
            cmd=[
                "/opt/poetry",
                "run",
                "uvicorn",
                "--factory",
                "--host",
                "10.20.30.40",
                "--port",
                "1234",
                "--reload",
                f"{patched_run.project_data['package_name']}.app:get_application",
            ],
            check=True,
        )

    def test_should_execute_make_install_and_exit_zero(self, patched_run, monkeypatch, fake_project, cli_runner):
        # given / when
        monkeypatch.chdir(fake_project["root"])
        monkeypatch.setenv("POETRY_BINARY", "/opt/poetry")
        result = cli_runner.invoke(patched_run, ["--install"])

        # then
        assert result.exit_code == 0
        patched_run.run_shell.assert_any_call(
            cmd=[
                "/opt/poetry",
                "install",
                "--no-interaction",
            ],
            check=True,
        )

    def test_should_exit_error_when_not_in_fastapi_mvc_project(self, cli_runner):
        # given / when
        result = cli_runner.invoke(run, [])

        # then
        assert result.exit_code == 1
        msg = "Not a fastapi-mvc project. Try 'fastapi-mvc new --help' for details how to create one."
        assert msg in result.output

    def test_should_exit_error_on_subprocess_error(self, patched_run, monkeypatch, fake_project, cli_runner):
        # given / when
        patched_run.run_shell.side_effect = CalledProcessError(1, [])
        monkeypatch.chdir(fake_project["root"])
        result = cli_runner.invoke(patched_run, [])

        # then
        assert result.exit_code == 1
        assert "Run 'make install` to install the project." in result.output
        patched_run.run_shell.assert_called_once()
