import pytest

from fastapi_mvc.utils import ensure_permissions, ensure_project_data


class TestEnsureProjectData:

    def test_should_not_raise_when_valid_fastapi_mvc_project_data(self):
        # given
        project_data = {
            "_commit": "0.4.0",
            "_src_path": "https://github.com/fastapi-mvc/copier-project.git",
            "aiohttp": True,
            "author": "John Doe",
            "chart_name": "fake-project",
            "container_image_name": "fake-project",
            "copyright_date": "2023",
            "email": "example@email.com",
            "fastapi_mvc_version": "0.26.0",
            "github_actions": True,
            "helm": True,
            "license": "MIT",
            "nix": True,
            "package_name": "fake_project",
            "project_description": "This project was generated with fastapi-mvc.",
            "project_name": "fake-project",
            "redis": True,
            "repo_url": "https://your.repo.url.here",
            "script_name": "fake-project",
            "version": "0.1.0"
        }

        # when / then
        ensure_project_data(project_data)

    def test_should_raise_when_not_valid_fastapi_mvc_project_data(self):
        # given
        project_data = {}

        # when / then
        with pytest.raises(SystemExit):
            ensure_project_data(project_data)


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
