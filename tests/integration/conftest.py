import os
import copy

import pytest
from click.testing import CliRunner
from fastapi_mvc.cli.new import new
from fastapi_mvc.cli.update import update


COPIER_PROJECT_RELEASES = {
    "0.1.0",
    "0.1.1",
    "0.2.0",
    "0.3.0",
    "0.4.0",
}


def assert_paths(paths, condition):
    for path in paths:
        assert condition(path)


@pytest.fixture
def new_copy():
    new_copy = copy.deepcopy(new)
    yield new_copy
    del new_copy


@pytest.fixture
def update_copy():
    update_copy = copy.deepcopy(update)
    yield update_copy
    del update_copy


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
    result = cli_runner.invoke(
        copy.deepcopy(new),
        ["--skip-install", "--no-interaction", f"{root_dir}"],
    )
    # make sure project was generated successfully
    assert result.exit_code == 0

    return root_dir


@pytest.fixture(scope="session")
def reference_projects(tmp_path_factory, cli_runner):
    tmp_dir = tmp_path_factory.mktemp("releases")
    projects = dict()

    for release in COPIER_PROJECT_RELEASES:
        project_dir = tmp_dir / release / "update-test"
        project_dir.mkdir(parents=True)
        result = cli_runner.invoke(
            copy.deepcopy(new),
            [
                "--skip-install",
                "--no-interaction",
                "--use-version",
                release,
                str(project_dir),
            ]
        )
        # make sure project was generated successfully
        assert result.exit_code == 0

        projects[release] = project_dir

    return projects
