import os
import inspect

import pytest
import mock
from fastapi_mvc.generators import GeneratorGenerator


CONTROLLER_DIR = os.path.abspath(
    os.path.join(
        inspect.getfile(GeneratorGenerator),
        "../"
    )
)


@pytest.fixture
def gen_obj():
    parser = mock.Mock()
    parser.package_name = "test_app"
    parser.folder_name = "test-app"

    gen = GeneratorGenerator(
        parser=parser,
        project_root="/path/to/project_root"
    )

    yield gen


def test_class_attrs():
    assert GeneratorGenerator.name == "generator"
    assert GeneratorGenerator.template == os.path.join(
        CONTROLLER_DIR,
        "template"
    )
    assert GeneratorGenerator.usage == os.path.join(
        CONTROLLER_DIR,
        "template/USAGE"
    )
    assert GeneratorGenerator.cli_arguments == [
        {
            "param_decls": ["NAME"],
            "required": True,
            "nargs": 1,
        },
    ]
    assert GeneratorGenerator.cli_options == [
        {
            "param_decls": ["-S", "--skip"],
            "is_flag": True,
            "help": "Skip files that already exist.",
        },
    ]


def test_object_attrs(gen_obj):
    assert gen_obj._project_root == "/path/to/project_root"
    assert gen_obj._context == {
        "package_name": "test_app",
        "folder_name": "test-app",
    }
    assert gen_obj._builtins == ["controller", "generator"]


@pytest.mark.parametrize("kwargs, expected_ctx", [
    (
        {
            "name": "test-generator",
            "skip": False,
        },
        {
            "package_name": "test_app",
            "folder_name": "test-app",
            "generator_name": "test-generator",
            "class_name": "TestGeneratorGenerator",
        },
    ),
    (
        {
            "name": "scaffold",
            "skip": True,
        },
        {
            "package_name": "test_app",
            "folder_name": "test-app",
            "generator_name": "scaffold",
            "class_name": "ScaffoldGenerator",
        },
    )
])
@mock.patch("fastapi_mvc.generators.generator.generator.cookiecutter")
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


@pytest.mark.parametrize("kwargs", [
    {
        "name": "controller",
        "skip": False,
    },
    {
        "name": "generator",
        "skip": False,
    }
])
@mock.patch("fastapi_mvc.generators.generator.generator.cookiecutter")
def test_new_invalid(cookie_mock, kwargs, gen_obj):
    with pytest.raises(SystemExit) as ex:
        gen_obj.new(**kwargs)
        assert ex.value.code == 1

    cookie_mock.assert_not_called()


def test_destroy(gen_obj):
    with pytest.raises(NotImplementedError):
        gen_obj.destroy()
