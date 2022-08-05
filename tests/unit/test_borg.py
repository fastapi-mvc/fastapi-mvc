import os

from unittest import mock
import pytest
from fastapi_mvc import Borg, __version__
from fastapi_mvc.generators import Generator


DATA_DIR = os.path.abspath(
    os.path.join(
        os.path.abspath(__file__),
        "../data",
    )
)

parser = mock.Mock()
parser.package_name = "test_app"
parser.folder_name = "test-app"
parser.script_name = "test-app"
parser.project_root = "/path/to/project"


@mock.patch("fastapi_mvc.borg.os.path.isdir", return_value=True)
@mock.patch("fastapi_mvc.borg.os.getenv", return_value="/custom/poetry")
@mock.patch("fastapi_mvc.borg.os.getcwd", return_value=DATA_DIR)
@mock.patch("fastapi_mvc.borg.Invoker")
@mock.patch("fastapi_mvc.borg.IniParser", return_value=parser)
def test_borg(parser_mock, invoker_mock, getcwd_mock, getenv_mock, isdir_mock):
    # Reset shared state for clean consistent test environment.
    Borg._Borg__shared_state = dict()

    first = Borg()

    assert (
        str(first) == "We are the Borg. You will be assimilated. Resistance is futile."
    )
    assert not first.parser
    assert sorted(first.generators.keys()) == ["controller", "generator"]
    assert issubclass(first.generators["controller"], Generator)
    assert first.generators["controller"].__name__ == "ControllerGenerator"
    assert issubclass(first.generators["generator"], Generator)
    assert first.generators["generator"].__name__ == "GeneratorGenerator"
    assert first.version == __version__
    assert first.poetry_path == "/custom/poetry/bin/poetry"

    first.require_project()
    first.load_generators()

    second = Borg()
    assert second.parser == parser
    assert sorted(second.generators.keys()) == sorted(
        ["controller", "foobar", "generator", "MyControllerGenerator"]
    )
    assert issubclass(second.generators["controller"], Generator)
    assert second.generators["controller"].__name__ == "ControllerGenerator"
    assert issubclass(second.generators["generator"], Generator)
    assert second.generators["generator"].__name__ == "GeneratorGenerator"
    assert issubclass(second.generators["MyControllerGenerator"], Generator)
    assert (
        second.generators["MyControllerGenerator"].__name__ == "MyControllerGenerator"
    )
    assert issubclass(second.generators["foobar"], Generator)
    assert second.generators["foobar"].__name__ == "FoobarGenerator"
    assert len(second._imported_paths) == 2
    assert "/path/to/project/lib/generators" in second._imported_paths
    assert "{0:s}/lib/generators".format(DATA_DIR) in second._imported_paths
    assert second.poetry_path == "/custom/poetry/bin/poetry"
    assert first.__dict__ == second.__dict__

    second.require_project()
    second.load_generators()

    second.my_attr = "foobar"
    assert first.my_attr == "foobar"

    first.enqueue("CMD1")
    second.enqueue("CMD2")
    first.enqueue("CMD3")
    first.execute()

    parser_mock.assert_called_once()
    getcwd_mock.assert_called_once()
    getenv_mock.assert_has_calls(
        [
            mock.call("HOME"),
            mock.call("POETRY_HOME", "/custom/poetry/.poetry"),
            mock.call("HOME"),
            mock.call("POETRY_HOME", "/custom/poetry/.poetry"),
        ]
    )
    isdir_mock.assert_any_call("/path/to/project/test_app")
    invoker_mock.assert_called_once()
    invoker_mock.return_value.enqueue.assert_has_calls(
        [
            mock.call("CMD1"),
            mock.call("CMD2"),
            mock.call("CMD3"),
        ]
    )
    invoker_mock.return_value.execute.assert_called_once()


@mock.patch("fastapi_mvc.borg.IniParser", side_effect=FileNotFoundError("Ups"))
def test_require_project_parser_error(parser_mock):
    # Reset shared state for clean consistent test environment.
    Borg._Borg__shared_state = dict()

    borg = Borg()
    assert not borg.parser

    with pytest.raises(SystemExit):
        borg.require_project()

    parser_mock.assert_called_once()


@mock.patch("fastapi_mvc.borg.os")
@mock.patch("fastapi_mvc.borg.IniParser", return_value=parser)
def test_require_project_files_error(parser_mock, os_mock):
    # Reset shared state for clean consistent test environment.
    Borg._Borg__shared_state = dict()

    os_mock.path.isdir.return_value = False
    os_mock.path.join.return_value = "/test/path"

    borg = Borg()
    assert not borg.parser

    with pytest.raises(SystemExit):
        borg.require_project()

    parser_mock.assert_called_once()
    os_mock.path.isdir.assert_called_once()


@mock.patch("fastapi_mvc.borg.os.getcwd", return_value=DATA_DIR)
def test_load_generators(getcwd_mock):
    # Reset shared state for clean consistent test environment.
    Borg._Borg__shared_state = dict()

    borg = Borg()
    assert len(borg._import_paths) == 1
    assert "{0:s}/lib/generators".format(DATA_DIR) in borg._import_paths
    assert not borg._imported_paths
    assert "MyControllerGenerator" not in borg.generators
    assert "foobar" not in borg.generators
    getcwd_mock.assert_called_once()

    borg.load_generators()

    assert sorted(borg.generators.keys()) == sorted(
        ["controller", "foobar", "generator", "MyControllerGenerator"]
    )
    assert issubclass(borg.generators["MyControllerGenerator"], Generator)
    assert borg.generators["MyControllerGenerator"].__name__ == "MyControllerGenerator"
    assert issubclass(borg.generators["foobar"], Generator)
    assert borg.generators["foobar"].__name__ == "FoobarGenerator"
    assert len(borg._imported_paths) == 1
    assert "{0:s}/lib/generators".format(DATA_DIR) in borg._imported_paths


@mock.patch("fastapi_mvc.borg.importlib.util")
@mock.patch("fastapi_mvc.borg.os.getcwd", return_value=DATA_DIR)
def test_load_generators_error(getcwd_mock, importlib_mock):
    # Reset shared state for clean consistent test environment.
    Borg._Borg__shared_state = dict()

    spec_mock = mock.Mock()
    spec_mock.loader.exec_module.side_effect = ImportError("Ups")
    importlib_mock.spec_from_file_location.return_value = spec_mock

    borg = Borg()

    assert len(borg._import_paths) == 1
    assert "{0:s}/lib/generators".format(DATA_DIR) in borg._import_paths
    assert not borg._imported_paths
    assert "MyControllerGenerator" not in borg.generators
    assert "foobar" not in borg.generators
    getcwd_mock.assert_called_once()

    borg.load_generators()

    assert "MyControllerGenerator" not in borg.generators
    assert "foobar" not in borg.generators
    assert len(borg._imported_paths) == 1
    assert "{0:s}/lib/generators".format(DATA_DIR) in borg._imported_paths
