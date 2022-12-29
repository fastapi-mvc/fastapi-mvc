import copy

import pytest
from fastapi_mvc.cli.cli import cli


class TestCliRoot:

    def test_should_exit_zero_when_invoked_empty(self, cli_runner):
        # given / when
        result = cli_runner.invoke(cli)

        # then
        assert result.exit_code == 0

    def test_should_exit_zero_when_invoked_with_help(self, cli_runner):
        # given / when
        result = cli_runner.invoke(cli, ["--help"])

        # then
        assert result.exit_code == 0

    def test_should_exit_error_when_invoked_with_invalid_option(self, cli_runner):
        # given / when
        result = cli_runner.invoke(cli, ["--not_exists"])

        # then
        assert result.exit_code == 2

    @pytest.mark.parametrize("args", [
        ["--verbose", "new", "--help"],
        ["new", "--help"],
        ["--verbose", "run", "--help"],
        ["run", "--help"],
    ])
    def test_should_exit_zero_when_invoked_with_options(self, cli_runner, args):
        # given / when
        result = cli_runner.invoke(cli, args)

        # then
        assert result.exit_code == 0

    @pytest.mark.parametrize("args", [
        ["n", "--help"],
        ["r", "--help"],
        ["g", "--help"],
    ])
    def test_should_exit_zero_when_invoked_using_aliases(self, cli_runner, args):
        # given / when
        result = cli_runner.invoke(cli, args)

        # then
        assert result.exit_code == 0

    def test_should_exit_zero_when_subcommand_is_hidden_or_none(self, cli_runner):
        # given
        cli_copy = copy.deepcopy(cli)
        cli_copy.commands["new"] = None
        cli_copy.commands["run"].hidden = True

        # when
        result = cli_runner.invoke(cli_copy, ["--help"])

        # then
        assert result.exit_code == 0
