import copy

from fastapi_mvc.cli.cli import cli


def test_root(cli_runner):
    result = cli_runner.invoke(cli)
    assert result.exit_code == 0


def test_root_help(cli_runner):
    result = cli_runner.invoke(cli, ["--help"])
    assert result.exit_code == 0


def test_root_invalid_options(cli_runner):
    result = cli_runner.invoke(cli, ["--not_exists"])
    assert result.exit_code == 2


def test_root_with_options(cli_runner):
    result = cli_runner.invoke(cli, ["--verbose", "new", "--help"])
    assert result.exit_code == 0

    result = cli_runner.invoke(cli, ["new", "--help"])
    assert result.exit_code == 0

    result = cli_runner.invoke(cli, ["--verbose", "run", "--help"])
    assert result.exit_code == 0

    result = cli_runner.invoke(cli, ["run", "--help"])
    assert result.exit_code == 0


def test_aliases(cli_runner):
    cli_copy = copy.deepcopy(cli)
    result = cli_runner.invoke(cli_copy, ["n", "--help"])
    assert result.exit_code == 0

    result = cli_runner.invoke(cli_copy, ["r", "--help"])
    assert result.exit_code == 0

    result = cli_runner.invoke(cli_copy, ["g", "--help"])
    assert result.exit_code == 0

    cli_copy.commands["new"] = None
    cli_copy.commands["run"].hidden = True
    result = cli_runner.invoke(cli_copy, ["--help"])
    assert result.exit_code == 0
