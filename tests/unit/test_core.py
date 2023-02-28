import os
from unittest import mock

import pytest
from fastapi_mvc import Generator, Command, ANSWERS_FILE


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


class TestCommand:

    def test_should_create_command_and_populate_defaults(self):
        # given / when
        command = Command(name="fake-command")

        # then
        assert command.name == "fake-command"
        assert not command.alias
        assert not command.project_data


class TestCommandEnsureProjectData:

    def test_should_not_raise_when_valid_fastapi_mvc_project(self, fake_project, monkeypatch):
        # given
        command = Command(name="fake-command")
        monkeypatch.chdir(fake_project["root"])

        # when
        command.ensure_project_data()

        # then
        assert command.project_data["package_name"] == "fake_project"
        assert command.project_data["project_name"] == "fake-project"

    def test_should_raise_when_not_fastapi_mvc_project(self):
        # given
        command = Command(name="fake-command")

        # when / then
        with pytest.raises(SystemExit):
            command.ensure_project_data()


class TestGenerator:

    def test_should_create_generator_and_populate_defaults(self):
        # given / when
        generator = Generator(name="fake-generator", template="https://fake.repo.git")

        # then
        assert generator.template == "https://fake.repo.git"
        assert not generator.vcs_ref
        assert generator.category == "Other"


class TestGeneratorEnsurePermissions:

    def test_should_not_raise_when_correct_permissions(self, fake_project, dummy_executable):
        # given
        generator = Generator(name="fake-generator", template="https://fake.repo.git")

        # when / then
        generator.ensure_permissions(fake_project["answers_file"])
        generator.ensure_permissions(fake_project["answers_file"], w=True)
        generator.ensure_permissions(dummy_executable, x=True)

    def test_should_raise_when_path_does_not_exists(self):
        # given
        generator = Generator(name="fake-generator", template="https://fake.repo.git")

        # when / then
        with pytest.raises(SystemExit):
            generator.ensure_permissions("/not/exist")

    def test_should_raise_when_path_not_readable(self):
        # given
        generator = Generator(name="fake-generator", template="https://fake.repo.git")

        # when / then
        with pytest.raises(SystemExit):
            generator.ensure_permissions("/etc/shadow")

    def test_should_raise_when_path_not_writeable(self):
        # given
        generator = Generator(name="fake-generator", template="https://fake.repo.git")

        # when / then
        with pytest.raises(SystemExit):
            generator.ensure_permissions("/etc/shadow", r=False, w=True)

    def test_should_raise_when_path_not_executable(self, fake_project):
        # given
        generator = Generator(name="fake-generator", template="https://fake.repo.git")

        # when / then
        with pytest.raises(SystemExit):
            generator.ensure_permissions(fake_project["answers_file"], x=True)


class TestGeneratorInsertRouterPath:

    def test_should_insert_router_import(self, monkeypatch, fake_project, fake_router):
        # given
        monkeypatch.chdir(fake_project["root"])
        generator = Generator(name="fake-generator", template="https://fake.repo.git")
        generator.ensure_project_data()

        # when
        generator.insert_router_import("fake_router")
        # test idempotence
        generator.insert_router_import("fake_router")

        # then
        assert fake_router.read_text() == router_expected

    def test_should_insert_router_import_at_file_end(self, monkeypatch, fake_project, fake_router2):
        # given
        monkeypatch.chdir(fake_project["root"])
        generator = Generator(name="fake-generator", template="https://fake.repo.git")
        generator.ensure_project_data()

        # when
        generator.insert_router_import("fake_router")
        # test idempotence
        generator.insert_router_import("fake_router")

        # then
        assert fake_router2.read_text() == router2_expected


class TestGeneratorRunCopy:

    @mock.patch("fastapi_mvc.core.copier")
    def test_should_call_copier_run_copy_with_defaults(self, copier_mock):
        # given
        generator = Generator(
            name="fake-generator",
            template="https://fake.repo.git",
            vcs_ref="master",
            category="Fake",
        )

        # when
        generator.run_copy(dst_path="/tmp/test", data={"foo": "bar"})

        # then
        copier_mock.run_copy.assert_called_once_with(
            src_path=generator.template,
            dst_path="/tmp/test",
            vcs_ref=generator.vcs_ref,
            answers_file=ANSWERS_FILE,
            data={"foo": "bar"},
        )


class TestGeneratorRunUpdate:

    @mock.patch("fastapi_mvc.core.copier")
    def test_should_call_copier_run_update_with_defaults(self, copier_mock):
        # given
        generator = Generator(
            name="fake-generator",
            template="https://fake.repo.git",
            vcs_ref="master",
            category="Fake",
        )

        # when
        generator.run_update(dst_path="/tmp/test", data={"foo": "bar"})

        # then
        copier_mock.run_update.assert_called_once_with(
            dst_path="/tmp/test",
            vcs_ref=generator.vcs_ref,
            answers_file=ANSWERS_FILE,
            data={"foo": "bar"},
        )
