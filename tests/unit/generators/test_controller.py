import copy
from unittest import mock

import pytest
from fastapi_mvc.generators import ControllerGenerator
from fastapi_mvc.constants import COPIER_CONTROLLER
from fastapi_mvc.generators.controller import insert_router_import


router_content = """\
from fastapi import APIRouter
from fake_project.app.controllers import ready

root_api_router = APIRouter(prefix="/api")

root_api_router.include_router(ready.router, tags=["ready"])
"""
router2_content = """\
import fastapi
from fake_project.app.controllers import ready

root_api_router = fastapi.APIRouter(prefix="/api")

root_api_router.include_router(ready.router, tags=["ready"])
"""
router_expected = """\
from fastapi import APIRouter
from fake_project.app.controllers import fake_router
from fake_project.app.controllers import ready

root_api_router = APIRouter(prefix="/api")

root_api_router.include_router(ready.router, tags=["ready"])
root_api_router.include_router(fake_router.router)
"""
router2_expected = """\
from fake_project.app.controllers import fake_router
import fastapi
from fake_project.app.controllers import ready

root_api_router = fastapi.APIRouter(prefix="/api")

root_api_router.include_router(ready.router, tags=["ready"])
root_api_router.include_router(fake_router.router)
"""


@pytest.fixture
def fake_router(fake_project):
    router = fake_project["app_dir"] / "router.py"
    router.write_text(router_content)

    yield router
    router.unlink()


@pytest.fixture
def fake_router2(fake_project):
    router2 = fake_project["app_dir"] / "router.py"
    router2.write_text(router2_content)

    yield router2
    router2.unlink()


class TestGeneratorInsertRouterPath:

    def test_should_insert_router_import(self, monkeypatch, fake_project, fake_router):
        # given
        monkeypatch.chdir(fake_project["root"])

        # when
        insert_router_import("fake_project", "fake_router")
        # test idempotence
        insert_router_import("fake_project", "fake_router")

        # then
        assert fake_router.read_text() == router_expected

    def test_should_insert_router_import_at_file_end(self, monkeypatch, fake_project, fake_router2):
        # given
        monkeypatch.chdir(fake_project["root"])

        # when
        insert_router_import("fake_project", "fake_router")
        # test idempotence
        insert_router_import("fake_project", "fake_router")

        # then
        assert fake_router2.read_text() == router2_expected


class TestControllerGenerator:

    @pytest.fixture
    def controller(self):
        controller = copy.deepcopy(ControllerGenerator)
        copier_patch = mock.patch(
            "fastapi_mvc.generators.controller.copier",
        )
        insert_patch = mock.patch("fastapi_mvc.generators.controller.insert_router_import")
        controller.copier = copier_patch.start()
        controller.insert_router_import = insert_patch.start()
        yield controller
        copier_patch.stop()
        insert_patch.stop()
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
        controller.copier.run_copy.assert_called_once_with(
            src_path=COPIER_CONTROLLER.template,
            vcs_ref=COPIER_CONTROLLER.vcs_ref,
            dst_path=str(fake_project["root"]),
            data={
                "project_name": "fake-project",
                "controller": "fake_controller",
                "endpoints": {},
            }
        )
        controller.insert_router_import.assert_called_once_with("fake_project", "fake_controller")

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
        controller.copier.run_copy.assert_called_once_with(
            src_path=COPIER_CONTROLLER.template,
            vcs_ref=COPIER_CONTROLLER.vcs_ref,
            dst_path=str(fake_project["root"]),
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
        controller.copier.run_copy.assert_called_once_with(
            src_path=COPIER_CONTROLLER.template,
            vcs_ref=COPIER_CONTROLLER.vcs_ref,
            dst_path=str(fake_project["root"]),
            data={
                "project_name": "fake-project",
                "controller": "fake_controller",
                "endpoints": {},
            }
        )
        controller.insert_router_import.assert_not_called()

    def test_should_exit_error_when_not_in_fastapi_mvc_project(self, controller, cli_runner, caplog):
        # given / when
        result = cli_runner.invoke(controller, ["fake-controller"])

        # then
        assert result.exit_code == 1
        msg = "Not a fastapi-mvc project. Try 'fastapi-mvc new --help' for details how to create one."
        assert msg in caplog.text
