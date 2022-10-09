"""Fastapi-mvc utilities - shell.

Attributes:
    log (logging.Logger): Logger class object instance.

"""
import os
import logging
import subprocess
import shutil


log = logging.getLogger(__name__)


def get_git_user_info():
    """Get git user information.

    Reads username and email information from git. If not exists, provide defaults
    values.

    Returns:
        typing.Tuple[str, str]: Tuple containing git username and email.

    """
    log.debug("Try read git user information.")
    defaults = ("John Doe", "example@email.com")

    if not shutil.which("git"):
        return defaults

    try:
        author = subprocess.check_output(["git", "config", "--get", "user.name"])
        author = author.decode("utf-8").strip()
    except subprocess.CalledProcessError:
        author = defaults[0]

    try:
        email = subprocess.check_output(["git", "config", "--get", "user.email"])
        email = email.decode("utf-8").strip()
    except subprocess.CalledProcessError:
        email = defaults[1]

    return author, email


def run_shell(cmd, cwd=None, check=False, stdout=None, stderr=None):
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
        stdout (typing.Union[None, int, typing.IO[typing.Any]]): Specify the
            executed program’s standard output file handles.
        stderr (typing.Union[None, int, typing.IO[typing.Any]]): Specify the
            executed program’s standard error file handles.

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
        )
        return process
    except subprocess.CalledProcessError as ex:
        log.debug(ex)
        raise ex
