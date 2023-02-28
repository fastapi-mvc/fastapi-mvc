import pytest

from fastapi_mvc.utils import ensure_permissions, ensure_project_data
from fastapi_mvc.constants import ANSWERS_FILE


class TestEnsureProjectData:

    def test_should_not_raise_when_valid_fastapi_mvc_project_data(self, fake_project, monkeypatch):
        # given
        monkeypatch.chdir(fake_project["root"])

        # then
        project_data = ensure_project_data()

        # then
        assert project_data["project_name"] == "fake-project"
        assert project_data["package_name"] == "fake_project"
        assert project_data["_src_path"] == "https://github.com/fastapi-mvc/copier-project.git"

    def test_should_raise_when_not_valid_fastapi_mvc_project_data(self, fake_project):
        # given / when / then
        with pytest.raises(SystemExit):
            ensure_project_data("/not/fastapi-mvc/project", answers_file=ANSWERS_FILE)
            ensure_project_data(str(fake_project["root"]), answers_file=".invalid_file")


class TestGeneratorEnsurePermissions:

    def test_should_not_raise_when_correct_permissions(self, fake_project, dummy_executable):
        # given / when / then
        ensure_permissions(fake_project["answers_file"])
        ensure_permissions(fake_project["answers_file"], w=True)
        ensure_permissions(dummy_executable, x=True)

    def test_should_raise_when_path_does_not_exists(self):
        # given / when / then
        with pytest.raises(SystemExit):
            ensure_permissions("/not/exist")

    def test_should_raise_when_path_not_readable(self):
        # given / when / then
        with pytest.raises(SystemExit):
            ensure_permissions("/etc/shadow")

    def test_should_raise_when_path_not_writeable(self):
        # given / when / then
        with pytest.raises(SystemExit):
            ensure_permissions("/etc/shadow", r=False, w=True)

    def test_should_raise_when_path_not_executable(self, fake_project):
        # given / when / then
        with pytest.raises(SystemExit):
            ensure_permissions(fake_project["answers_file"], x=True)
