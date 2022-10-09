import os
from unittest import mock

import pytest
from fastapi_mvc.cli.generate import get_generate_cmd
from fastapi_mvc.generators import controller, generator
from ..data.lib.generators.foobar import foobar
from ..data.lib.generators.my_controller import my_controller


generators = {
    "controller": controller,
    "generator": generator,
    "foobar": foobar,
    "my-controller": my_controller,
}


@mock.patch("fastapi_mvc.cli.generate.load_generators", return_value=generators)
def test_generate_help(load_mock, cli_runner):
    result = cli_runner.invoke(get_generate_cmd(), ["--help"])
    assert result.exit_code == 0
    load_mock.assert_called_once()


def test_generate_invalid_options(cli_runner):
    result = cli_runner.invoke(get_generate_cmd(), ["--not_exists"])
    assert result.exit_code == 2


@pytest.mark.parametrize(
    "name",
    [
        "controller",
        "generator",
        "foobar",
        "my-controller",
    ],
)
@mock.patch("fastapi_mvc.cli.generate.load_generators", return_value=generators)
def test_generate_subcommands(load_mock, cli_runner, name):
    result = cli_runner.invoke(get_generate_cmd(), [name, "--help"])
    assert result.exit_code == 0
    load_mock.assert_called_once()


@mock.patch("fastapi_mvc.cli.generate.load_generators", return_value=generators)
def test_generate_invalid_subcommand(load_mock, cli_runner):
    result = cli_runner.invoke(get_generate_cmd(), ["notexist", "--help"])
    assert result.exit_code == 2
    assert "No such generator 'notexist'." in result.output
    load_mock.assert_called_once()
