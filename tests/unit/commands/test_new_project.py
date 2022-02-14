from datetime import datetime

import mock
import pytest
from fastapi_mvc.commands import GenerateNewProject
from fastapi_mvc.version import __version__


@pytest.mark.parametrize(
    "app_path, options, expected",
    [
        (
            "/test/path/my-app",
            {
                "skip_redis": False,
                "skip_aiohttp": False,
                "skip_vagrantfile": False,
                "skip_helm": False,
                "skip_actions": False,
                "skip_codecov": False,
                "skip_install": False,
                "license": "MIT",
                "repo_url": "https://your.repo.url.here"
            },
            {
                "context": {
                    "project_name": "my-app",
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
                "output_dir": "/test/path"
            }
        ),
        (
            "foobar",
            {
                "skip_redis": True,
                "skip_aiohttp": True,
                "skip_vagrantfile": True,
                "skip_helm": True,
                "skip_actions": True,
                "skip_codecov": True,
                "skip_install": False,
                "license": "ISC",
                "repo_url": "https://scm.test/repo"
            },
            {
                "context": {
                    "project_name": "foobar",
                    "redis": "no",
                    "aiohttp": "no",
                    "github_actions": "no",
                    "vagrantfile": "no",
                    "helm": "no",
                    "codecov": "no",
                    "author": "Joe",
                    "email": "email@test.com",
                    "license": "ISC",
                    "repo_url": "https://scm.test/repo",
                    "year": datetime.today().year,
                    "fastapi_mvc_version": __version__,
                },
                "output_dir": "."
            }
        ),
        (
                "my-awesome-project",
                {
                    "skip_redis": True,
                    "skip_aiohttp": True,
                    "skip_vagrantfile": True,
                    "skip_helm": True,
                    "skip_actions": True,
                    "skip_codecov": True,
                    "skip_install": True,
                    "license": "Apache2.0",
                    "repo_url": "https://scm.test/repo"
                },
                {
                    "context": {
                        "project_name": "my-awesome-project",
                        "redis": "no",
                        "aiohttp": "no",
                        "github_actions": "no",
                        "vagrantfile": "no",
                        "helm": "no",
                        "codecov": "no",
                        "author": "Joe",
                        "email": "email@test.com",
                        "license": "Apache2.0",
                        "repo_url": "https://scm.test/repo",
                        "year": datetime.today().year,
                        "fastapi_mvc_version": __version__,
                    },
                    "output_dir": "."
                }
        ),
    ]
)
@mock.patch("fastapi_mvc.commands.new_project.ShellUtils")
@mock.patch("fastapi_mvc.commands.new_project.ProjectGenerator")
def test_execute(gen_mock, utils_mock, app_path, options, expected):
    utils_mock.get_git_user_info.return_value = ("Joe", "email@test.com")

    command = GenerateNewProject(app_path=app_path, options=options)
    command.execute()

    utils_mock.get_git_user_info.assert_called_once()
    gen_mock.return_value.new.assert_called_once_with(**expected)

    # if not options["skip_install"]:
    #     utils_mock.run_shell.assert_called_once_with(
    #         cmd=["make", "install"], cwd=app_path
    #     )
    # else:
    #     utils_mock.run_shell.assert_not_called()
