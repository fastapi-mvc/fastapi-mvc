"""Unit tests suite for fastapi-mvc generate command.

Note:
    CLI generate command (DynamicMultiCommand) needs to be shallow copied
    because otherwise, it will be initialized only once for all tests cases
    (provided they were not executed separately). For other click CLI commands
    this might be no factor. But DynamicMultiCommand uses fastapi-mvc generators
    data to programmatically generate CLI subcommands, which happens once. Thus
    it shallow copied into cli_runner.invoke().

"""
import os
from copy import copy

import mock
import pytest
from fastapi_mvc.cli.generate import generate
from fastapi_mvc.exceptions import FileError
from fastapi_mvc.generators import ControllerGenerator, GeneratorGenerator
from ..data.cli_outputs import (
    generate_root_help,
    generate_controller_help,
    generate_generator_help,
)
from ..data.lib.generators.my_controller.my_controller import MyControllerGenerator
from ..data.lib.generators.foobar.foobar import FoobarGenerator


DATA_DIR = os.path.abspath(
    os.path.join(
        os.path.abspath(__file__),
        "../../data",
    )
)


def mock_generators_factory(only_builtins=False):
    """Create mocks based on builtins generators.

    Programmatically creating generators mocks to unit test programmatically
    generated CLI subcommands based on generators classes (in this case created mocks).

    I know what you're thinking, this shouldn't be that complex the first place.
    Me to :D!

    Thing is, programmatically generated CLI uses class attributes
    (or class variables if you will) to create `click.Command` objects, without the need
    to create a concrete generator class object instance. It doesn't make sense to have X
    generators objects if you will at most use only one. Unfortunately mock doesn't have any
    magic tool/function to inherit data from mock object created out of mock
    object which kinda imitates class.

    """
    generators = [ControllerGenerator, GeneratorGenerator]
    mock_gens = dict()
    class_variables = [
        "name",
        "template",
        "usage",
        "category",
        "cli_options",
        "cli_arguments",
    ]

    if not only_builtins:
        generators.append(FoobarGenerator)
        generators.append(MyControllerGenerator)

    for gen in generators:
        cls_mock = mock.Mock()
        obj_mock = mock.Mock()

        for attr in class_variables:
            setattr(cls_mock, attr, getattr(gen, attr, None))
            setattr(obj_mock, attr, getattr(gen, attr, None))

        cls_mock.return_value = obj_mock
        mock_gens[cls_mock.name] = cls_mock

    return mock_gens


parser = mock.Mock()
parser.package_name = "test_app"
parser.folder_name = "test-app"
parser.project_root = "/path/to/project"


@mock.patch("fastapi_mvc.cli.generate.Borg")
def test_generate_help(borg_mock, cli_runner):
    borg_mock.return_value.parser = parser
    borg_mock.return_value.generators = mock_generators_factory()

    result = cli_runner.invoke(copy(generate), ["--help"])
    assert result.exit_code == 0
    assert result.output == generate_root_help

    borg_mock.assert_called_once()
    borg_mock.return_value.load_generators.assert_called_once()


@mock.patch("fastapi_mvc.cli.generate.Borg")
def test_generate_invalid_options(borg_mock, cli_runner):
    result = cli_runner.invoke(copy(generate), ["--not_exists"])
    assert result.exit_code == 2

    borg_mock.assert_not_called()


@pytest.mark.parametrize("sub_cmd, help_tmpl", [
    (
        "controller",
        generate_controller_help
    ),
    (
        "generator",
        generate_generator_help
    ),
])
@mock.patch("fastapi_mvc.cli.generate.Borg")
def test_generate_subcommands_help(borg_mock, cli_runner, sub_cmd, help_tmpl):
    borg_mock.return_value.parser = parser
    borg_mock.return_value.generators = mock_generators_factory()

    result = cli_runner.invoke(copy(generate), [sub_cmd, "--help"])
    assert result.exit_code == 0

    usage = borg_mock.return_value.generators[sub_cmd].usage

    with open(usage, "r") as f:
        epilog = f.read()

    assert result.output == help_tmpl.format(
        usage=epilog.strip()
    )

    borg_mock.assert_called_once()
    borg_mock.return_value.load_generators.assert_called_once()


@mock.patch("fastapi_mvc.cli.generate.Borg")
def test_subcommands_no_project(borg_mock, cli_runner):
    borg_mock.return_value.parser = parser
    borg_mock.return_value.load_generators.side_effect = FileError("Ups")

    result = cli_runner.invoke(copy(generate), ["controller", "--help"])
    assert result.exit_code == FileError.code

    borg_mock.assert_called_once()
    borg_mock.return_value.load_generators.assert_called_once()


@pytest.mark.parametrize("sub_cmd, args, expected", [
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
    )
])
@mock.patch("fastapi_mvc.cli.generate.Borg")
def test_subcommands_with_options(borg_mock, cli_runner, sub_cmd, args, expected):
    borg_mock.return_value.parser = parser
    borg_mock.return_value.generators = mock_generators_factory()

    result = cli_runner.invoke(copy(generate), args)
    assert result.exit_code == 0

    assert borg_mock.call_count == 2
    borg_mock.return_value.load_generators.assert_called_once()

    mock_gen = borg_mock.return_value.generators[sub_cmd]
    mock_gen.return_value.new.assert_called_once_with(**expected)


@mock.patch("fastapi_mvc.cli.generate.Borg")
def test_no_subcommand(borg_mock, cli_runner):
    borg_mock.return_value.parser = parser
    borg_mock.return_value.generators = mock_generators_factory()

    result = cli_runner.invoke(copy(generate), ["notexist", "ARG"])
    assert result.exit_code == 2
    assert "No such generator 'notexist'." in result.output

    borg_mock.assert_called_once()
    borg_mock.return_value.load_generators.assert_called_once()
