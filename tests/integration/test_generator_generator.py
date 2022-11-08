import os

from fastapi_mvc.cli.generate import get_generate_cmd
from fastapi_mvc.generators import generator


def assert_paths(paths, condition):
    for path in paths:
        assert condition(path)


def test_generator(cli_runner, fake_project, monkeypatch):
    monkeypatch.chdir(fake_project)
    result = cli_runner.invoke(
        generator,
        ["foo-bar"],
    )
    assert result.exit_code == 0

    paths = [
        "lib/generators/foo_bar/foo_bar.py",
        "lib/generators/foo_bar/__init__.py",
        "lib/generators/foo_bar/.envrc",
        "lib/generators/foo_bar/.gitignore",
        "lib/generators/foo_bar/CHANGELOG.md",
        "lib/generators/foo_bar/README.md",
        "lib/generators/foo_bar/copier.yml",
        "lib/generators/foo_bar/poetry.lock",
        "lib/generators/foo_bar/pyproject.toml",
        "lib/generators/foo_bar/update.sh",
        "lib/generators/foo_bar/default.nix",
        "lib/generators/foo_bar/shell.nix",
        "lib/generators/foo_bar/.generator.yml",
        "lib/generators/foo_bar/template/{{package_name}}/hello_world.py.jinja",
    ]

    assert_paths(paths, condition=lambda x: os.path.isfile(x))
    result = cli_runner.invoke(get_generate_cmd(), ["foo-bar", "dummy"])
    assert result.exit_code == 0
    assert os.path.isfile("test_project/hello_world.py")
