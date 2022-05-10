import os
import inspect
from datetime import datetime

import pytest
import mock
import click
from cookiecutter.exceptions import OutputDirExistsException
from fastapi_mvc.generators import ProjectGenerator
from fastapi_mvc.version import __version__


CONTROLLER_DIR = os.path.abspath(os.path.join(inspect.getfile(ProjectGenerator), "../"))


@pytest.fixture
def gen_obj():
    yield ProjectGenerator()


def test_class_variables():
    assert ProjectGenerator.name == "new"
    assert ProjectGenerator.template == os.path.join(CONTROLLER_DIR, "template")
    assert not ProjectGenerator.usage
    assert ProjectGenerator.category == "Project"

    assert len(ProjectGenerator.cli_arguments) == 1
    assert isinstance(ProjectGenerator.cli_arguments[0], click.Argument)
    assert ProjectGenerator.cli_arguments[0].opts == ["APP_PATH"]
    assert ProjectGenerator.cli_arguments[0].required
    assert isinstance(ProjectGenerator.cli_arguments[0].type, click.Path)
    assert not ProjectGenerator.cli_arguments[0].type.exists
    assert ProjectGenerator.cli_arguments[0].nargs == 1

    assert len(ProjectGenerator.cli_options) == 7
    assert isinstance(ProjectGenerator.cli_options[0], click.Option)
    assert ProjectGenerator.cli_options[0].opts == ["-R", "--skip-redis"]
    assert ProjectGenerator.cli_options[0].help == "Skip Redis utility files."
    assert ProjectGenerator.cli_options[0].is_flag
    assert isinstance(ProjectGenerator.cli_options[1], click.Option)
    assert ProjectGenerator.cli_options[1].opts == ["-A", "--skip-aiohttp"]
    assert ProjectGenerator.cli_options[1].help == "Skip aiohttp utility files."
    assert ProjectGenerator.cli_options[1].is_flag
    assert isinstance(ProjectGenerator.cli_options[2], click.Option)
    assert ProjectGenerator.cli_options[2].opts == ["-H", "--skip-helm"]
    assert ProjectGenerator.cli_options[2].help == "Skip Helm chart files."
    assert ProjectGenerator.cli_options[2].is_flag
    assert isinstance(ProjectGenerator.cli_options[3], click.Option)
    assert ProjectGenerator.cli_options[3].opts == ["-G", "--skip-actions"]
    assert ProjectGenerator.cli_options[3].help == "Skip GitHub actions files."
    assert ProjectGenerator.cli_options[3].is_flag
    assert isinstance(ProjectGenerator.cli_options[4], click.Option)
    assert ProjectGenerator.cli_options[4].opts == ["-I", "--skip-install"]
    assert ProjectGenerator.cli_options[4].help == "Do not run make install."
    assert ProjectGenerator.cli_options[4].is_flag
    assert isinstance(ProjectGenerator.cli_options[5], click.Option)
    assert ProjectGenerator.cli_options[5].opts == ["--license"]
    assert ProjectGenerator.cli_options[5].help == "Choose license."
    assert ProjectGenerator.cli_options[5].default == "MIT"
    assert ProjectGenerator.cli_options[5].show_default
    assert ProjectGenerator.cli_options[5].envvar == "LICENSE"
    assert isinstance(ProjectGenerator.cli_options[5].type, click.Choice)
    assert ProjectGenerator.cli_options[5].type.choices == [
        "MIT",
        "BSD2",
        "BSD3",
        "ISC",
        "Apache2.0",
        "LGPLv3+",
        "LGPLv3",
        "LGPLv2+",
        "LGPLv2",
        "no",
    ]
    assert isinstance(ProjectGenerator.cli_options[6], click.Option)
    assert ProjectGenerator.cli_options[6].opts == ["--repo-url"]
    assert ProjectGenerator.cli_options[6].help == "Repository url."
    assert ProjectGenerator.cli_options[6].type == click.STRING
    assert ProjectGenerator.cli_options[6].default == "https://your.repo.url.here"
    assert ProjectGenerator.cli_options[6].envvar == "REPO_URL"

    assert ProjectGenerator.cli_short_help == "Create a new FastAPI application."
    assert (
        ProjectGenerator.cli_help
        == """\
    The 'fastapi-mvc new' command creates a new FastAPI application with a
    default directory structure and configuration at the path you specify.
    """
    )


@pytest.mark.parametrize(
    "kwargs, expected_ctx, out_dir",
    [
        (
            {
                "app_path": "/test/path/test-project",
                "skip_redis": False,
                "skip_aiohttp": False,
                "skip_helm": False,
                "skip_actions": False,
                "skip_install": False,
                "license": "MIT",
                "repo_url": "https://your.repo.url.here",
            },
            {
                "project_name": "test-project",
                "redis": "yes",
                "aiohttp": "yes",
                "github_actions": "yes",
                "helm": "yes",
                "author": "John Doe",
                "email": "example@email.com",
                "license": "MIT",
                "repo_url": "https://your.repo.url.here",
                "year": datetime.today().year,
                "fastapi_mvc_version": __version__,
            },
            "/test/path",
        ),
        (
            {
                "app_path": "test-project",
                "skip_redis": True,
                "skip_aiohttp": True,
                "skip_helm": True,
                "skip_actions": True,
                "skip_install": True,
                "license": "Apache2.0",
                "repo_url": "https://scm.test/repo",
            },
            {
                "project_name": "test-project",
                "redis": "no",
                "aiohttp": "no",
                "github_actions": "no",
                "helm": "no",
                "author": "John Doe",
                "email": "example@email.com",
                "license": "Apache2.0",
                "repo_url": "https://scm.test/repo",
                "year": datetime.today().year,
                "fastapi_mvc_version": __version__,
            },
            ".",
        ),
    ],
)
@mock.patch("fastapi_mvc.generators.project.project.ShellUtils")
@mock.patch("fastapi_mvc.generators.project.project.cookiecutter")
def test_new(cookie_mock, utils_mock, kwargs, expected_ctx, out_dir, gen_obj):
    utils_mock.get_git_user_info.return_value = (
        "John Doe",
        "example@email.com",
    )

    gen_obj.new(**kwargs)

    utils_mock.get_git_user_info.assert_called_once()
    cookie_mock.assert_called_once_with(
        gen_obj.template,
        extra_context=expected_ctx,
        no_input=True,
        output_dir=out_dir,
    )

    if not kwargs["skip_install"]:
        utils_mock.run_shell.assert_called_once_with(
            cmd=["make", "install"], cwd=kwargs["app_path"]
        )
    else:
        utils_mock.run_shell.assert_not_called()


@mock.patch("fastapi_mvc.generators.project.project.ShellUtils")
@mock.patch(
    "fastapi_mvc.generators.project.project.cookiecutter",
    side_effect=OutputDirExistsException(),
)
def test_new_dir_exists(cookie_mock, utils_mock, gen_obj):
    utils_mock.get_git_user_info.return_value = (
        "John Doe",
        "example@email.com",
    )
    with pytest.raises(SystemExit):
        gen_obj.new(
            app_path="/test/path/test-project",
            skip_redis=False,
            skip_aiohttp=False,
            skip_helm=False,
            skip_actions=False,
            skip_install=False,
            license="MIT",
            repo_url="https://your.repo.url.here",
        )

    utils_mock.get_git_user_info.assert_called_once()
    cookie_mock.assert_called_once_with(
        gen_obj.template,
        extra_context={
            "project_name": "test-project",
            "redis": "yes",
            "aiohttp": "yes",
            "github_actions": "yes",
            "helm": "yes",
            "author": "John Doe",
            "email": "example@email.com",
            "license": "MIT",
            "repo_url": "https://your.repo.url.here",
            "year": datetime.today().year,
            "fastapi_mvc_version": __version__,
        },
        no_input=True,
        output_dir="/test/path",
    )

    utils_mock.run_shell.assert_not_called()


def test_destroy(gen_obj):
    with pytest.raises(NotImplementedError):
        gen_obj.destroy()
