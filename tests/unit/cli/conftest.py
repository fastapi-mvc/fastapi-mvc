import pytest
import mock
from click.testing import CliRunner
from fastapi_mvc.generators import ControllerGenerator, GeneratorGenerator
from ..data.lib.generators.my_controller.my_controller import MyControllerGenerator
from ..data.lib.generators.foobar.foobar import FoobarGenerator


@pytest.fixture
def cli_runner():
    yield CliRunner()


@pytest.fixture
def mock_generators():
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
    generators = [
        ControllerGenerator,
        GeneratorGenerator,
        FoobarGenerator,
        MyControllerGenerator,
    ]
    mock_gens = dict()
    class_variables = [
        "name",
        "template",
        "usage",
        "category",
        "cli_options",
        "cli_arguments",
        "cli_help",
        "cli_short_help",
        "cli_deprecated",
    ]

    for gen in generators:
        cls_mock = mock.Mock()
        obj_mock = mock.Mock()

        for attr in class_variables:
            setattr(cls_mock, attr, getattr(gen, attr, None))
            setattr(obj_mock, attr, getattr(gen, attr, None))

        with open(cls_mock.usage, "r") as f:
            cls_mock.read_usage.return_value = f.read()

        cls_mock.return_value = obj_mock
        mock_gens[cls_mock.name] = cls_mock

    yield mock_gens
