import mock
from fastapi_mvc.cli.commands.run import run


def test_run_help(cli_runner):
    result = cli_runner.invoke(run, ["--help"])
    assert result.exit_code == 0


def test_run_invalid_option(cli_runner):
    result = cli_runner.invoke(run, ["--not_exists"])
    assert result.exit_code == 2


@mock.patch("fastapi_mvc.cli.commands.run.IniParser")
@mock.patch("fastapi_mvc.cli.commands.new.ShellUtils.run_shell")
def test_run_default_options(utils_mck, ini_mck, cli_runner):
    ini_mck.return_value.package_name = "foobar"

    result = cli_runner.invoke(run, [])
    assert result.exit_code == 0

    utils_mck.assert_called_once_with(
        [
            "poetry",
            "run",
            "uvicorn",
            "--host",
            "127.0.0.1",
            "--port",
            "8000",
            "--reload",
            "foobar.app.asgi:application",
        ]
    )


@mock.patch("fastapi_mvc.cli.commands.run.IniParser")
@mock.patch("fastapi_mvc.cli.commands.new.ShellUtils.run_shell")
def test_run_with_options(utils_mck, ini_mck, cli_runner):
    ini_mck.return_value.package_name = "foobar"

    result = cli_runner.invoke(
        run, ["--host", "10.20.30.40", "-p", "1234"]
    )
    assert result.exit_code == 0

    utils_mck.assert_called_once_with(
        [
            "poetry",
            "run",
            "uvicorn",
            "--host",
            "10.20.30.40",
            "--port",
            "1234",
            "--reload",
            "foobar.app.asgi:application",
        ]
    )
