import mock
from fastapi_mvc.cli.commands.run import run


def test_run_help(cli_runner):
    result = cli_runner.invoke(run, ["--help"])
    assert result.exit_code == 0


def test_run_invalid_option(cli_runner):
    result = cli_runner.invoke(run, ["--not_exists"])
    assert result.exit_code == 2


@mock.patch("fastapi_mvc.cli.commands.run.IniParser")
@mock.patch("fastapi_mvc.cli.commands.run.uvicorn.run", return_value=0)
def test_run_default_options(uvi_mck, ini_mck, cli_runner):
    ini_mck.return_value.package_name = "foobar"

    result = cli_runner.invoke(run, [])
    assert result.exit_code == 0

    uvi_mck.assert_called_once_with(
        "foobar.app.asgi:application",
        host="127.0.0.1",
        port=8000,
        reload=True,
        workers=1,
        log_config=None,
        access_log=True,
    )


@mock.patch("fastapi_mvc.cli.commands.run.IniParser")
@mock.patch("fastapi_mvc.cli.commands.run.uvicorn.run", return_value=0)
def test_run_with_options(uvi_mck, ini_mck, cli_runner):
    ini_mck.return_value.package_name = "foobar"

    result = cli_runner.invoke(
        run, ["--host", "10.20.30.40", "-p", 1234, "--no-reload", "-w", 2]
    )
    assert result.exit_code == 0

    uvi_mck.assert_called_once_with(
        "foobar.app.asgi:application",
        host="10.20.30.40",
        port=1234,
        reload=False,
        workers=2,
        log_config=None,
        access_log=True,
    )
