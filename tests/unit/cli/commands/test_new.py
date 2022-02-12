from datetime import datetime

import mock
import pytest
from fastapi_mvc.cli.commands.new import new
from fastapi_mvc.version import __version__
from cookiecutter.exceptions import OutputDirExistsException


def test_new_help(cli_runner):
    result = cli_runner.invoke(new, ["--help"])
    assert result.exit_code == 0


def test_new_invalid_option(cli_runner):
    result = cli_runner.invoke(new, ["--not_exists"])
    assert result.exit_code == 2


@mock.patch("fastapi_mvc.cli.commands.new.ShellUtils")
@mock.patch("fastapi_mvc.cli.commands.new.ProjectGenerator")
def test_new_default_values(gen_mock, utils_mock, cli_runner):
    utils_mock.get_git_user_info.return_value = ("Joe", "email@test.com")

    result = cli_runner.invoke(new, ["testapp"])
    assert result.exit_code == 0

    utils_mock.get_git_user_info.assert_called_once()
    utils_mock.run_shell.assert_called_once_with(
        cmd=["make", "install"], cwd="testapp"
    )
    gen_mock.return_value.new.assert_called_once_with(
        context={
            "project_name": "testapp",
            "redis": "yes",
            "aiohttp": "yes",
            "github_actions": "yes",
            "vagrantfile": "yes",
            "helm": "yes",
            "codecov": "yes",
            "author": "Joe",
            "email": "email@test.com",
            "license": "MIT",
            "repo_url": "https://your.repo.url.here",
            "year": datetime.today().year,
            "fastapi_mvc_version": __version__,
        },
        output_dir=".",
    )


@pytest.mark.parametrize(
    "args",
    (
        [
            "-R",
            "-A",
            "-V",
            "-H",
            "-G",
            "-C",
            "-I",
            "--license",
            "LGPLv3+",
            "--repo-url",
            "https://github.com/gandalf/gondorapi",
            "/tmp/testapp"
        ],
        [
            "--skip-redis",
            "--skip-aiohttp",
            "--skip-vagrantfile",
            "--skip-helm",
            "--skip-actions",
            "--skip-codecov",
            "--skip-install",
            "--license",
            "LGPLv3+",
            "--repo-url",
            "https://github.com/gandalf/gondorapi",
            "/tmp/testapp",
        ],
    ),
)
@mock.patch("fastapi_mvc.cli.commands.new.ShellUtils")
@mock.patch("fastapi_mvc.cli.commands.new.ProjectGenerator")
def test_new_with_options(gen_mock, utils_mock, cli_runner, args):
    utils_mock.get_git_user_info.return_value = ("Joe", "email@test.com")

    result = cli_runner.invoke(new, args)
    assert result.exit_code == 0

    utils_mock.run_project_install.assert_not_called()
    gen_mock.return_value.new.assert_called_once_with(
        context={
            "project_name": "testapp",
            "redis": "no",
            "aiohttp": "no",
            "github_actions": "no",
            "vagrantfile": "no",
            "helm": "no",
            "codecov": "no",
            "author": "Joe",
            "license": "LGPLv3+",
            "email": "email@test.com",
            "repo_url": "https://github.com/gandalf/gondorapi",
            "year": datetime.today().year,
            "fastapi_mvc_version": __version__,
        },
        output_dir="/tmp",
    )


@mock.patch("fastapi_mvc.cli.commands.new.ShellUtils")
@mock.patch("fastapi_mvc.cli.commands.new.ProjectGenerator")
def test_new_cookiecutter_exception(gen_mock, utils_mock, cli_runner):
    utils_mock.get_git_user_info.return_value = ("Joe", "email@test.com")
    gen_mock.return_value.new.side_effect = OutputDirExistsException()

    result = cli_runner.invoke(new, ["/tmp/testapp"])
    assert result.exit_code == 1

    utils_mock.get_git_user_info.assert_called_once()
    utils_mock.run_project_install.assert_not_called()
    gen_mock.return_value.new.assert_called_once_with(
        context={
            "project_name": "testapp",
            "redis": "yes",
            "aiohttp": "yes",
            "github_actions": "yes",
            "vagrantfile": "yes",
            "helm": "yes",
            "codecov": "yes",
            "author": "Joe",
            "email": "email@test.com",
            "license": "MIT",
            "repo_url": "https://your.repo.url.here",
            "year": datetime.today().year,
            "fastapi_mvc_version": __version__,
        },
        output_dir="/tmp",
    )
