import os
from unittest import mock

import pytest
from fastapi_mvc.generators import ScriptGenerator


DATA_DIR = os.path.abspath(
    os.path.join(
        os.path.abspath(__file__),
        "../../data",
    )
)


def test_script_help(cli_runner):
    result = cli_runner.invoke(ScriptGenerator, ["--help"])
    assert result.exit_code == 0


def test_script_invalid_options(cli_runner):
    result = cli_runner.invoke(ScriptGenerator, ["--not_exists"])
    assert result.exit_code == 2


@mock.patch("fastapi_mvc.generators.script.Generator.run_copy")
def test_script_default_values(copier_mock, monkeypatch, cli_runner):
    # Change working directory to fake project. It is easier to fake fastapi-mvc project,
    # rather than mocking ctx injected to command via @click.pass_context decorator.
    monkeypatch.chdir(DATA_DIR)

    result = cli_runner.invoke(ScriptGenerator, ["custom-script.sh"])
    assert result.exit_code == 0

    copier_mock.assert_called_once_with(
        data={
            "nix": False,
            "script": "custom-script.sh",
        },
        answers_file=None,
    )


@pytest.mark.parametrize(
    "args, expected",
    [
        (
            [
                "-n",
                "Mambo-No6",
            ],
            {
                "data": {
                    "nix": True,
                    "script": "mambo-no6",
                },
                "answers_file": None,
            },
        )
    ],
)
@mock.patch("fastapi_mvc.generators.script.Generator.run_copy")
def test_script_with_options(copier_mock, monkeypatch, cli_runner, args, expected):
    # Change working directory to fake project. It is easier to fake fastapi-mvc project,
    # rather than mocking ctx injected to command via @click.pass_context decorator.
    monkeypatch.chdir(DATA_DIR)

    result = cli_runner.invoke(ScriptGenerator, args)
    assert result.exit_code == 0

    copier_mock.assert_called_once_with(**expected)
