import os

import pytest
import mock
from click.testing import CliRunner
from fastapi_mvc import Borg
from fastapi_mvc.generators import ProjectGenerator


DATA_DIR = os.path.abspath(
    os.path.join(
        os.path.abspath(__file__),
        "../../data",
    )
)


def create_mock_generators(generators):
    """Create mocks based on builtins and test generators.

    Programmatically creating generators mocks to unit test programmatically
    generated CLI subcommands based on generators classes (in this case created mocks).

    I know what you're thinking, this shouldn't be that complex the first place.
    Me to :D!

    Thing is, programmatically generated CLI uses class variables
    (or class attributes if you will) to create `click.Command` objects, without the need
    to create a concrete generator class object instance. It doesn't make sense to have X
    generators objects if you will at most use only one. Unfortunately mock doesn't have any
    magic tool/function to inherit data from mock object created out of mock
    object which kinda imitates class.

    Args:
        generators (typing.List[Generator]): List of generators to mock.

    Returns:
        typing.Dict[str, mock.Mock]: Mocks generators.

    """
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

        if cls_mock.usage:
            with open(cls_mock.usage, "r") as f:
                cls_mock.read_usage.return_value = f.read()

        cls_mock.return_value = obj_mock
        mock_gens[cls_mock.name] = cls_mock

    return mock_gens


@pytest.fixture
def cli_runner():
    yield CliRunner()


@pytest.fixture
def mock_generators():
    # Reset shared state for clean consistent test environment.
    Borg._Borg__shared_state = dict()

    borg = Borg()
    borg.import_paths.clear()
    borg.import_paths.add(os.path.join(DATA_DIR, "lib/generators"))
    borg.load_generators()

    yield create_mock_generators(borg.generators.values())


@pytest.fixture
def mock_project_gen():
    yield create_mock_generators([ProjectGenerator])[ProjectGenerator.name]
