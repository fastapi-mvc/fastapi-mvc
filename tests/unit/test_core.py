import os
from unittest import mock

import pytest
from fastapi_mvc import Generator, Command, ANSWERS_FILE


DATA_DIR = os.path.abspath(
    os.path.join(
        os.path.abspath(__file__),
        "../data",
    )
)
router_content = """\
from fastapi import APIRouter
from example.app.controllers import ready

root_api_router = APIRouter(prefix="/api")

root_api_router.include_router(ready.router, tags=["ready"])
"""
router_expected = """\
from fastapi import APIRouter
from example.app.controllers import test
from example.app.controllers import ready

root_api_router = APIRouter(prefix="/api")

root_api_router.include_router(ready.router, tags=["ready"])
root_api_router.include_router(test.router)
"""
router2_content = """\
import fastapi
from example.app.controllers import ready

root_api_router = fastapi.APIRouter(prefix="/api")

root_api_router.include_router(ready.router, tags=["ready"])
"""
router2_expected = """\
import fastapi
from example.app.controllers import ready

root_api_router = fastapi.APIRouter(prefix="/api")

root_api_router.include_router(ready.router, tags=["ready"])
from example.app.controllers import test
root_api_router.include_router(test.router)
"""



@pytest.fixture
def cmd_obj():
    yield Command(name="test")


@pytest.fixture
def gen_obj():
    yield Generator(
        name="test",
        template="https://my.repo.git",
        vcs_ref="master",
        category="Custom",
    )


def test_command_poetry_path(cmd_obj):
    env = {"POETRY_BINARY": "/path/to/poetry"}
    with mock.patch.dict(os.environ, env, clear=True):
        assert cmd_obj.poetry_path == "/path/to/poetry"

    env = {"POETRY_HOME": "/opt/poetry"}
    with mock.patch.dict(os.environ, env, clear=True):
        assert cmd_obj.poetry_path == "/opt/poetry/venv/bin/poetry"

    env = {"HOME": "/home/john"}
    with mock.patch.dict(os.environ, env, clear=True):
        assert cmd_obj.poetry_path == "/home/john/.local/share/pypoetry/venv/bin/poetry"


def test_command_ensure_project_data(monkeypatch, cmd_obj):
    with pytest.raises(SystemExit):
        cmd_obj.ensure_project_data()

    # Change working directory to fake project. It is easier to fake fastapi-mvc project,
    # rather than mocking ctx injected to command via @click.pass_context decorator.
    monkeypatch.chdir(DATA_DIR)
    cmd_obj.ensure_project_data()
    assert cmd_obj.project_data["package_name"] == "test_app"
    assert cmd_obj.project_data["project_name"] == "test-app"


@mock.patch("fastapi_mvc.core.copier")
def test_generator_run_auto(copier_mock, gen_obj):
    gen_obj.run_auto(dst_path="/tmp/test", data={"foo": "bar"})
    copier_mock.run_auto.assert_called_once_with(
        src_path=gen_obj.template,
        dst_path="/tmp/test",
        vcs_ref=gen_obj.vcs_ref,
        answers_file=ANSWERS_FILE,
        data={"foo": "bar"},
    )


@mock.patch("fastapi_mvc.core.copier")
def test_generator_run_copy(copier_mock, gen_obj):
    gen_obj.run_copy(dst_path="/tmp/test", data={"foo": "bar"})
    copier_mock.run_copy.assert_called_once_with(
        src_path=gen_obj.template,
        dst_path="/tmp/test",
        vcs_ref=gen_obj.vcs_ref,
        answers_file=ANSWERS_FILE,
        data={"foo": "bar"},
    )

@mock.patch("fastapi_mvc.core.copier")
def test_generator_run_update(copier_mock, gen_obj):
    gen_obj.run_update(dst_path="/tmp/test", data={"foo": "bar"})
    copier_mock.run_update.assert_called_once_with(
        dst_path="/tmp/test",
        vcs_ref=gen_obj.vcs_ref,
        answers_file=ANSWERS_FILE,
        data={"foo": "bar"},
    )


@mock.patch("fastapi_mvc.core.copier")
def test_generator_run_auto_overrides(copier_mock, gen_obj):
    gen_obj.template = "./."
    gen_obj.vcs_ref = None
    gen_obj.run_auto(dst_path="/tmp/test", data={"foo": "bar"})
    copier_mock.run_auto.assert_called_once_with(
        src_path="./.",
        dst_path="/tmp/test",
        vcs_ref=None,
        answers_file=ANSWERS_FILE,
        data={"foo": "bar"},
    )


@mock.patch("fastapi_mvc.core.copier")
def test_generator_run_copy_overrides(copier_mock, gen_obj):
    gen_obj.template = "./."
    gen_obj.vcs_ref = None
    gen_obj.run_copy(dst_path="/tmp/test", data={"foo": "bar"})
    copier_mock.run_copy.assert_called_once_with(
        src_path="./.",
        dst_path="/tmp/test",
        vcs_ref=None,
        answers_file=ANSWERS_FILE,
        data={"foo": "bar"},
    )

@mock.patch("fastapi_mvc.core.copier")
def test_generator_run_update_overrides(copier_mock, gen_obj):
    gen_obj.vcs_ref = None
    gen_obj.run_update(dst_path="/tmp/test", data={"foo": "bar"})
    copier_mock.run_update.assert_called_once_with(
        dst_path="/tmp/test",
        vcs_ref=None,
        answers_file=ANSWERS_FILE,
        data={"foo": "bar"},
    )


@pytest.mark.parametrize(
    "content, expected", [
        (router_content, router_expected),
        (router2_content, router2_expected),
    ]
)
@mock.patch("fastapi_mvc.core.os.getcwd")
def test_generator_insert_router_import(cwd_mock, tmp_path, gen_obj, content, expected):
    gen_obj.project_data = {"package_name": "example" }
    root = tmp_path / "example"
    root.mkdir()
    app = root / "example" / "app"
    app.mkdir(parents=True)
    router = app / "router.py"
    router.write_text(content)

    cwd_mock.return_value = str(root)
    gen_obj.insert_router_import("test")
    router.read_text() == expected
    gen_obj.insert_router_import("test")
    router.read_text() == expected
