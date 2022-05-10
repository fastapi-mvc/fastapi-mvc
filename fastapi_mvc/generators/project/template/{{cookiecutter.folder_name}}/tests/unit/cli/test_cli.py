from {{cookiecutter.package_name}}.cli import cli


def test_root(cli_runner):
    result = cli_runner.invoke(cli)
    assert result.exit_code == 0


def test_root_options(cli_runner):
    result = cli_runner.invoke(cli, ["--verbose", "serve", "--help"])
    assert result.exit_code == 0
    result = cli_runner.invoke(cli, ["serve", "--help"])
    assert result.exit_code == 0


def test_root_help(cli_runner):
    result = cli_runner.invoke(cli, ["--help"])
    assert result.exit_code == 0


def test_root_invalid_option(cli_runner):
    result = cli_runner.invoke(cli, ["--not_exists"])
    assert result.exit_code == 2
