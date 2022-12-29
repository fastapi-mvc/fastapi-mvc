import os

from copier.user_data import load_answersfile_data
from tests.integration.conftest import assert_paths
from fastapi_mvc import ANSWERS_FILE
from fastapi_mvc.cli.new import new


class TestCliNewCommand:

    def test_should_generate_new_project_with_default_structure(self, cli_runner):
        with cli_runner.isolated_filesystem() as tmp:
            # given / when
            result = cli_runner.invoke(
                new, ["--skip-install", "--no-interaction", "test-project"]
            )

            # then
            assert result.exit_code == 0
            assert_paths(
                paths=[
                    f"{tmp}/test-project",
                    f"{tmp}/test-project/test_project",
                    f"{tmp}/test-project/test_project/app",
                    f"{tmp}/test-project/test_project/app/controllers",
                    f"{tmp}/test-project/test_project/app/models",
                    f"{tmp}/test-project/test_project/app/views",
                    f"{tmp}/test-project/test_project/app/utils",
                    f"{tmp}/test-project/test_project/app/exceptions",
                    f"{tmp}/test-project/test_project/config",
                    f"{tmp}/test-project/test_project/cli",
                    f"{tmp}/test-project/charts/test-project",
                    f"{tmp}/test-project/manifests",
                    f"{tmp}/test-project/tests",
                    f"{tmp}/test-project/docs",
                    f"{tmp}/test-project/build",
                    f"{tmp}/test-project/.github",
                    f"{tmp}/test-project/.github/workflows",
                    f"{tmp}/test-project/docs",
                    f"{tmp}/test-project/docs",
                    f"{tmp}/test-project/docs",
                    f"{tmp}/test-project/docs",
                    f"{tmp}/test-project/.git",
                ],
                condition=lambda x: os.path.isdir(x),
            )
            assert_paths(
                paths=[
                    f"{tmp}/test-project/build/dev-env.sh",
                    f"{tmp}/test-project/tests/unit/app/utils/test_redis.py",
                    f"{tmp}/test-project/test_project/app/utils/redis.py",
                    f"{tmp}/test-project/tests/unit/app/utils/test_aiohttp_client.py",
                    f"{tmp}/test-project/test_project/app/utils/aiohttp_client.py",
                    f"{tmp}/test-project/shell.nix",
                    f"{tmp}/test-project/image.nix",
                    f"{tmp}/test-project/default.nix",
                    f"{tmp}/test-project/editable.nix",
                    f"{tmp}/test-project/overlay.nix",
                    f"{tmp}/test-project/flake.nix",
                    f"{tmp}/test-project/flake.lock",
                ],
                condition=lambda x: os.path.isfile(x),
            )

    def test_should_generate_new_project_with_minimal_structure(self, cli_runner):
        with cli_runner.isolated_filesystem() as tmp:
            # given / when
            result = cli_runner.invoke(
                new,
                [
                    "--skip-redis",
                    "--skip-aiohttp",
                    "--skip-helm",
                    "--skip-actions",
                    "--skip-install",
                    "--skip-nix",
                    "--no-interaction",
                    "test-project",
                ],
            )

            # then
            assert result.exit_code == 0
            assert_paths(
                paths=[
                    f"{tmp}/test-project/charts",
                    f"{tmp}/test-project/.github",
                    f"{tmp}/test-project/build/dev-env.sh",
                    f"{tmp}/test-project/manifests",
                    f"{tmp}/test-project/tests/unit/app/utils/test_redis.py",
                    f"{tmp}/test-project/test_project/app/utils/redis.py",
                    f"{tmp}/test-project/tests/unit/app/utils/test_aiohttp_client.py",
                    f"{tmp}/test-project/test_project/app/utils/aiohttp_client.py",
                    f"{tmp}/test-project/shell.nix",
                    f"{tmp}/test-project/image.nix",
                    f"{tmp}/test-project/default.nix",
                    f"{tmp}/test-project/editable.nix"
                    f"{tmp}/test-project/overlay.nix",
                    f"{tmp}/test-project/flake.nix",
                    f"{tmp}/test-project/flake.lock",
                ],
                condition=lambda x: not os.path.exists(x),
            )

    def test_should_generate_using_overriden_template(self, cli_runner):
        with cli_runner.isolated_filesystem() as tmp:
            # given / when
            result = cli_runner.invoke(
                new,
                [
                    "--skip-install",
                    "--no-interaction",
                    "--use-repo",
                    "https://github.com/rszamszur/copier-project",
                    "--use-version",
                    "master",
                    "test-project"
                ],
            )

            # then
            assert result.exit_code == 0
            data = load_answersfile_data(f"{tmp}/test-project", ANSWERS_FILE)
            assert data["_commit"] == "82234c2"
            assert data["_src_path"] == "https://github.com/rszamszur/copier-project"

    def test_should_generate_and_install(self, monkeypatch, cli_runner):
        with cli_runner.isolated_filesystem() as tmp:
            # given / when
            monkeypatch.setenv("POETRY_VIRTUALENVS_IN_PROJECT", "true")
            result = cli_runner.invoke(new, ["--no-interaction", "test-project"])

            # then
            assert result.exit_code == 0
            assert_paths(
                paths=[
                    f"{tmp}/test-project/.venv",
                    f"{tmp}/test-project/.venv/bin",
                    f"{tmp}/test-project/.venv/lib",
                ],
                condition=lambda x: os.path.isdir(x),
            )
