import subprocess

import mock
import pytest
from fastapi_mvc import Borg, __version__
from fastapi_mvc.generators import builtins


parser = mock.Mock()
parser.package_name = "test_app"
parser.folder_name = "test-app"
parser.script_name = "test-app"
parser.project_root = "/path/to/project"


@mock.patch("fastapi_mvc.borg.os")
@mock.patch("fastapi_mvc.borg.ShellUtils")
@mock.patch("fastapi_mvc.borg.Invoker")
@mock.patch("fastapi_mvc.borg.IniParser", return_value=parser)
@mock.patch("fastapi_mvc.borg.load_generators")
def test_borg(load_mock, parser_mock, invoker_mock, utils_mock, os_mock):
    # Reset shared state for clean consistent test environment.
    Borg._Borg__shared_state = dict()

    os_mock.path.isdir.return_value = True

    first = Borg()
    assert str(first) == "We are the Borg. You will be assimilated. Resistance is futile."

    assert not first.parser
    assert not first._project_installed
    assert not first._generators_loaded
    assert first.generators == builtins
    assert first.version == __version__

    first.require_project()
    first.load_generators()
    first.require_installed()

    second = Borg()
    assert second.parser == parser
    assert second._project_installed
    assert second.generators != builtins
    assert second._generators_loaded

    second.require_project()
    second.load_generators()
    second.require_installed()

    second.my_attr = "foobar"
    assert first.my_attr == "foobar"

    first.enqueue_command("CMD1")
    second.enqueue_command("CMD2")
    first.enqueue_command("CMD3")
    first.execute()

    load_mock.assert_called_once_with(parser.project_root)
    parser_mock.assert_called_once()
    os_mock.path.isdir.assert_called_once()
    invoker_mock.assert_called_once()
    invoker_mock.return_value.enqueue.assert_has_calls(
        [
            mock.call("CMD1"),
            mock.call("CMD2"),
            mock.call("CMD3"),
        ]
    )
    invoker_mock.return_value.execute.assert_called_once()
    utils_mock.run_shell.assert_called_once_with(
        cmd=[
            "poetry",
            "run",
            parser.script_name,
            "--help",
        ],
        cwd=parser.project_root,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


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


@mock.patch(
    "fastapi_mvc.borg.ShellUtils.run_shell",
    side_effect=subprocess.CalledProcessError(1, [])
)
@mock.patch("fastapi_mvc.borg.os")
@mock.patch("fastapi_mvc.borg.IniParser", return_value=parser)
def test_require_installed_error(parser_mock, os_mock, run_mock):
    # Reset shared state for clean consistent test environment.
    Borg._Borg__shared_state = dict()

    os_mock.path.isdir.return_value = True

    borg = Borg()
    assert not borg.parser
    assert not borg._project_installed

    with pytest.raises(SystemExit):
        borg.require_installed()

    parser_mock.assert_called_once()
    os_mock.path.isdir.assert_called_once()
    run_mock.assert_called_once_with(
        cmd=[
            "poetry",
            "run",
            parser.script_name,
            "--help",
        ],
        cwd=parser.project_root,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


@mock.patch("fastapi_mvc.borg.load_generators")
@mock.patch("fastapi_mvc.borg.os")
@mock.patch("fastapi_mvc.borg.IniParser", return_value=parser)
def test_load_generators(parser_mock, os_mock, load_mock):
    # Reset shared state for clean consistent test environment.
    Borg._Borg__shared_state = dict()

    os_mock.path.isdir.return_value = True

    borg = Borg()
    assert not borg.parser
    assert not borg._generators_loaded

    borg.load_generators()

    parser_mock.assert_called_once()
    os_mock.path.isdir.assert_called_once()
    load_mock.assert_called_once_with(parser.project_root)
    assert borg.parser == parser
    assert borg._generators_loaded
    assert borg.generators != builtins
