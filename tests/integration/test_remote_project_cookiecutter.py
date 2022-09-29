import os
import pytest

from click.testing import CliRunner
from fastapi_mvc.cli.new import get_new_cmd


@pytest.fixture
def cli_runner():
    yield CliRunner()


def test_project_cookiecutter(cli_runner, tmp_path):
    app_path = f"{tmp_path}/test-project"
    result = cli_runner.invoke(get_new_cmd(), ["--skip-install", app_path])
    assert result.exit_code == 0

    assert os.path.exists(app_path)
    assert os.path.isdir(app_path)


def test_project_cookiecutter_minimal(cli_runner, tmp_path):
    app_path = f"{tmp_path}/test-project"
    result = cli_runner.invoke(
        get_new_cmd(),
        [
            "-R",
            "-A",
            "-H",
            "-G",
            "-I",
            "-N",
            "--license",
            "ISC",
            "--repo-url",
            "https://test.repo",
            app_path
        ],
    )
    assert result.exit_code == 0

    assert os.path.exists(app_path)
    assert os.path.isdir(app_path)

    paths = [
        "charts",
        ".github",
        "build/dev-env.sh",
        "manifests",
        "tests/unit/app/utils/test_aiohttp_client.py",
        "test_project/app/utils/aiohttp_client.py",
        "shell.nix",
        "image.nix",
        "default.nix",
        "overlay.nix",
        "Nix.mk",
    ]

    for path in paths:
        assert not os.path.exists(
            os.path.join(app_path, path),
        )
