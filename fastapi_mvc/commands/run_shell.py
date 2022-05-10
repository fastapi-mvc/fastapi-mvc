"""Command design pattern - run shell command."""
from fastapi_mvc.commands import Command
from fastapi_mvc.utils import ShellUtils


class RunShell(Command):
    """Define the common interface for ShellUtils.run_shell method.

    Args:
        cmd (list): Shell command to run.
        cwd (str): Path under which process should execute command. Defaults
            to current working directory.
        check (bool): If True raise a subprocess.CalledProcessError error when
            a process returns non-zero exit status.
        stdout (Union[None, int, IO[Any]]): Specify the executed program’s
            standard output file handles.
        stderr (Union[None, int, IO[Any]]): Specify the executed program’s
            standard error file handles.

    Attributes:
        _cmd (list): Shell command to run.
        _cwd (str): Path under which process should execute command. Defaults
            to current working directory.
        _check (bool): If True raise a subprocess.CalledProcessError error when
            a process returns non-zero exit status.
        _stdout (Union[None, int, IO[Any]]): Specify the executed program’s
            standard output file handles.
        _stderr (Union[None, int, IO[Any]]): Specify the executed program’s
            standard error file handles.

    """

    __slots__ = (
        "_cmd",
        "_cwd",
        "_check",
        "_stdout",
        "_stderr",
    )

    def __init__(self, cmd, cwd=None, check=False, stdout=None, stderr=None):
        """Initialize RunShell class object instance."""
        Command.__init__(self)
        self._log.debug("Initialize RunShell class object instance.")
        self._cmd = cmd
        self._cwd = cwd
        self._check = check
        self._stdout = stdout
        self._stderr = stderr

    def execute(self):
        """Execute RunShell command."""
        self._log.info("Executing shell command: {cmd}".format(cmd=self._cmd))
        ShellUtils.run_shell(
            cmd=self._cmd,
            cwd=self._cwd,
            check=self._check,
            stdout=self._stdout,
            stderr=self._stderr,
        )
