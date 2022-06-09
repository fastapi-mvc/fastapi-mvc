import os

from fastapi_mvc.generators import GeneratorGenerator


def test_generator_cookiecutter(cookies):
    result = cookies.bake(
        template=GeneratorGenerator.template,
        extra_context={
            "package_name": "test_project",
            "folder_name": "test-project",
            "generator_name": "foo_bar",
            "class_name": "FooBarGenerator",
        },
    )

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_path.name == "test-project"
    assert result.project_path.is_dir()

    paths = [
        "lib/generators/foo_bar/foo_bar.py",
        "lib/generators/foo_bar/__init__.py",
        "lib/generators/foo_bar/template/USAGE",
        "lib/generators/foo_bar/template/hooks",
        "lib/generators/foo_bar/template/cookiecutter.json",
        "lib/generators/foo_bar/template/{{cookiecutter.folder_name}}",
        "lib/generators/foo_bar/template/{{cookiecutter.folder_name}}/{{cookiecutter.package_name}}",
    ]

    for path in paths:
        assert os.path.exists(
            os.path.join(result.project_path, path),
        )
