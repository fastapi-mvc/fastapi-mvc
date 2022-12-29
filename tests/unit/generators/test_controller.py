import copy
from unittest import mock

import pytest
from fastapi_mvc.generators import ControllerGenerator


class TestControllerGenerator:

    @pytest.fixture
    def controller(self):
        controller = copy.deepcopy(ControllerGenerator)
        controller.run_copy = mock.Mock()
        controller.insert_router_import = mock.Mock()
        yield controller
        del controller

    def test_should_exit_zero_when_invoked_with_help(self, controller, cli_runner):
        # given / when
        result = cli_runner.invoke(controller, ["--help"])

        # then
        assert result.exit_code == 0

    def test_should_exit_error_when_invoked_with_invalid_option(self, controller, cli_runner):
        # given / when
        result = cli_runner.invoke(controller, ["--not_exists"])

        # then
        assert result.exit_code == 2

    def test_should_call_copier_using_default_values(self, controller, monkeypatch, fake_project, cli_runner):
        # given / when
        monkeypatch.chdir(fake_project["root"])
        result = cli_runner.invoke(controller, ["fake-controller"])

        # then
        assert result.exit_code == 0
        controller.run_copy.assert_called_once_with(
            data={
                "project_name": "fake-project",
                "controller": "fake_controller",
                "endpoints": {},
            }
        )
        controller.insert_router_import.assert_called_once_with("fake_controller")

    def test_should_call_copier_with_parsed_arguments(self, controller, monkeypatch, fake_project, cli_runner):
        # given / when
        monkeypatch.chdir(fake_project["root"])
        result = cli_runner.invoke(
            controller,
            [
                "--skip-routes",
                "STOCK-MARKET",
                "ticker",
                "buy:post",
                "sell:delete",
            ],
        )

        # then
        assert result.exit_code == 0
        controller.run_copy.assert_called_once_with(
            data={
                "project_name": "fake-project",
                "controller": "stock_market",
                "endpoints": {
                    "ticker": "get",
                    "buy": "post",
                    "sell": "delete",
                },
            }
        )

    def test_should_skip_router_import_insert(self, controller, monkeypatch, fake_project, cli_runner):
        # given / when
        monkeypatch.chdir(fake_project["root"])
        result = cli_runner.invoke(
            controller,
            ["fake-controller", "--skip-routes"],
        )

        # then
        assert result.exit_code == 0
        controller.run_copy.assert_called_once_with(
            data={
                "project_name": "fake-project",
                "controller": "fake_controller",
                "endpoints": {},
            }
        )
        controller.insert_router_import.assert_not_called()

    def test_should_exit_error_when_not_in_fastapi_mvc_project(self, controller, cli_runner):
        # given / when
        result = cli_runner.invoke(controller, ["fake-controller"])

        # then
        assert result.exit_code == 1
        msg = "Not a fastapi-mvc project. Try 'fastapi-mvc new --help' for details how to create one."
        assert msg in result.output
