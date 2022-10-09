import os
from unittest import mock

import pytest
from fastapi_mvc.generators import load_generators


DATA_DIR = os.path.abspath(
    os.path.join(
        os.path.abspath(__file__),
        "../../data",
    )
)


@mock.patch("fastapi_mvc.generators.loader.os.getcwd", return_value=DATA_DIR)
def test_load_generators(getcwd_mock):
    generators = load_generators()
    getcwd_mock.assert_called_once()

    assert sorted(generators.keys()) == sorted(
        ["controller", "foobar", "generator", "my-controller"]
    )


@mock.patch("fastapi_mvc.generators.loader.importlib.util")
@mock.patch("fastapi_mvc.generators.loader.os.getcwd", return_value=DATA_DIR)
def test_load_generators_error(getcwd_mock, importlib_mock):
    spec_mock = mock.Mock()
    spec_mock.loader.exec_module.side_effect = ImportError("Ups")
    importlib_mock.spec_from_file_location.return_value = spec_mock

    generators = load_generators()

    assert sorted(generators.keys()) == sorted(["controller", "generator"])
