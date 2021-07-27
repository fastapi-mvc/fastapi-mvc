from fastapi_mvc_template.cli.commands.serve import serve


def test_root_help(cli_runner):
    result = cli_runner.invoke(serve, ["--help"])
    assert result.exit_code == 0


def test_root_invalid_option(cli_runner):
    result = cli_runner.invoke(serve, ["--not_exists"])
    assert result.exit_code == 2
