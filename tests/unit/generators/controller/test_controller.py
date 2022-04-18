import os
import inspect

import pytest
import mock
from fastapi_mvc.generators import ControllerGenerator


CONTROLLER_DIR = os.path.abspath(
    os.path.join(
        inspect.getfile(ControllerGenerator),
        "../"
    )
)


@pytest.fixture
def gen_obj():
    parser = mock.Mock()
    parser.package_name = "test_app"
    parser.folder_name = "test-app"

    gen = ControllerGenerator(
        parser=parser,
        project_root="/path/to/project_root"
    )

    yield gen


def test_class_attrs():
    assert ControllerGenerator.name == "controller"
    assert ControllerGenerator.template == os.path.join(
        CONTROLLER_DIR,
        "template"
    )
    assert ControllerGenerator.usage == os.path.join(
        CONTROLLER_DIR,
        "template/USAGE"
    )
    assert ControllerGenerator.cli_arguments == [
        {
            "param_decls": ["NAME"],
            "required": True,
            "nargs": 1,
        },
        {
            "param_decls": ["ENDPOINTS"],
            "required": False,
            "nargs": -1,
        },
    ]
    assert ControllerGenerator.cli_options == [
        {
            "param_decls": ["-S", "--skip"],
            "is_flag": True,
            "help": "Skip files that already exist.",
        },
        {
            "param_decls": ["-R", "--skip-routes"],
            "is_flag": True,
            "help": "Wether to skip routes entry",
        },
    ]


def test_object_attrs(gen_obj):
    assert gen_obj._project_root == "/path/to/project_root"
    assert gen_obj._context == {
        "package_name": "test_app",
        "folder_name": "test-app",
    }


@pytest.mark.parametrize("kwargs, expected_ctx", [
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
            "controller_name": "test-controller",
            "controller_endpoints": {},
            "skip_routes": False
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
            )
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
            "skip_routes": True
        },
    )
])
@mock.patch("fastapi_mvc.generators.controller.controller.cookiecutter")
def test_new(cookie_mock, kwargs, expected_ctx, gen_obj):
    gen_obj.new(**kwargs)

    cookie_mock.assert_called_once_with(
        gen_obj.template,
        extra_context=expected_ctx,
        output_dir=os.path.abspath(
            os.path.join(
                gen_obj._project_root,
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
