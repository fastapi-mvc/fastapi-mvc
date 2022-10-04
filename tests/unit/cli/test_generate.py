from unittest import mock

import pytest
from fastapi_mvc.cli.generate import get_generate_cmd
from ..data.cli_outputs import (
    generate_root_help,
    generate_controller_help,
    generate_generator_help,
)


parser = mock.Mock()
parser.package_name = "test_app"
parser.folder_name = "test-app"
parser.project_root = "/path/to/project"


@mock.patch("fastapi_mvc.cli.generate.Borg")
def test_generate_help(borg_mock, cli_runner, mock_generators):
    borg_mock.return_value.parser = parser
    borg_mock.return_value.generators = mock_generators

    result = cli_runner.invoke(get_generate_cmd(), ["--help"])
    assert result.exit_code == 0
    assert result.output == generate_root_help

    borg_mock.assert_called_once()
    borg_mock.return_value.load_generators.assert_called_once()


@mock.patch("fastapi_mvc.cli.generate.Borg")
def test_generate_invalid_options(borg_mock, cli_runner):
    result = cli_runner.invoke(get_generate_cmd(), ["--not_exists"])
    assert result.exit_code == 2

    borg_mock.assert_called_once()
    borg_mock.return_value.load_generators.assert_called_once()


@pytest.mark.parametrize(
    "sub_cmd, help_tmpl",
    [
        ("controller", generate_controller_help),
        ("generator", generate_generator_help),
    ],
)
@mock.patch("fastapi_mvc.cli.generate.Borg")
def test_generate_subcommands_help(
    borg_mock, cli_runner, sub_cmd, help_tmpl, mock_generators
):
    borg_mock.return_value.parser = parser
    borg_mock.return_value.generators = mock_generators

    result = cli_runner.invoke(get_generate_cmd(), [sub_cmd, "--help"])
    assert result.exit_code == 0

    usage = borg_mock.return_value.generators[sub_cmd].usage

    with open(usage, "r") as f:
        epilog = f.read()

    assert result.output == help_tmpl.format(usage=epilog.strip())

    borg_mock.assert_called_once()
    borg_mock.return_value.load_generators.assert_called_once()


@pytest.mark.parametrize(
    "sub_cmd, args, expected",
    [
        (
            "controller",
            ["controller", "foobar"],
            {
                "name": "foobar",
                "skip": False,
                "skip_routes": False,
                "endpoints": (),
            },
        ),
        (
            "controller",
            ["controller", "--skip", "--skip-routes", "my_controller"],
            {
                "name": "my_controller",
                "skip": True,
                "skip_routes": True,
                "endpoints": (),
            },
        ),
        (
            "controller",
            ["controller", "-S", "-R", "stock_market", "ticker", "buy:post"],
            {
                "name": "stock_market",
                "skip": True,
                "skip_routes": True,
                "endpoints": (
                    "ticker",
                    "buy:post",
                ),
            },
        ),
        (
            "generator",
            ["generator", "foobar"],
            {
                "name": "foobar",
                "skip": False,
            },
        ),
        (
            "generator",
            ["generator", "--skip", "my_gen"],
            {
                "name": "my_gen",
                "skip": True,
            },
        ),
    ],
)
@mock.patch("fastapi_mvc.cli.generate.RunGenerator")
@mock.patch("fastapi_mvc.cli.generate.Borg")
def test_subcommands_with_options(
    borg_mock, run_gen_mock, cli_runner, sub_cmd, args, expected, mock_generators
):
    borg_mock.return_value.parser = parser
    borg_mock.return_value.generators = mock_generators

    result = cli_runner.invoke(get_generate_cmd(), args)
    assert result.exit_code == 0

    assert borg_mock.call_count == 2
    borg_mock.return_value.load_generators.assert_called_once()
    borg_mock.return_value.require_project.assert_called_once()

    mock_gen = borg_mock.return_value.generators[sub_cmd]
    mock_gen.assert_called_once_with(parser)

    run_gen_mock.assert_called_once_with(
        generator=mock_gen.return_value,
        options=expected,
    )
    borg_mock.return_value.enqueue.assert_called_once_with(run_gen_mock.return_value)
    borg_mock.return_value.execute.assert_called_once()


@mock.patch("fastapi_mvc.cli.generate.Borg")
def test_no_subcommand(borg_mock, cli_runner, mock_generators):
    borg_mock.return_value.parser = parser
    borg_mock.return_value.generators = mock_generators

    result = cli_runner.invoke(get_generate_cmd(), ["notexist", "ARG"])
    assert result.exit_code == 2
    assert "No such generator 'notexist'." in result.output

    borg_mock.assert_called_once()
    borg_mock.return_value.load_generators.assert_called_once()
