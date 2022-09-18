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
    assert ProjectGenerator.template == "https://github.com/fastapi-mvc/cookiecutter.git"
    assert not ProjectGenerator.usage
    assert ProjectGenerator.category == "Project"

    assert len(ProjectGenerator.cli_arguments) == 1
    assert isinstance(ProjectGenerator.cli_arguments[0], click.Argument)
    assert ProjectGenerator.cli_arguments[0].opts == ["APP_PATH"]
    assert ProjectGenerator.cli_arguments[0].required
    assert isinstance(ProjectGenerator.cli_arguments[0].type, click.Path)
    assert not ProjectGenerator.cli_arguments[0].type.exists
    assert ProjectGenerator.cli_arguments[0].nargs == 1

    assert len(ProjectGenerator.cli_options) == 10
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
    assert ProjectGenerator.cli_options[5].opts == ["-N", "--skip-nix"]
    assert ProjectGenerator.cli_options[5].help == "Skip nix expression files."
    assert ProjectGenerator.cli_options[5].is_flag
    assert isinstance(ProjectGenerator.cli_options[6], click.Option)
    assert ProjectGenerator.cli_options[6].opts == ["--license"]
    assert ProjectGenerator.cli_options[6].help == "Choose license."
    assert ProjectGenerator.cli_options[6].default == "MIT"
    assert ProjectGenerator.cli_options[6].show_default
    assert ProjectGenerator.cli_options[6].envvar == "LICENSE"
    assert isinstance(ProjectGenerator.cli_options[6].type, click.Choice)
    assert ProjectGenerator.cli_options[6].type.choices == [
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
    assert isinstance(ProjectGenerator.cli_options[7], click.Option)
    assert ProjectGenerator.cli_options[7].opts == ["--repo-url"]
    assert ProjectGenerator.cli_options[7].help == "New project repository url."
    assert ProjectGenerator.cli_options[7].type == click.STRING
    assert ProjectGenerator.cli_options[7].default == "https://your.repo.url.here"
    assert ProjectGenerator.cli_options[7].envvar == "REPO_URL"
    assert isinstance(ProjectGenerator.cli_options[8], click.Option)
    assert ProjectGenerator.cli_options[8].opts == ["--template-version"]
    assert ProjectGenerator.cli_options[8].help == "The branch, tag or commit ID to checkout after clone."
    assert ProjectGenerator.cli_options[8].type == click.STRING
    assert ProjectGenerator.cli_options[8].default == "master"
    assert ProjectGenerator.cli_options[8].show_default
    assert isinstance(ProjectGenerator.cli_options[9], click.Option)
    assert ProjectGenerator.cli_options[9].opts == ["--override-template"]
    assert ProjectGenerator.cli_options[9].help == "Overrides fastapi-mvc cookiecutter template repository."
    assert ProjectGenerator.cli_options[9].type == click.STRING

    assert ProjectGenerator.cli_short_help == "Create a new FastAPI application."
    assert (
        ProjectGenerator.cli_help
        == """\
    The 'fastapi-mvc new' command creates a new FastAPI application with a
    default directory structure and configuration at the path you specify.

    Default Project template used: https://github.com/fastapi-mvc/cookiecutter

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
                "skip_nix": False,
                "skip_actions": False,
                "skip_install": False,
                "license": "MIT",
                "repo_url": "https://your.repo.url.here",
                "template_version": "master",
                "override_template": None,
            },
            {
                "project_name": "test-project",
                "redis": "yes",
                "aiohttp": "yes",
                "github_actions": "yes",
                "helm": "yes",
                "nix": "yes",
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
                "skip_nix": True,
                "skip_actions": True,
                "skip_install": True,
                "license": "Apache2.0",
                "repo_url": "https://scm.test/repo",
                "template_version": "0.1.0",
                "override_template": "https://my.template.git"
            },
            {
                "project_name": "test-project",
                "redis": "no",
                "aiohttp": "no",
                "github_actions": "no",
                "helm": "no",
                "nix": "no",
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
        gen_obj.template if not kwargs["override_template"] else kwargs["override_template"],
        checkout=kwargs["template_version"],
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
            skip_nix=False,
            skip_actions=False,
            skip_install=False,
            license="MIT",
            repo_url="https://your.repo.url.here",
            template_version="master",
            override_template=None,
        )

    utils_mock.get_git_user_info.assert_called_once()
    cookie_mock.assert_called_once_with(
        gen_obj.template,
        checkout="master",
        extra_context={
            "project_name": "test-project",
            "redis": "yes",
            "aiohttp": "yes",
            "github_actions": "yes",
            "helm": "yes",
            "nix": "yes",
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
