import mock
from {{cookiecutter.package_name}}.cli.commands.serve import serve


def test_serve_help(cli_runner):
    result = cli_runner.invoke(serve, ["--help"])
    assert result.exit_code == 0


@mock.patch("{{cookiecutter.package_name}}.cli.commands.serve.run_wsgi")
def test_serve_options(run_mock, cli_runner, ):
    result = cli_runner.invoke(serve, ["--host", "localhost", "-p", 5000, "-w", 2])
    assert result.exit_code == 0
    run_mock.assert_called_once_with(
        host="localhost",
        port="5000",
        workers="2",
    )


def test_serve_invalid_option(cli_runner):
    result = cli_runner.invoke(serve, ["--not_exists"])
    assert result.exit_code == 2
