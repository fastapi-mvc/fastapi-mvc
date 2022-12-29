import os

from fastapi_mvc.generators import GeneratorGenerator
from tests.integration.conftest import assert_paths


class TestGeneratorGeneratorCli:

    def test_should_generate_generator_with_default_structure(self, cli_runner, default_project, monkeypatch):
        # given
        monkeypatch.chdir(default_project)
        result = cli_runner.invoke(GeneratorGenerator, ["foo-bar"])

        # then
        assert result.exit_code == 0
        assert_paths(
            [
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
            ],
            condition=lambda x: os.path.isfile(x),
        )

    def test_should_generate_generator_with_minimal_structure(self, cli_runner, default_project, monkeypatch):
        # given
        monkeypatch.chdir(default_project)
        result = cli_runner.invoke(GeneratorGenerator, ["--skip-nix", "foo-bar"])

        # then
        assert result.exit_code == 0
        assert_paths(
            [
                "lib/generators/foo_bar/default.nix",
                "lib/generators/foo_bar/shell.nix",
            ],
            condition=lambda x: os.path.exists(x),
        )
