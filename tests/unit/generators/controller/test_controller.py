import os
import inspect

import pytest
from unittest import mock
from click import Argument, Option
from fastapi_mvc.generators import ControllerGenerator


CONTROLLER_DIR = os.path.abspath(
    os.path.join(inspect.getfile(ControllerGenerator), "../")
)


parser = mock.Mock()
parser.package_name = "test_app"
parser.folder_name = "test-app"
parser.project_root = "/path/to/project_root"


@pytest.fixture
def gen_obj():
    yield ControllerGenerator(parser=parser)


def test_class_variables():
    assert ControllerGenerator.name == "controller"
    assert ControllerGenerator.template == os.path.join(CONTROLLER_DIR, "template")
    assert ControllerGenerator.usage == os.path.join(CONTROLLER_DIR, "template/USAGE")
    assert ControllerGenerator.category == "Builtins"

    assert len(ControllerGenerator.cli_arguments) == 2
    assert isinstance(ControllerGenerator.cli_arguments[0], Argument)
    assert ControllerGenerator.cli_arguments[0].opts == ["NAME"]
    assert ControllerGenerator.cli_arguments[0].required
    assert ControllerGenerator.cli_arguments[0].nargs == 1
    assert isinstance(ControllerGenerator.cli_arguments[1], Argument)
    assert ControllerGenerator.cli_arguments[1].opts == ["ENDPOINTS"]
    assert not ControllerGenerator.cli_arguments[1].required
    assert ControllerGenerator.cli_arguments[1].nargs == -1

    assert len(ControllerGenerator.cli_options) == 2
    assert isinstance(ControllerGenerator.cli_options[0], Option)
    assert ControllerGenerator.cli_options[0].opts == ["-S", "--skip"]
    assert ControllerGenerator.cli_options[0].help == "Skip files that already exist."
    assert ControllerGenerator.cli_options[0].is_flag
    assert isinstance(ControllerGenerator.cli_options[1], Option)
    assert ControllerGenerator.cli_options[1].opts == ["-R", "--skip-routes"]
    assert ControllerGenerator.cli_options[1].help == "Weather to skip routes entry."
    assert ControllerGenerator.cli_options[1].is_flag


def test_object_attrs(gen_obj):
    assert gen_obj._parser == parser


@pytest.mark.parametrize(
    "kwargs, expected_ctx",
    [
        (
            {
                "name": "test-controller",
                "skip": False,
                "skip_routes": False,
                "endpoints": (),
            },
            {
                "package_name": "test_app",
                "folder_name": "test-app",
                "controller_name": "test_controller",
                "controller_endpoints": {},
                "skip_routes": False,
            },
        ),
        (
            {
                "name": "stock_market",
                "skip": True,
                "skip_routes": True,
                "endpoints": (
                    "ticker",
                    "buy:post",
                    "sell:delete",
                ),
            },
            {
                "package_name": "test_app",
                "folder_name": "test-app",
                "controller_name": "stock_market",
                "controller_endpoints": {
                    "ticker": "get",
                    "buy": "post",
                    "sell": "delete",
                },
                "skip_routes": True,
            },
        ),
    ],
)
@mock.patch("fastapi_mvc.generators.controller.controller.cookiecutter")
def test_new(cookie_mock, kwargs, expected_ctx, gen_obj):
    gen_obj.new(**kwargs)

    cookie_mock.assert_called_once_with(
        gen_obj.template,
        extra_context=expected_ctx,
        output_dir=os.path.abspath(
            os.path.join(
                "/path/to/project_root",
                "../",
            )
        ),
        no_input=True,
        overwrite_if_exists=True,
        skip_if_file_exists=kwargs["skip"],
    )


def test_destroy(gen_obj):
    with pytest.raises(NotImplementedError):
        gen_obj.destroy()
