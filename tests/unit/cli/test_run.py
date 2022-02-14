import os

import mock
import pytest
from fastapi_mvc.cli.run import run


DATA_DIR = os.path.abspath(
    os.path.join(
        os.path.abspath(__file__),
        "../../data",
    )
)


def test_run_help(cli_runner):
    result = cli_runner.invoke(run, ["--help"])
    assert result.exit_code == 0


def test_run_invalid_options(cli_runner):
    result = cli_runner.invoke(run, ["--not_exists"])
    assert result.exit_code == 2


@mock.patch("fastapi_mvc.cli.run.os.getcwd", return_value=DATA_DIR)
@mock.patch("fastapi_mvc.cli.run.VerifyInstall")
@mock.patch("fastapi_mvc.cli.run.RunUvicorn")
@mock.patch("fastapi_mvc.cli.run.Invoker")
def test_run_default_values(invoker_mock, run_mock, verify_mock, os_mock, cli_runner):
    result = cli_runner.invoke(run, [])
    assert result.exit_code == 0

    os_mock.assert_called_once()
    verify_mock.assert_called_once_with(script_name="test-app")
    invoker_mock.assert_called_once()
    run_mock.assert_called_once_with(
        host="127.0.0.1", port="8000", package_name="test_app",
    )
    assert invoker_mock.return_value.on_start == verify_mock.return_value
    assert invoker_mock.return_value.on_finish == run_mock.return_value
    invoker_mock.return_value.execute.assert_called_once()


@pytest.mark.parametrize(
    "args, expected",
    [
        (
            ["--host", "10.20.30.40", "--port", "1234"],
            {"host": "10.20.30.40", "port": "1234", "package_name": "test_app"}
        ),
        (
            ["--host", "192.168.0.10", "-p", "9001"],
            {"host": "192.168.0.10", "port": "9001", "package_name": "test_app"}
        )
    ]
)
@mock.patch("fastapi_mvc.cli.run.os.getcwd", return_value=DATA_DIR)
@mock.patch("fastapi_mvc.cli.run.VerifyInstall")
@mock.patch("fastapi_mvc.cli.run.RunUvicorn")
@mock.patch("fastapi_mvc.cli.run.Invoker")
def test_run_with_options(invoker_mock, run_mock, verify_mock, os_mock, cli_runner, args, expected):
    result = cli_runner.invoke(run, args)
    assert result.exit_code == 0

    os_mock.assert_called_once()
    verify_mock.assert_called_once_with(script_name="test-app")
    invoker_mock.assert_called_once()
    run_mock.assert_called_once_with(**expected)
    assert invoker_mock.return_value.on_start == verify_mock.return_value
    assert invoker_mock.return_value.on_finish == run_mock.return_value
    invoker_mock.return_value.execute.assert_called_once()
