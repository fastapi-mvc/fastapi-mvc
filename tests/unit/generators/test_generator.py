import copy
from unittest import mock
from datetime import datetime

import pytest
from fastapi_mvc.generators import GeneratorGenerator
from fastapi_mvc.constants import COPIER_GENERATOR


class TestGeneratorGenerator:

    @pytest.fixture
    def generator(self):
        generator = copy.deepcopy(GeneratorGenerator)
        copier_patch = mock.patch(
            "fastapi_mvc.generators.generator.copier",
        )
        generator.copier = copier_patch.start()
        yield generator
        copier_patch.stop()
        del generator

    def test_should_exit_zero_when_invoked_with_help(self, generator, cli_runner):
        # given / when
        result = cli_runner.invoke(generator, ["--help"])

        # then
        assert result.exit_code == 0

    def test_should_exit_error_when_invoked_with_invalid_option(self, generator, cli_runner):
        # given / when
        result = cli_runner.invoke(generator, ["--not_exists"])

        # then
        assert result.exit_code == 2

    def test_should_call_copier_using_default_values(self, generator, monkeypatch, fake_project, cli_runner):
        # given / when
        monkeypatch.chdir(fake_project["root"])
        result = cli_runner.invoke(generator, ["fake-generator"])

        # then
        assert result.exit_code == 0
        generator.copier.run_copy.assert_called_once_with(
            src_path=COPIER_GENERATOR.template,
            vcs_ref=COPIER_GENERATOR.vcs_ref,
            dst_path="./lib/generators/fake_generator",
            data={
                "generator": "fake_generator",
                "nix": True,
                "github_actions": True,
                "repo_url": "https://your.repo.url.here",
                "license": "MIT",
                "copyright_date": datetime.today().year,
            },
            answers_file=".generator.yml",
        )

    def test_should_call_copier_with_parsed_arguments(self, generator, monkeypatch, fake_project, cli_runner):
        # given / when
        monkeypatch.chdir(fake_project["root"])
        result = cli_runner.invoke(
            generator,
            [
                "--skip-nix",
                "--skip-actions",
                "--license",
                "ISC",
                "--repo-url",
                "https://mambo.no6.git",
                "Mambo-No6",
            ],
        )

        # then
        assert result.exit_code == 0
        generator.copier.run_copy.assert_called_once_with(
            src_path=COPIER_GENERATOR.template,
            vcs_ref=COPIER_GENERATOR.vcs_ref,
            dst_path="./lib/generators/mambo_no6",
            data={
                "generator": "mambo_no6",
                "nix": False,
                "github_actions": False,
                "repo_url": "https://mambo.no6.git",
                "license": "ISC",
                "copyright_date": datetime.today().year,
            },
            answers_file=".generator.yml",
        )

    def test_should_exit_error_when_not_in_fastapi_mvc_project(self, generator, cli_runner, caplog):
        # given / when
        result = cli_runner.invoke(generator, ["fake-generator"])

        # then
        assert result.exit_code == 1
        msg = "Not a fastapi-mvc project. Try 'fastapi-mvc new --help' for details how to create one."
        assert msg in caplog.text
