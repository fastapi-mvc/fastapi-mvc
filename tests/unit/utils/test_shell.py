import os
import subprocess
from subprocess import CalledProcessError
from unittest import mock

import pytest
from fastapi_mvc.utils import get_git_user_info, run_shell, get_poetry_path


class TestGetPoetryPath:

    @pytest.mark.parametrize("variable, value, expected", [
        ("HOME", "/home/foobar", "/home/foobar/.local/share/pypoetry/venv/bin/poetry"),
        ("POETRY_BINARY", "/path/to/poetry", "/path/to/poetry"),
        ("POETRY_HOME", "/opt/poetry", "/opt/poetry/venv/bin/poetry")
    ])
    def test_should_return_poetry_path_from_env(self, variable, value, expected):
        with mock.patch.dict(os.environ, {variable: value}, clear=True):
            # given / when
            poetry_path = get_poetry_path()

            # then
            assert poetry_path == expected


class TestGetGitUserInfo:

    @mock.patch(
        "fastapi_mvc.utils.shell.subprocess.check_output",
        side_effect=[
            "Darth Vader".encode("utf-8"),
            "join@galactic.empire".encode("utf-8"),
        ],
    )
    def test_should_return_git_username_and_email(self, check_mock):
        # given / when
        author, email = get_git_user_info()

        # then
        assert author == "Darth Vader"
        assert email == "join@galactic.empire"
        check_mock.assert_has_calls(
            [
                mock.call(["git", "config", "--get", "user.name"]),
                mock.call(["git", "config", "--get", "user.email"]),
            ]
        )

    @mock.patch(
        "fastapi_mvc.utils.shell.subprocess.check_output",
        side_effect=CalledProcessError(1, []),
    )
    def test_should_return_defaults_when_subprocess_error(self, check_mock):
        # given / when
        author, email = get_git_user_info()

        # then
        assert author == "John Doe"
        assert email == "example@email.com"
        check_mock.assert_has_calls(
            [
                mock.call(["git", "config", "--get", "user.name"]),
                mock.call(["git", "config", "--get", "user.email"]),
            ]
        )

    @mock.patch(
        "fastapi_mvc.utils.shell.shutil.which",
        return_value=False,
    )
    @mock.patch("fastapi_mvc.utils.shell.subprocess.check_output")
    def test_should_return_defaults_when_no_git_present(self, check_mock, which_mock):
        # given / when
        author, email = get_git_user_info()

        # then
        assert author == "John Doe"
        assert email == "example@email.com"
        which_mock.assert_called_once_with("git")
        check_mock.assert_not_called()


class TestRunShell:

    def test_should_call_and_populate_defaults(self):
        # given
        cmd = ["/usr/bin/env", "true"]

        # when
        process = run_shell(cmd)

        # then
        assert process.returncode == 0
        assert process.args == cmd
        assert not process.stderr
        assert not process.stdout

    def test_should_call_with_args(self, fake_project):
        # given /when
        process = run_shell(
            cmd=["/usr/bin/env", "true"],
            cwd=fake_project["root"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        # then
        assert process.returncode == 0

    def test_should_raise_when_subprocess_failed_and_check_is_true(self):
        # given
        check = True

        # when / then
        with pytest.raises(subprocess.CalledProcessError):
            run_shell(
                cmd=["/usr/bin/env", "false"],
                check=check,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

    def test_should_not_raise_when_subprocess_failed_and_check_is_false(self):
        # given
        check = False

        # when
        process = run_shell(
            cmd=["/usr/bin/env", "false"],
            check=check,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        # then
        assert process.returncode != 0

    @pytest.mark.parametrize("env, expected", [
        (
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
            {
                "VIRTUAL_ENV": "/home/foobar/repos/fastapi-mvc/.venv",
                "PATH": "/home/foobar/.local/bin:/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/home/foobar/repos/fastapi-mvc/.venv/bin",
            },
            {
                "PATH": "/home/foobar/.local/bin:/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin"
            },
        )
    ])
    @mock.patch("fastapi_mvc.utils.shell.subprocess.run")
    def test_should_remove_venv_from_path_if_activated(self, run_mock, env, expected):
        # given / when
        with mock.patch.dict(os.environ, env, clear=True):
            run_shell(["make", "install"], "/path/to/execute")

        # then
        run_mock.assert_called_once_with(
            ["make", "install"],
            cwd="/path/to/execute",
            env=expected,
            check=False,
            stdout=None,
            stderr=None,
            input=None,
            capture_output=False,
        )
