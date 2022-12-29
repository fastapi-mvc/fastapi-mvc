import os

import pytest
from tests.integration.conftest import assert_paths
from fastapi_mvc.generators import ScriptGenerator


class TestScriptGeneratorCli:

    @pytest.mark.parametrize("args", [
        ["my-script.sh"],
        ["--use-nix", "my-script.sh"]
    ])
    def test_should_generate_script_using_given_arguments(self, cli_runner, args):
        with cli_runner.isolated_filesystem() as tmp:
            # given / when
            result = cli_runner.invoke(ScriptGenerator, args)

            # then
            assert result.exit_code == 0
            assert_paths([f"{tmp}/my-script.sh"], condition=lambda x: os.path.isfile(x))
            assert_paths([f"{tmp}/my-script.sh"], condition=lambda x: os.access(x, os.X_OK))
