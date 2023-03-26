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
                "lib/generators/foo_bar/update.sh",
                "lib/generators/foo_bar/flake.nix",
                "lib/generators/foo_bar/flake.lock",
                "lib/generators/foo_bar/.generator.yml",
                "lib/generators/foo_bar/template/{{package_name}}/hello_world.py.jinja",
                "lib/generators/foo_bar/.github/dependabot.yml",
                "lib/generators/foo_bar/.github/workflows/update-flake.yml"
            ],
            condition=lambda x: os.path.isfile(x),
        )

    def test_should_generate_generator_with_minimal_structure(self, cli_runner, default_project, monkeypatch):
        # given
        monkeypatch.chdir(default_project)
        result = cli_runner.invoke(GeneratorGenerator, ["--skip-nix", "--skip-actions", "minimal"])

        # then
        assert result.exit_code == 0
        assert_paths(
            [
                "lib/generators/minimal/flake.nix",
                "lib/generators/minimal/flake.lock",
                "lib/generators/minimal/.github/dependabot.yml",
                "lib/generators/minimal/.github/workflows/update-flake.yml"
            ],
            condition=lambda x: not os.path.exists(x),
        )
