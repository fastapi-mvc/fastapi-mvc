import pytest

from fastapi_mvc.utils import ensure_permissions, require_fastapi_mvc_project, load_answers_file
from fastapi_mvc.constants import ANSWERS_FILE


class TestLoadAnswersFile:

    def test_should_return_loaded_answers_file_using_defaults(self, fake_project, monkeypatch):
        # given
        monkeypatch.chdir(fake_project["root"])

        # when
        project_data = load_answers_file()

        # then
        assert project_data["project_name"] == "fake-project"
        assert project_data["package_name"] == "fake_project"
        assert project_data["_src_path"] == "https://github.com/fastapi-mvc/copier-project.git"

    def test_should_return_loaded_answers_file(self, fake_project):
        # given
        project_root = str(fake_project["root"])
        answers_file = ANSWERS_FILE

        # when
        project_data = load_answers_file(project_root, answers_file)

        # then
        assert project_data["project_name"] == "fake-project"
        assert project_data["package_name"] == "fake_project"
        assert project_data["_src_path"] == "https://github.com/fastapi-mvc/copier-project.git"

    def test_should_return_empty_dict(self):
        # given / when
        project_data = load_answers_file("/path/not/exist", ".foobar.yml")

        # then
        assert not project_data


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


class TestRequireFastapiMvcProject:

    @pytest.fixture
    def incomplete_answers_file(self, tmp_path):
        file = tmp_path / ANSWERS_FILE
        file.write_text(
            """_commit: efb938e\n_src_path: /tmp\npackage_name: fake_project\n"""
        )
        return file

    def test_should_not_raise_when_valid_fastapi_mvc_project(self, fake_project, monkeypatch):
        # given
        monkeypatch.chdir(fake_project["root"])

        # then
        project_data = require_fastapi_mvc_project()

        # then
        assert project_data["project_name"] == "fake-project"
        assert project_data["package_name"] == "fake_project"
        assert project_data["_src_path"] == "https://github.com/fastapi-mvc/copier-project.git"

    def test_should_raise_when_fastapi_mvc_project_data_empty(self):
        # given / when / then
        with pytest.raises(SystemExit):
            require_fastapi_mvc_project()

    def test_should_raise_when_not_valid_fastapi_mvc_project_data(self, monkeypatch, incomplete_answers_file):
        # given
        monkeypatch.chdir(incomplete_answers_file.parent)

        # when / then
        with pytest.raises(SystemExit):
            require_fastapi_mvc_project()
