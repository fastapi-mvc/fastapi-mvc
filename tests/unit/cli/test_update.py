import copy
from unittest import mock

import pytest
from copier.errors import UserMessageError
from fastapi_mvc.cli.update import update
from fastapi_mvc.constants import ANSWERS_FILE, COPIER_PROJECT


class TestCliUpdateCommand:

    @pytest.fixture
    def patched_update(self):
        cmd = copy.deepcopy(update)
        copier_patch = mock.patch(
            "fastapi_mvc.cli.update.copier",
        )
        cmd.copier = copier_patch.start()
        yield cmd
        copier_patch.stop()
        del cmd

    def test_should_exit_zero_when_invoked_with_help(self, monkeypatch, fake_project, cli_runner):
        # given / when
        monkeypatch.chdir(fake_project["root"])
        result = cli_runner.invoke(update, ["--help"])

        # then
        assert result.exit_code == 0

    def test_should_exit_error_when_invoked_with_invalid_option(self, cli_runner):
        # given / when
        result = cli_runner.invoke(update, ["--not_exists"])

        # then
        assert result.exit_code == 2

    def test_should_exit_zero_and_call_copier_with_defaults(self, patched_update, monkeypatch, fake_project, cli_runner):
        # given / when
        monkeypatch.chdir(fake_project["root"])
        result = cli_runner.invoke(patched_update, [])

        # then
        assert result.exit_code == 0
        patched_update.copier.run_update.assert_called_once_with(
            vcs_ref=COPIER_PROJECT.vcs_ref,
            answers_file=ANSWERS_FILE,
            user_defaults={
                "_commit": "efb938e",
                "_src_path": "https://github.com/fastapi-mvc/copier-project.git",
                "aiohttp": True,
                "author": "Radosław Szamszur",
                "chart_name": "fake-project",
                "container_image_name": "fake-project",
                "copyright_date": "2022",
                "email": "github@rsd.sh",
                "fastapi_mvc_version": "0.17.0",
                "github_actions": True,
                "helm": True,
                "license": "MIT",
                "nix": True,
                "package_name": "fake_project",
                "project_description": "This project was generated with fastapi-mvc.",
                "project_name": "fake-project",
                "redis": True,
                "repo_url": "https://your.repo.url.here",
                "script_name": "fake-project",
                "version": "0.1.0",
            },
            pretend=False,
            unsafe=True,
        )

    def test_should_exit_zero_and_call_copier_with_parsed_arguments(self, patched_update, monkeypatch, fake_project, cli_runner):
        # given / when
        monkeypatch.chdir(fake_project["root"])
        result = cli_runner.invoke(
            patched_update, [
                "--no-interaction",
                "--pretend",
                "--use-version",
                "master",
            ],
        )

        # then
        assert result.exit_code == 0
        patched_update.copier.run_update.assert_called_once_with(
            vcs_ref="master",
            answers_file=ANSWERS_FILE,
            data={
                "_commit": "efb938e",
                "_src_path": "https://github.com/fastapi-mvc/copier-project.git",
                "aiohttp": True,
                "author": "Radosław Szamszur",
                "chart_name": "fake-project",
                "container_image_name": "fake-project",
                "copyright_date": "2022",
                "email": "github@rsd.sh",
                "fastapi_mvc_version": "0.17.0",
                "github_actions": True,
                "helm": True,
                "license": "MIT",
                "nix": True,
                "package_name": "fake_project",
                "project_description": "This project was generated with fastapi-mvc.",
                "project_name": "fake-project",
                "redis": True,
                "repo_url": "https://your.repo.url.here",
                "script_name": "fake-project",
                "version": "0.1.0",
            },
            overwrite=True,
            pretend=True,
            unsafe=True,
        )

    def test_should_exit_error_when_not_in_fastapi_mvc_project(self, cli_runner, caplog):
        # given / when
        result = cli_runner.invoke(update, [])

        # then
        assert result.exit_code == 1
        msg = "Not a fastapi-mvc project. Try 'fastapi-mvc new --help' for details how to create one."
        assert msg in caplog.text

    def test_should_exit_error_on_copier_error(self, patched_update, monkeypatch, fake_project, cli_runner):
        # given / when
        patched_update.copier.run_update.side_effect = UserMessageError("Fake error")
        monkeypatch.chdir(fake_project["root"])
        result = cli_runner.invoke(patched_update, [])

        # then
        assert result.exit_code == 2
        assert "Fake error" in result.output
        patched_update.copier.run_update.assert_called_once()
