import os
from subprocess import CalledProcessError

import pytest
import mock
from fastapi_mvc.utils import ShellUtils


@mock.patch(
    "fastapi_mvc.utils.shell.subprocess.check_output",
    side_effect=[
        "Darth Vader".encode("utf-8"),
        "join@galactic.empire".encode("utf-8"),
    ],
)
def test_get_git_user_info(check_mock):
    author, email = ShellUtils.get_git_user_info()
    assert author == "Darth Vader"
    assert email == "join@galactic.empire"

    calls = [
        mock.call(["git", "config", "--get", "user.name"]),
        mock.call(["git", "config", "--get", "user.email"]),
    ]
    check_mock.assert_has_calls(calls)


@mock.patch(
    "fastapi_mvc.utils.shell.subprocess.check_output",
    side_effect=CalledProcessError(1, []),
)
def test_get_git_user_info_defaults(check_mock):
    author, email = ShellUtils.get_git_user_info()
    assert author == "John Doe"
    assert email == "example@email.com"

    calls = [
        mock.call(["git", "config", "--get", "user.name"]),
        mock.call(["git", "config", "--get", "user.email"]),
    ]
    check_mock.assert_has_calls(calls)


@pytest.mark.parametrize(
    "cmd, cwd, check, env, expected",
    [
        (
            ["make", "install"],
            "/path/to/execute",
            False,
            {
                "SHELL": "/bin/bash",
                "HOSTNAME": "foobar",
                "PWD": "/home/foobar/repos/fastapi-mvc",
                "LOGNAME": "foobar",
                "HOME": "/home/foobar",
                "USERNAME": "foobar",
                "LANG": "en_GB.UTF-8",
                "VIRTUAL_ENV": "/home/foobar/repos/fastapi-mvc/.venv",
                "USER": "foobar",
                "PATH": "/home/foobar/repos/fastapi-mvc/.venv/bin:/home/foobar/bin:/home/foobar/.local/bin:/home/foobar/.poetry/bin:/home/foobar/bin:/home/foobar/.local/bin:/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin",
            },
            {
                "SHELL": "/bin/bash",
                "HOSTNAME": "foobar",
                "PWD": "/home/foobar/repos/fastapi-mvc",
                "LOGNAME": "foobar",
                "HOME": "/home/foobar",
                "USERNAME": "foobar",
                "LANG": "en_GB.UTF-8",
                "USER": "foobar",
                "PATH": "/home/foobar/bin:/home/foobar/.local/bin:/home/foobar/.poetry/bin:/home/foobar/bin:/home/foobar/.local/bin:/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin",
            },
        ),
        (
            ["--opt", "/test/value", "--opt2", "False"],
            "/path/to/execute",
            True,
            {
                "SHELL": "/bin/bash",
                "HOSTNAME": "foobar",
                "PWD": "/home/foobar/repos/fastapi-mvc",
                "LOGNAME": "foobar",
                "HOME": "/home/foobar",
                "USERNAME": "foobar",
                "LANG": "en_GB.UTF-8",
            },
            {
                "SHELL": "/bin/bash",
                "HOSTNAME": "foobar",
                "PWD": "/home/foobar/repos/fastapi-mvc",
                "LOGNAME": "foobar",
                "HOME": "/home/foobar",
                "USERNAME": "foobar",
                "LANG": "en_GB.UTF-8",
            },
        ),
        (
            ["make", "install"],
            os.getcwd(),
            False,
            {
                "VIRTUAL_ENV": "/home/foobar/repos/fastapi-mvc/.venv",
                "PATH": "/home/foobar/.local/bin:/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/home/foobar/repos/fastapi-mvc/.venv/bin",
            },
            {
                "PATH": "/home/foobar/.local/bin:/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin"
            },
        ),
    ],
)
@mock.patch("fastapi_mvc.utils.shell.subprocess.run")
def test_run_shell(run_mock, cmd, cwd, check, env, expected):
    with mock.patch("fastapi_mvc.utils.shell.os.environ.copy") as os_mock:
        os_mock.return_value = env

        ShellUtils.run_shell(
            cmd=cmd,
            cwd=cwd,
            check=check
        )
        os_mock.assert_called_once()
        run_mock.assert_called_once_with(
            cmd, cwd=cwd, env=expected, check=check,
        )


@mock.patch("fastapi_mvc.utils.shell.subprocess.run")
def test_run_shell_defaults(run_mock):
    env = {"FOO": "BAR"}

    with mock.patch("fastapi_mvc.utils.shell.os.environ.copy") as os_mock:
        os_mock.return_value = env

        ShellUtils.run_shell(["test"])

        os_mock.assert_called_once()
        run_mock.assert_called_once_with(
            ["test"], cwd=os.getcwd(), env=env, check=False
        )
