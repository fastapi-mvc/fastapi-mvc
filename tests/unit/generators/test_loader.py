from unittest import mock

from fastapi_mvc.generators import load_generators


class TestLoadGenerators:

    def test_should_load_custom_generators_from_default_path(self, monkeypatch, fake_project_with_generators):
        # given
        monkeypatch.chdir(fake_project_with_generators["root"])

        # when
        generators = load_generators()

        # then
        assert sorted(generators.keys()) == sorted(
            ["controller", "foobar", "generator", "my-controller", "script"]
        )

    @mock.patch("fastapi_mvc.generators.loader.importlib.util")
    def test_should_continue_on_import_error(self, importlib_mock, monkeypatch, fake_project_with_generators):
        # given
        monkeypatch.chdir(fake_project_with_generators["root"])
        spec_mock = mock.Mock()
        spec_mock.loader.exec_module.side_effect = ImportError("Ups")
        importlib_mock.spec_from_file_location.return_value = spec_mock

        # when
        generators = load_generators()

        # then
        assert sorted(generators.keys()) == sorted(
            ["controller", "generator", "script"]
        )

    def test_should_load_generators_from_custom_path(self, monkeypatch, fake_project_with_generators):
        # given
        monkeypatch.setenv(
            "FMVC_PATH", str(fake_project_with_generators["generators_dir"])
        )

        # when
        generators = load_generators()

        # then
        assert sorted(generators.keys()) == sorted(
            ["controller", "foobar", "generator", "my-controller", "script"]
        )
