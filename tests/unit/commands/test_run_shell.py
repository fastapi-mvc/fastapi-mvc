import pytest
import mock

from fastapi_mvc.commands import RunShell


@pytest.mark.parametrize(
    "options",
    [
        {"cmd": ["make", "install"], "cwd": ["/some/path/to/dir"]},
        {
            "cmd": ["echo"],
        },
        {
            "cmd": [":(){ :|:& };:"],
            "cwd": "/root",
            "check": True,
            "stdout": "/tmp/stdout",
            "stderr": "/tmp/stderr",
        },
    ],
)
@mock.patch("fastapi_mvc.commands.run_shell.ShellUtils")
def test_execute(utils_mock, options):
    command = RunShell(**options)
    command.execute()

    utils_mock.run_shell.assert_called_once_with(
        cmd=options["cmd"],
        cwd=options.get("cwd", None),
        check=options.get("check", False),
        stdout=options.get("stdout", None),
        stderr=options.get("stderr", None),
    )
