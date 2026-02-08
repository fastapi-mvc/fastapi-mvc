"""Fastapi-mvc utilities - shell.

Attributes:
    log (logging.Logger): Logger class object instance.

"""

from typing import Tuple, List, IO, AnyStr, Optional, Union, Any
import os
import logging
import subprocess
import shutil

log = logging.getLogger(__name__)


def get_poetry_path() -> str:
    """Get Poetry executable abspath.

    Returns:
        Poetry executable abspath.

    """
    poetry_path = os.getenv("POETRY_BINARY", "")

    if not poetry_path:
        poetry_home = os.getenv(
            "POETRY_HOME", f"{os.getenv('HOME')}/.local/share/pypoetry"
        )
        return f"{poetry_home}/venv/bin/poetry"

    return poetry_path


def get_git_user_info() -> Tuple[str, str]:
    """Get git user information.

    Reads username and email information from git. If not exists, provide defaults
    values.

    Returns:
        Tuple containing git username and email.

    """
    log.debug("Try read git user information.")
    defaults = ("John Doe", "example@email.com")

    if not shutil.which("git"):
        return defaults

    try:
        author = (
            subprocess.check_output(["git", "config", "--get", "user.name"])
            .decode("utf-8")
            .strip()
        )
    except subprocess.CalledProcessError:
        author = defaults[0]

    try:
        email = (
            subprocess.check_output(["git", "config", "--get", "user.email"])
            .decode("utf-8")
            .strip()
        )
    except subprocess.CalledProcessError:
        email = defaults[1]

    return author, email


def run_shell(
    cmd: List[str],
    cwd: Optional[str] = None,
    check: bool = False,
    stdout: Optional[Union[int, IO[AnyStr]]] = None,
    stderr: Optional[Union[int, IO[AnyStr]]] = None,
    input: Optional[Union[str, bytes]] = None,
    capture_output: bool = False,
) -> "subprocess.CompletedProcess[Any]":
    """Run shell command without activated virtualenv.

    If virtual env is activated, remove it from PATH in order to ensure command proper
    execution. For more information, see issue:
    https://github.com/fastapi-mvc/fastapi-mvc/issues/37

    Args:
        cmd (list): Shell command to run.
        cwd (str): Path under which process should execute command. Defaults
            to current working directory.
        check (bool): If True raise a subprocess.CalledProcessError error
            when a process returns non-zero exit status.
        stdout (typing.Optional[typing.Union[int, IO[typing.AnyStr]]]): Specify the
            executed program’s standard output file handles.
        stderr (typing.Optional[typing.Union[int, IO[typing.AnyStr]])): Specify the
            executed program’s standard error file handles.
        input (typing.Optional[typing.Union[bytes, str]])): If given the input argument
            is passed to the subprocess’s stdin.
        capture_output (bool): If True, stdout and stderr will be captured.

    Returns:
        CompletedProcess: Class object instance.

    Raises:
        subprocess.CalledProcessError: If spawned proces finishes with an
            error and check is True.

    """
    if not cwd:
        cwd = os.getcwd()

    log.debug(f"Run shell command: {cmd} under path: {cwd}")
    env = os.environ.copy()

    if "VIRTUAL_ENV" in env:
        log.warning("Activated virtual env detected.")

        venv_path = f"{env['VIRTUAL_ENV']}/bin"
        del env["VIRTUAL_ENV"]

        env["PATH"] = env["PATH"].replace(venv_path, "").strip(":")

    try:
        process = subprocess.run(
            cmd,
            cwd=cwd,
            env=env,
            check=check,
            stdout=stdout,
            stderr=stderr,
            input=input,
            capture_output=capture_output,
        )
        return process
    except subprocess.CalledProcessError as ex:
        log.debug(ex)
        raise ex
