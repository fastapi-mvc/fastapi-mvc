import os

import pytest
from click.testing import CliRunner
from fastapi_mvc.cli.new import new


def assert_paths(paths, condition):
    for path in paths:
        assert condition(path)


@pytest.fixture(scope="session")
def cli_runner():
    yield CliRunner(
        env={
            "POETRY_HOME": os.getenv("POETRY_HOME", default="/tmp/poetry"),
            "POETRY_CONFIG_DIR": os.getenv("POETRY_CONFIG_DIR", default="/tmp/poetry"),
            "POETRY_VIRTUALENVS_PATH": os.getenv("POETRY_VIRTUALENVS_PATH", default="/tmp/poetry/store"),
        },
    )


@pytest.fixture(scope="session")
def default_project(tmp_path_factory, cli_runner):
    tmp_dir = tmp_path_factory.mktemp("projects")
    root_dir = tmp_dir / "default-project"
    cli_runner.invoke(new, ["--skip-install", "--no-interaction", str(root_dir)])

    return root_dir
