import copy
from unittest import mock

import pytest
from fastapi_mvc.generators import ScriptGenerator
from fastapi_mvc.constants import COPIER_SCRIPT


class TestScriptGenerator:

    @pytest.fixture
    def script(self):
        script = copy.deepcopy(ScriptGenerator)
        copier_patch = mock.patch(
            "fastapi_mvc.generators.script.copier",
        )
        script.copier = copier_patch.start()
        yield script
        copier_patch.stop()
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
        script.copier.run_copy.assert_called_once_with(
            src_path=COPIER_SCRIPT.template,
            vcs_ref=COPIER_SCRIPT.vcs_ref,
            data={
                "nix": False,
                "script": "fake-script.sh",
            },
            unsafe=True,
        )

    def test_should_call_copier_with_parsed_arguments(self, script, cli_runner):
        # given / when
        result = cli_runner.invoke(script, ["-n", "Mambo-No6"])

        # then
        assert result.exit_code == 0
        script.copier.run_copy.assert_called_once_with(
            src_path=COPIER_SCRIPT.template,
            vcs_ref=COPIER_SCRIPT.vcs_ref,
            data={
                "nix": True,
                "script": "mambo-no6",
            },
            unsafe=True,
        )
