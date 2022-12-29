import copy
from unittest import mock

import pytest
from fastapi_mvc.generators import ScriptGenerator


class TestScriptGenerator:

    @pytest.fixture
    def script(self):
        script = copy.deepcopy(ScriptGenerator)
        script.run_copy = mock.Mock()
        yield script
        del script

    def test_should_exit_zero_when_invoked_with_help(self, script, cli_runner):
        # given / when
        result = cli_runner.invoke(script, ["--help"])

        # then
        assert result.exit_code == 0

    def test_should_exit_error_when_invoked_with_invalid_option(self, script, cli_runner):
        # given / when
        result = cli_runner.invoke(ScriptGenerator, ["--not_exists"])

        # then
        assert result.exit_code == 2

    def test_should_call_copier_using_default_values(self, script, cli_runner):
        # given / when
        result = cli_runner.invoke(script, ["fake-script.sh"])

        # then
        assert result.exit_code == 0
        script.run_copy.assert_called_once_with(
            data={
                "nix": False,
                "script": "fake-script.sh",
            },
            answers_file=None,
        )

    def test_should_call_copier_with_parsed_arguments(self, script, cli_runner):
        # given / when
        result = cli_runner.invoke(script, ["-n", "Mambo-No6"])

        # then
        assert result.exit_code == 0
        script.run_copy.assert_called_once_with(
            data={
                "nix": True,
                "script": "mambo-no6",
            },
            answers_file=None,
        )
