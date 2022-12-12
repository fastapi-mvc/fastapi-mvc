import os
from datetime import datetime
from unittest import mock

import pytest
from fastapi_mvc import VERSION
from fastapi_mvc.cli.new import new


DIR = os.getcwd()


def test_new_help(cli_runner):
    result = cli_runner.invoke(new, ["--help"])
    assert result.exit_code == 0


def test_new_invalid_options(cli_runner):
    result = cli_runner.invoke(new, ["--not_exists"])
    assert result.exit_code == 2


@mock.patch("fastapi_mvc.cli.new.shutil.which", return_value=True)
@mock.patch("fastapi_mvc.cli.new.run_shell")
@mock.patch("fastapi_mvc.cli.new.get_git_user_info", return_value=("John", "ex@ma.il"))
@mock.patch("fastapi_mvc.cli.new.Generator.run_auto")
def test_new_default_values(copier_mock, git_mock, shell_mock, which_mock, cli_runner):
    result = cli_runner.invoke(new, ["test-project"])
    assert result.exit_code == 0

    git_mock.assert_called_once()
    shell_mock.assert_has_calls(
        [
            mock.call(cmd=["git", "init"], cwd=f"{DIR}/test-project"),
            mock.call(cmd=["make", "install"], cwd=f"{DIR}/test-project"),
        ]
    )
    copier_mock.assert_called_once_with(
        dst_path=f"{DIR}/test-project",
        user_defaults={
            "project_name": "test-project",
            "author": "John",
            "email": "ex@ma.il",
            "copyright_date": datetime.today().year,
            "fastapi_mvc_version": VERSION,
            "nix": True,
            "redis": True,
            "aiohttp": True,
            "github_actions": True,
            "helm": True,
            "license": "MIT",
            "repo_url": "https://your.repo.url.here",
            "container_image_name": "test-project",
            "chart_name": "test-project",
            "script_name": "test-project",
            "project_description": "This project was generated with fastapi-mvc.",
            "version": "0.1.0",
        },
    )
    which_mock.assert_called_once_with("make")


@pytest.mark.parametrize(
    "args, expected",
    [
        (
            [
                "-R",
                "-A",
                "-H",
                "-G",
                "-I",
                "-N",
                "--license",
                "LGPLv3+",
                "--repo-url",
                "https://github.com/gandalf/gondorapi",
                "test-project",
            ],
            {
                "dst_path": f"{DIR}/test-project",
                "user_defaults": {
                    "project_name": "test-project",
                    "author": "John",
                    "email": "ex@ma.il",
                    "copyright_date": datetime.today().year,
                    "fastapi_mvc_version": VERSION,
                    "nix": False,
                    "redis": False,
                    "aiohttp": False,
                    "github_actions": False,
                    "helm": False,
                    "license": "LGPLv3+",
                    "repo_url": "https://github.com/gandalf/gondorapi",
                    "container_image_name": "test-project",
                    "chart_name": "test-project",
                    "script_name": "test-project",
                    "project_description": "This project was generated with fastapi-mvc.",
                    "version": "0.1.0",
                },
            },
        ),
        (
            [
                "--no-interaction",
                "--repo-url",
                "https://thethingyouallbeenwaitingfor.trustme",
                "--use-repo",
                "https://howtomambo.git",
                "--use-version",
                "0.1.0",
                f"{DIR}/Mambo_No6",
            ],
            {
                "dst_path": f"{DIR}/Mambo_No6",
                "data": {
                    "project_name": "Mambo_No6",
                    "author": "John",
                    "email": "ex@ma.il",
                    "copyright_date": datetime.today().year,
                    "fastapi_mvc_version": VERSION,
                    "nix": True,
                    "redis": True,
                    "aiohttp": True,
                    "github_actions": True,
                    "helm": True,
                    "license": "MIT",
                    "repo_url": "https://thethingyouallbeenwaitingfor.trustme",
                    "container_image_name": "Mambo_No6",
                    "chart_name": "Mambo_No6",
                    "script_name": "Mambo_No6",
                    "project_description": "This project was generated with fastapi-mvc.",
                    "version": "0.1.0",
                },
            },
        ),
        (
            ["."],
            {
                "dst_path": f"{DIR}",
                "user_defaults": {
                    "project_name": os.path.basename(DIR),
                    "author": "John",
                    "email": "ex@ma.il",
                    "copyright_date": datetime.today().year,
                    "fastapi_mvc_version": VERSION,
                    "nix": True,
                    "redis": True,
                    "aiohttp": True,
                    "github_actions": True,
                    "helm": True,
                    "license": "MIT",
                    "repo_url": "https://your.repo.url.here",
                    "container_image_name": os.path.basename(DIR),
                    "chart_name": os.path.basename(DIR),
                    "script_name": os.path.basename(DIR),
                    "project_description": "This project was generated with fastapi-mvc.",
                    "version": "0.1.0",
                },
            }
        ),
    ],
)
@mock.patch("fastapi_mvc.cli.new.shutil.which", return_value=True)
@mock.patch("fastapi_mvc.cli.new.run_shell")
@mock.patch("fastapi_mvc.cli.new.get_git_user_info", return_value=("John", "ex@ma.il"))
@mock.patch("fastapi_mvc.cli.new.Generator.run_auto")
def test_new_with_options(
    copier_mock, git_mock, shell_mock, which_mock, cli_runner, args, expected
):
    result = cli_runner.invoke(new, args)
    assert result.exit_code == 0

    git_mock.assert_called_once()
    copier_mock.assert_called_once_with(**expected)
    calls = [
        mock.call(cmd=["git", "init"], cwd=expected["dst_path"]),
        mock.call(cmd=["make", "install"], cwd=expected["dst_path"]),
    ]

    if "--skip-install" in args or "-I" in args:
        calls.pop()
    else:
        which_mock.assert_called_once_with("make")

    shell_mock.assert_has_calls(calls)


@mock.patch("fastapi_mvc.cli.new.shutil.which", return_value=None)
@mock.patch("fastapi_mvc.cli.new.run_shell")
@mock.patch("fastapi_mvc.cli.new.get_git_user_info", return_value=("John", "ex@ma.il"))
@mock.patch("fastapi_mvc.cli.new.Generator.run_auto")
def test_new_no_make(copier_mock, git_mock, shell_mock, which_mock, cli_runner):
    result = cli_runner.invoke(new, ["test-project"])
    assert result.exit_code == 0

    git_mock.assert_called_once()
    shell_mock.assert_called_once_with(
        cmd=["git", "init"], cwd=f"{DIR}/test-project"
    )
    copier_mock.assert_called_once_with(
        dst_path=f"{DIR}/test-project",
        user_defaults={
            "project_name": "test-project",
            "author": "John",
            "email": "ex@ma.il",
            "copyright_date": datetime.today().year,
            "fastapi_mvc_version": VERSION,
            "nix": True,
            "redis": True,
            "aiohttp": True,
            "github_actions": True,
            "helm": True,
            "license": "MIT",
            "repo_url": "https://your.repo.url.here",
            "container_image_name": "test-project",
            "chart_name": "test-project",
            "script_name": "test-project",
            "project_description": "This project was generated with fastapi-mvc.",
            "version": "0.1.0",
        },
    )
    which_mock.assert_called_once_with("make")
