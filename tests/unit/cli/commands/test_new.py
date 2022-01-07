import os
from datetime import datetime

import mock
from fastapi_mvc.cli.commands.new import new
from cookiecutter.exceptions import OutputDirExistsException


template_dir = os.path.abspath(
    os.path.join(
        os.path.abspath(__file__),
        "../../../../../fastapi_mvc/template",
    )
)


def test_new_help(cli_runner):
    result = cli_runner.invoke(new, ["--help"])
    assert result.exit_code == 0


def test_serve_invalid_option(cli_runner):
    result = cli_runner.invoke(new, ["--not_exists"])
    assert result.exit_code == 2


@mock.patch("fastapi_mvc.cli.commands.new.cookiecutter")
@mock.patch(
    "fastapi_mvc.cli.commands.new.subprocess.check_output",
    side_effect=["Joe".encode("utf-8"), "email@test.com".encode("utf-8")]
)
@mock.patch("fastapi_mvc.cli.commands.new.subprocess.run")
def test_new_default_options(run_mock, check_mock, cookie_mock, cli_runner):
    result = cli_runner.invoke(new, ["/tmp/testapp"])
    assert result.exit_code == 0
    cookie_mock.assert_called_once_with(
        template_dir,
        extra_context={
            'project_name': 'testapp',
            'redis': 'yes',
            'aiohttp': 'yes',
            'github_actions': 'yes',
            'vagrantfile': 'yes',
            'helm': 'yes',
            'codecov': 'yes',
            'author': "Joe",
            'email': "email@test.com",
            'repo_url': 'https://your.repo.url.here',
            'year': datetime.today().year
        },
        no_input=True,
        output_dir="/tmp",
    )
    calls = [
        mock.call(["git", "config", "--get", "user.name"]),
        mock.call(["git", "config", "--get", "user.email"])
    ]
    check_mock.assert_has_calls(calls)
    run_mock.assert_called_once_with(["make", "install"], cwd="/tmp/testapp")


@mock.patch("fastapi_mvc.cli.commands.new.cookiecutter")
@mock.patch(
    "fastapi_mvc.cli.commands.new.subprocess.check_output",
    side_effect=["Joe".encode("utf-8"), "email@test.com".encode("utf-8")]
)
def test_new_skip_options(check_mock, cookie_mock, cli_runner):
    result = cli_runner.invoke(
        new,
        ["-R", "-A", "-V", "-H", "-G", "-C", "-I", "testapp"]
    )
    assert result.exit_code == 0
    cookie_mock.assert_called_once_with(
        template_dir,
        extra_context={
            'project_name': 'testapp',
            'redis': 'no',
            'aiohttp': 'no',
            'github_actions': 'no',
            'vagrantfile': 'no',
            'helm': 'no',
            'codecov': 'no',
            'author': "Joe",
            'email': "email@test.com",
            'repo_url': 'https://your.repo.url.here',
            'year': datetime.today().year
        },
        no_input=True,
        output_dir=".",
    )
    calls = [
        mock.call(["git", "config", "--get", "user.name"]),
        mock.call(["git", "config", "--get", "user.email"])
    ]
    check_mock.assert_has_calls(calls)


@mock.patch(
    "fastapi_mvc.cli.commands.new.cookiecutter",
    side_effect=OutputDirExistsException(),
)
@mock.patch(
    "fastapi_mvc.cli.commands.new.subprocess.check_output",
    side_effect=["Joe".encode("utf-8"), "email@test.com".encode("utf-8")]
)
def test_new_dir_exists(check_mock, cookie_mock, cli_runner):
    result = cli_runner.invoke(new, ["testapp"])
    assert result.exit_code == 1
    cookie_mock.assert_called_once_with(
        template_dir,
        extra_context={
            'project_name': 'testapp',
            'redis': 'yes',
            'aiohttp': 'yes',
            'github_actions': 'yes',
            'vagrantfile': 'yes',
            'helm': 'yes',
            'codecov': 'yes',
            'author': "Joe",
            'email': "email@test.com",
            'repo_url': 'https://your.repo.url.here',
            'year': datetime.today().year
        },
        no_input=True,
        output_dir=".",
    )
    calls = [
        mock.call(["git", "config", "--get", "user.name"]),
        mock.call(["git", "config", "--get", "user.email"])
    ]
    check_mock.assert_has_calls(calls)
