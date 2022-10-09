import pytest
from click.testing import CliRunner
from fastapi_mvc.cli.new import new


content = """\
# Changes here will be overwritten by Copier
_commit: efb938e
_src_path: https://github.com/fastapi-mvc/copier-project.git
aiohttp: true
author: Radosław Szamszur
chart_name: test-project
container_image_name: test-project
copyright_date: '2022'
email: github@rsd.sh
fastapi_mvc_version: 0.17.0
github_actions: true
helm: true
license: MIT
nix: true
package_name: test_project
project_description: This project was generated with fastapi-mvc.
project_name: test-project
redis: true
repo_url: https://your.repo.url.here
script_name: test-project
version: 0.1.0

"""


@pytest.fixture
def cli_runner():
    yield CliRunner(
        env={
            "POETRY_HOME": "/tmp/poetry",
            "POETRY_CONFIG_DIR": "/tmp/poetry",
            "POETRY_VIRTUALENVS_PATH": "/opt/poetry/store",
        },
    )


@pytest.fixture(scope="session")
def fake_project(tmp_path_factory):
    root_dir = tmp_path_factory.mktemp("test-project")
    app_dir = root_dir / "test_project" / "app"
    app_dir.mkdir(parents=True)
    answers = root_dir / ".fastapi-mvc.yml"
    answers.write_text(content)

    return root_dir
