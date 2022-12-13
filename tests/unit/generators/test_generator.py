import os
from unittest import mock
from datetime import datetime

import pytest
from fastapi_mvc.generators import GeneratorGenerator


DATA_DIR = os.path.abspath(
    os.path.join(
        os.path.abspath(__file__),
        "../../data",
    )
)


def test_generator_help(cli_runner):
    result = cli_runner.invoke(GeneratorGenerator, ["--help"])
    assert result.exit_code == 0


def test_generator_invalid_options(cli_runner):
    result = cli_runner.invoke(GeneratorGenerator, ["--not_exists"])
    assert result.exit_code == 2


@mock.patch("fastapi_mvc.generators.generator.Generator.run_copy")
def test_generator_default_values(copier_mock, monkeypatch, cli_runner):
    # Change working directory to fake project. It is easier to fake fastapi-mvc project,
    # rather than mocking ctx injected to command via @click.pass_context decorator.
    monkeypatch.chdir(DATA_DIR)

    result = cli_runner.invoke(GeneratorGenerator, ["custom-generator"])
    assert result.exit_code == 0

    copier_mock.assert_called_once_with(
        dst_path="./lib/generators/custom_generator",
        data={
            "generator": "custom_generator",
            "nix": True,
            "repo_url": "https://your.repo.url.here",
            "license": "MIT",
            "copyright_date": datetime.today().year,
        },
        answers_file=".generator.yml",
    )


@pytest.mark.parametrize(
    "args, expected",
    [
        (
            [
                "-N",
                "--license",
                "ISC",
                "--repo-url",
                "https://mambo.no6.git",
                "Mambo-No6",
            ],
            {
                "dst_path": "./lib/generators/mambo_no6",
                "data": {
                    "generator": "mambo_no6",
                    "nix": False,
                    "repo_url": "https://mambo.no6.git",
                    "license": "ISC",
                    "copyright_date": datetime.today().year,
                },
                "answers_file": ".generator.yml",
            },
        )
    ],
)
@mock.patch("fastapi_mvc.generators.generator.Generator.run_copy")
def test_generator_with_options(copier_mock, monkeypatch, cli_runner, args, expected):
    # Change working directory to fake project. It is easier to fake fastapi-mvc project,
    # rather than mocking ctx injected to command via @click.pass_context decorator.
    monkeypatch.chdir(DATA_DIR)

    result = cli_runner.invoke(GeneratorGenerator, args)
    assert result.exit_code == 0

    copier_mock.assert_called_once_with(**expected)


def test_generator_not_in_project(cli_runner):
    result = cli_runner.invoke(GeneratorGenerator, ["custom-generator"])
    assert result.exit_code == 1
    msg = "Not a fastapi-mvc project. Try 'fastapi-mvc new --help' for details how to create one."
    assert msg in result.output
