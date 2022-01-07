import os
import subprocess

import mock
from fastapi_mvc.cli.commands.new import new


template_dir = os.path.abspath(
    os.path.join(
        os.path.abspath(__file__),
        "../../../../../fastapi_mvc/template",
    )
)

try:
    user = (
        subprocess.check_output(["git", "config", "--get", "user.name"])
            .decode("utf-8")
            .strip()
    )
    email = (
        subprocess.check_output(["git", "config", "--get", "user.email"])
            .decode("utf-8")
            .strip()
    )
except subprocess.CalledProcessError:
    user = None
    email = None


def test_new_help(cli_runner):
    result = cli_runner.invoke(new, ["--help"])
    assert result.exit_code == 0


def test_serve_invalid_option(cli_runner):
    result = cli_runner.invoke(new, ["--not_exists"])
    assert result.exit_code == 2


@mock.patch("fastapi_mvc.cli.commands.new.cookiecutter")
def test_new_default_options(run_mock, cli_runner):
    result = cli_runner.invoke(new, ["testapp"])
    assert result.exit_code == 0
    run_mock.assert_called_once_with(
        template_dir,
        extra_context={
            'project_name': 'testapp',
            'redis': 'yes',
            'aiohttp': 'yes',
            'github_actions': 'yes',
            'vagrantfile': 'yes',
            'helm': 'yes',
            'author': user,
            'email': email,
            'repo_url': None,
            'year': 2022
        },
        no_input=True,
    )


@mock.patch("fastapi_mvc.cli.commands.new.cookiecutter")
def test_new_skip_options(run_mock, cli_runner):
    result = cli_runner.invoke(new, ["-R", "-A", "-V", "-H", "-G", "testapp"])
    assert result.exit_code == 0
    run_mock.assert_called_once_with(
        template_dir,
        extra_context={
            'project_name': 'testapp',
            'redis': 'no',
            'aiohttp': 'no',
            'github_actions': 'no',
            'vagrantfile': 'no',
            'helm': 'no',
            'author': user,
            'email': email,
            'repo_url': None,
            'year': 2022
        },
        no_input=True,
    )
