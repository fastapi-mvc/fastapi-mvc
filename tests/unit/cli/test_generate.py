import pytest
from fastapi_mvc.cli.generate import get_generate_cmd


class TestCliGenerateCommand:

    def test_should_exit_zero_when_invoked_with_help(self, monkeypatch, fake_project_with_generators, cli_runner):
        # given / when
        monkeypatch.chdir(fake_project_with_generators["root"])
        result = cli_runner.invoke(get_generate_cmd(), ["--help"])

        # then
        assert result.exit_code == 0

    def test_should_exit_error_when_invoked_with_invalid_option(self, cli_runner):
        # given / when
        result = cli_runner.invoke(get_generate_cmd(), ["--not_exists"])

        # then
        assert result.exit_code == 2

    @pytest.mark.parametrize(
        "name",
        [
            "controller",
            "ctl",
            "generator",
            "gen",
            "foobar",
            "foo",
            "my-controller",
            "my-ctl",
        ],
    )
    def test_should_exit_zero_when_invoked_existing_generator(self, monkeypatch, fake_project_with_generators, cli_runner, name):
        # given / when
        monkeypatch.chdir(fake_project_with_generators["root"])
        result = cli_runner.invoke(get_generate_cmd(), [name, "--help"])

        # then
        assert result.exit_code == 0

    def test_should_exit_error_when_invoked_not_existing_generator(self, monkeypatch, fake_project, cli_runner):
        # given / when
        monkeypatch.chdir(fake_project["root"])
        result = cli_runner.invoke(get_generate_cmd(), ["notexist", "--help"])

        # then
        assert result.exit_code == 2
