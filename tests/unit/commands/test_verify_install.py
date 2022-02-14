from subprocess import DEVNULL

import mock
import pytest
from fastapi_mvc.commands import VerifyInstall
from fastapi_mvc.exceptions import CommandException


@pytest.mark.parametrize(
    "script_name",
    [
        "app-script",
        "foobar",
    ]
)
@mock.patch(
    "fastapi_mvc.commands.verify_install.ShellUtils.run_shell",
    return_value=mock.Mock(returncode=0)
)
def test_execute(run_mock, script_name):
    command = VerifyInstall(script_name=script_name)
    command.execute()

    run_mock.assert_called_once_with(
        cmd=[
            "poetry",
            "run",
            script_name,
            "--help",
        ],
        stdout=DEVNULL,
        stderr=DEVNULL,
    )


@mock.patch(
    "fastapi_mvc.commands.verify_install.ShellUtils.run_shell",
    return_value=mock.Mock(returncode=1)
)
def test_execute_exception(run_mock):
    with pytest.raises(CommandException) as ex:
        command = VerifyInstall(script_name="foobar")
        command.execute()

        assert str(ex) == "Project not installed."
        run_mock.assert_called_once_with(
            cmd=[
                "poetry",
                "run",
                "foobar",
                "--help",
            ],
            stdout=DEVNULL,
            stderr=DEVNULL,
        )
