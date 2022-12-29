import os
import stat
import shutil

import pytest
from click.testing import CliRunner


test_generators_path = os.path.abspath(
    os.path.join(
        os.path.abspath(__file__),
        "../custom_generators",
    )
)
answers_file_content = """\
# Changes here will be overwritten by Copier
_commit: efb938e
_src_path: https://github.com/fastapi-mvc/copier-project.git
aiohttp: true
author: Radosław Szamszur
chart_name: fake-project
container_image_name: fake-project
copyright_date: '2022'
email: github@rsd.sh
fastapi_mvc_version: 0.17.0
github_actions: true
helm: true
license: MIT
nix: true
package_name: fake_project
project_description: This project was generated with fastapi-mvc.
project_name: fake-project
redis: true
repo_url: https://your.repo.url.here
script_name: fake-project
version: 0.1.0

"""


@pytest.fixture
def cli_runner():
    yield CliRunner()


@pytest.fixture(scope="session")
def fake_project(tmp_path_factory):
    root_dir = tmp_path_factory.mktemp("fake-project")
    app_dir = root_dir / "fake_project" / "app"
    app_dir.mkdir(parents=True)
    answers = root_dir / ".fastapi-mvc.yml"
    answers.write_text(answers_file_content)

    return {
        "root": root_dir,
        "module_dir": app_dir.parent,
        "app_dir": app_dir,
        "answers_file": answers,
    }


@pytest.fixture(scope="session")
def fake_project_with_generators(tmp_path_factory):
    root_dir = tmp_path_factory.mktemp("fake-project")
    app_dir = root_dir / "fake_project" / "app"
    app_dir.mkdir(parents=True)
    answers = root_dir / ".fastapi-mvc.yml"
    answers.write_text(answers_file_content)
    generators_dir = root_dir / "lib" / "generators"
    generators_dir.mkdir(parents=True)
    shutil.copytree(test_generators_path, generators_dir, dirs_exist_ok=True)

    return {
        "root": root_dir,
        "module_dir": app_dir.parent,
        "app_dir": app_dir,
        "answers_file": answers,
        "generators_dir": generators_dir,
    }


@pytest.fixture
def dummy_executable(tmp_path):
    dummy_exec = tmp_path / "dummy-executable"
    dummy_exec.write_text("""#!/usr/env/bin bash\necho "Hello world!"\n""")
    dummy_exec.chmod(dummy_exec.stat().st_mode | stat.S_IEXEC)
    yield dummy_exec
    dummy_exec.unlink()
