import os

from fastapi_mvc.cli.new import new


def assert_paths(paths, condition):
    for path in paths:
        assert condition(path)


def test_new_default_project(cli_runner):
    with cli_runner.isolated_filesystem() as tmp:
        result = cli_runner.invoke(
            new, ["--skip-install", "--no-interaction", "test-project"]
        )
        assert result.exit_code == 0

        dirs = [
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
        ]
        assert_paths(dirs, condition=lambda x: os.path.isdir(x))


def test_new_project_minmal(cli_runner):
    with cli_runner.isolated_filesystem() as tmp:
        cli_runner.invoke(
            new,
            result=cli_runner.invoke(
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
            ),
        )

        paths = [
            "charts",
            ".github",
            "build/dev-env.sh",
            "manifests",
            "tests/unit/app/utils/test_redis.py",
            "test_project/app/utils/redis.py",
            "tests/unit/app/utils/test_aiohttp_client.py",
            "test_project/app/utils/aiohttp_client.py",
            "shell.nix",
            "image.nix",
            "default.nix",
            "overlay.nix",
            "Nix.mk",
        ]
        assert_paths(paths, lambda x: not os.path.exists(x))
