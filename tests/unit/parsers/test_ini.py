import os

import mock
import pytest
from fastapi_mvc.parsers import IniParser


DATA_DIR = os.path.abspath(
    os.path.join(
        os.path.abspath(__file__),
        "../../data",
    )
)


@pytest.fixture
def parser():
    yield IniParser(DATA_DIR)


def test_parser_properties(parser):
    assert parser.project_root == DATA_DIR
    assert parser.folder_name == "test-app"
    assert parser.package_name == "test_app"
    assert parser.script_name == "test-app"
    assert parser.helm == "yes"
    assert parser.chart_name == "test-app"
    assert parser.redis == "yes"
    assert parser.github_actions == "yes"
    assert parser.version == "x.y.z"

    with mock.patch("fastapi_mvc.parsers.ini.os.getcwd") as mck:
        mck.return_value = DATA_DIR

        default = IniParser()
        assert default.project_root == DATA_DIR


@mock.patch("fastapi_mvc.parsers.ini.os.path.exists", return_value=False)
def test_parser_ini_not_exists(exists_mock):
    with pytest.raises(FileNotFoundError) as ex:
        IniParser("/test/path")
        assert str(ex) == "/test/path/fastapi-mvc.ini does not exist."

    exists_mock.assert_called_once_with("/test/path/fastapi-mvc.ini")


@mock.patch("fastapi_mvc.parsers.ini.os.path.isfile", return_value=False)
@mock.patch("fastapi_mvc.parsers.ini.os.path.exists", return_value=True)
def test_parser_ini_not_a_file(exists_mock, isfile_mock):
    with pytest.raises(IsADirectoryError) as ex:
        IniParser("/test/path")
        assert str(ex) == "/test/path/fastapi-mvc.ini is not a file."

    exists_mock.assert_called_once_with("/test/path/fastapi-mvc.ini")
    isfile_mock.assert_called_once_with("/test/path/fastapi-mvc.ini")


@mock.patch("fastapi_mvc.parsers.ini.os.access", return_value=False)
@mock.patch("fastapi_mvc.parsers.ini.os.path.isfile", return_value=True)
@mock.patch("fastapi_mvc.parsers.ini.os.path.exists", return_value=True)
def test_parser_ini_not_readable(exists_mock, isfile_mock, access_mock):
    with pytest.raises(PermissionError) as ex:
        IniParser("/test/path")
        assert str(ex) == "/test/path/fastapi-mvc.ini is not readable."

    exists_mock.assert_called_once_with("/test/path/fastapi-mvc.ini")
    isfile_mock.assert_called_once_with("/test/path/fastapi-mvc.ini")
    access_mock.assert_called_once_with("/test/path/fastapi-mvc.ini", os.R_OK)
