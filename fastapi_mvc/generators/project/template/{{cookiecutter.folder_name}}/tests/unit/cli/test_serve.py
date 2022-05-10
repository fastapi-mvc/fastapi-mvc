import os

import mock
import pytest
from {{cookiecutter.package_name}}.cli.serve import serve


current_dir = os.path.dirname(__file__)
pid_file = os.path.join(current_dir, "test.pid")


def test_serve_help(cli_runner):
    result = cli_runner.invoke(serve, ["--help"])
    assert result.exit_code == 0


@pytest.mark.parametrize(
    "opts, expected",
    [
        (
            [],
            {},
        ),
        (
            ["--bind", "localhost:5000", "-w", 2],
            {
                "bind": "localhost:5000",
                "workers": 2,
            },
        ),
        (
            [
                "--bind",
                "localhost:5000",
                "-w",
                2,
                "--daemon",
                "--env",
                "FOO=BAR",
                "--env",
                "USE_FORCE=True",
                "--pid",
                pid_file,
            ],
            {
                "bind": "localhost:5000",
                "workers": 2,
                "daemon": True,
                "raw_env": ("FOO=BAR", "USE_FORCE=True"),
                "pidfile": pid_file,
            },
        ),
        (
            [
                "--bind",
                "localhost:5000",
                "-w",
                2,
                "-D",
                "-e",
                "FOO=BAR",
                "-e",
                "USE_FORCE=True",
                "--pid",
                pid_file,
            ],
            {
                "bind": "localhost:5000",
                "workers": 2,
                "daemon": True,
                "raw_env": ("FOO=BAR", "USE_FORCE=True"),
                "pidfile": pid_file,
            },
        ),
    ],
)
@mock.patch("{{cookiecutter.package_name}}.cli.serve.get_application")
@mock.patch("{{cookiecutter.package_name}}.cli.serve.ApplicationLoader")
def test_serve_options(wsgi_mock, asgi_mock, cli_runner, opts, expected):
    result = cli_runner.invoke(serve, opts)
    assert result.exit_code == 0

    wsgi_mock.assert_called_once_with(
        application=asgi_mock.return_value,
        overrides=expected,
    )


@pytest.mark.parametrize(
    "opts",
    [
        (["--not_exists"]),
        (["--pid", "/path/does/not/exist"]),
    ],
)
def test_serve_invalid_option(cli_runner, opts):
    result = cli_runner.invoke(serve, opts)
    assert result.exit_code == 2
