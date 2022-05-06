import os

import mock
import pytest
from click import BadParameter
from {{cookiecutter.package_name}}.cli.commands.serve import (
    serve,
    validate_directory,
)


current_dir = os.path.dirname(__file__)
pid_file = os.path.join(current_dir, "test.pid")
conf_file = os.path.abspath(
    os.path.join(
        current_dir,
        "../../../../{{cookiecutter.package_name}}/config/gunicorn.conf.py"
    )
)


def test_validate_directory():
    result = validate_directory(mock.MagicMock(), mock.MagicMock(), current_dir)
    assert result == current_dir

    with pytest.raises(BadParameter):
        validate_directory(
            mock.MagicMock(), mock.MagicMock(), "/path/does/not/exist"
        )

    with mock.patch("{{cookiecutter.package_name}}.cli.commands.serve.os.access") as mck:
        mck.return_value = False

        with pytest.raises(BadParameter):
            validate_directory(
                mock.MagicMock(), mock.MagicMock(), os.path.abspath(__file__)
            )

        mck.assert_called_once_with(current_dir, os.W_OK)


def test_serve_help(cli_runner):
    result = cli_runner.invoke(serve, ["--help"])
    assert result.exit_code == 0


@mock.patch("{{cookiecutter.package_name}}.cli.commands.serve.run_wsgi")
@pytest.mark.parametrize(
    "opts, expected",
    [
        (
            ["--host", "localhost", "-p", 5000, "-w", 2],
            {
                "host": "localhost",
                "port": "5000",
                "workers": "2",
                "daemon": False,
                "env": (),
                "pid": None,
                "config": None,
            },
        ),
        (
            [
                "--host",
                "localhost",
                "-p",
                5000,
                "-w",
                2,
                "--daemon",
                "--env",
                "FOO=BAR",
                "--env",
                "USE_FORCE=True",
                "--pid",
                pid_file,
                "--config",
                conf_file,
            ],
            {
                "host": "localhost",
                "port": "5000",
                "workers": "2",
                "daemon": True,
                "env": ("FOO=BAR", "USE_FORCE=True"),
                "pid": pid_file,
                "config": conf_file,
            },
        ),
        (
            [
                "--host",
                "localhost",
                "-p",
                5000,
                "-w",
                2,
                "-D",
                "-e",
                "FOO=BAR",
                "-e",
                "USE_FORCE=True",
                "--pid",
                pid_file,
                "-c",
                conf_file,
            ],
            {
                "host": "localhost",
                "port": "5000",
                "workers": "2",
                "daemon": True,
                "env": ("FOO=BAR", "USE_FORCE=True"),
                "pid": pid_file,
                "config": conf_file,
            },
        ),
    ],
)
def test_serve_options(run_mock, cli_runner, opts, expected):
    result = cli_runner.invoke(serve, opts)
    assert result.exit_code == 0
    run_mock.assert_called_once_with(**expected)


@pytest.mark.parametrize(
    "opts",
    [
        (["--not_exists"]),
        (["-p", "not number"]),
        (["-c", "/path/does/not/exist"]),
        (["--pid", "/path/does/not/exist"]),
    ],
)
def test_serve_invalid_option(cli_runner, opts):
    result = cli_runner.invoke(serve, opts)
    assert result.exit_code == 2
