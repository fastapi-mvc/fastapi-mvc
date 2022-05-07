import os
import inspect

import pytest
import mock
from fastapi_mvc.generators import GeneratorGenerator, Generator


CONTROLLER_DIR = os.path.abspath(
    os.path.join(inspect.getfile(GeneratorGenerator), "../")
)


parser = mock.Mock()
parser.package_name = "test_app"
parser.folder_name = "test-app"
parser.project_root = "/path/to/project_root"


@pytest.fixture
def gen_obj():
    yield GeneratorGenerator(parser=parser)


def test_class_variables():
    assert GeneratorGenerator.name == "generator"
    assert GeneratorGenerator.template == os.path.join(CONTROLLER_DIR, "template")
    assert GeneratorGenerator.usage == os.path.join(CONTROLLER_DIR, "template/USAGE")
    assert GeneratorGenerator.category == "Builtins"
    assert GeneratorGenerator.cli_arguments == Generator.cli_arguments
    assert GeneratorGenerator.cli_options == Generator.cli_options


def test_object_attrs(gen_obj):
    assert gen_obj._parser == parser
    assert gen_obj._builtins == ["controller", "generator"]


@pytest.mark.parametrize(
    "kwargs, expected_ctx",
    [
        (
            {
                "name": "test-generator",
                "skip": False,
            },
            {
                "package_name": "test_app",
                "folder_name": "test-app",
                "generator_name": "test_generator",
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
        ),
    ],
)
@mock.patch("fastapi_mvc.generators.generator.generator.cookiecutter")
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


@pytest.mark.parametrize(
    "kwargs",
    [
        {
            "name": "controller",
            "skip": False,
        },
        {
            "name": "generator",
            "skip": False,
        },
    ],
)
@mock.patch("fastapi_mvc.generators.generator.generator.cookiecutter")
def test_new_invalid(cookie_mock, kwargs, gen_obj):
    with pytest.raises(SystemExit) as ex:
        gen_obj.new(**kwargs)
        assert ex.value.code == 1

    cookie_mock.assert_not_called()


def test_destroy(gen_obj):
    with pytest.raises(NotImplementedError):
        gen_obj.destroy()
