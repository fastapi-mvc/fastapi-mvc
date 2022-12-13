import os
from unittest import mock

import pytest
from fastapi_mvc.generators import ControllerGenerator


DATA_DIR = os.path.abspath(
    os.path.join(
        os.path.abspath(__file__),
        "../../data",
    )
)


def test_controller_help(cli_runner):
    result = cli_runner.invoke(ControllerGenerator, ["--help"])
    assert result.exit_code == 0


def test_controller_invalid_options(cli_runner):
    result = cli_runner.invoke(ControllerGenerator, ["--not_exists"])
    assert result.exit_code == 2


@mock.patch("fastapi_mvc.generators.controller.Generator.insert_router_import")
@mock.patch("fastapi_mvc.generators.controller.Generator.run_copy")
def test_controller_default_values(copier_mock, instert_mock, monkeypatch, cli_runner):
    # Change working directory to fake project. It is easier to fake fastapi-mvc project,
    # rather than mocking ctx injected to command via @click.pass_context decorator.
    monkeypatch.chdir(DATA_DIR)

    result = cli_runner.invoke(ControllerGenerator, ["custom-controller"])
    assert result.exit_code == 0

    instert_mock.assert_called_once_with("custom_controller")
    copier_mock.assert_called_once_with(
        data={
            "project_name": "test-app",
            "controller": "custom_controller",
            "endpoints": {},
        }
    )


@pytest.mark.parametrize(
    "args, expected",
    [
        (
            [
                "--skip-routes",
                "STOCK-MARKET",
                "ticker",
                "buy:post",
                "sell:delete",
            ],
            {
                "project_name": "test-app",
                "controller": "stock_market",
                "endpoints": {
                    "ticker": "get",
                    "buy": "post",
                    "sell": "delete",
                },
            },
        ),
        (
            [
                "-R",
                "invoker",
                "execute:POST",
                "cancel-launch:PUt",
            ],
            {
                "project_name": "test-app",
                "controller": "invoker",
                "endpoints": {
                    "execute": "post",
                    "cancel_launch": "put",
                },
            },
        ),
    ],
)
@mock.patch("fastapi_mvc.generators.controller.Generator.insert_router_import")
@mock.patch("fastapi_mvc.generators.controller.Generator.run_copy")
def test_controller_with_options(
    copier_mock, instert_mock, monkeypatch, cli_runner, args, expected
):
    # Change working directory to fake project. It is easier to fake fastapi-mvc project,
    # rather than mocking ctx injected to command via @click.pass_context decorator.
    monkeypatch.chdir(DATA_DIR)
    result = cli_runner.invoke(ControllerGenerator, args)
    assert result.exit_code == 0

    copier_mock.assert_called_once_with(data=expected)
    if "-R" in args or "--skip-routes" in args:
        instert_mock.assert_not_called()
    else:
        instert_mock.assert_called_once_with(expected["controller"])


def test_controller_not_in_project(cli_runner):
    result = cli_runner.invoke(ControllerGenerator, ["custom-controller"])
    assert result.exit_code == 1
    msg = "Not a fastapi-mvc project. Try 'fastapi-mvc new --help' for details how to create one."
    assert msg in result.output
