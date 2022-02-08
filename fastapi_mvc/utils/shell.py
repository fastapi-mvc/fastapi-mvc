"""FastAPI MVC shell utilities implementation."""
import os
import logging
import subprocess


class ShellUtils(object):
    """Shell utilities class definition.

    Attributes:
        _log(logging.Logger): Logger class object instance.

    """

    _log = logging.getLogger(__name__)

    @classmethod
    def get_git_user_info(cls):
        """Get git user information.

        Reads username and email information from git. If not exists, provide
        defaults values.

        Returns:
            Tuple containing git username and email.

        """
        cls._log.info("Try read git user information.")

        try:
            author = subprocess.check_output(
                ["git", "config", "--get", "user.name"]
            )
            author = author.decode("utf-8").strip()
        except subprocess.CalledProcessError:
            author = "John Doe"

        try:
            email = subprocess.check_output(
                ["git", "config", "--get", "user.email"]
            )
            email = email.decode("utf-8").strip()
        except subprocess.CalledProcessError:
            email = "example@email.com"

        return author, email

    @classmethod
    def run_project_install(cls, project_path):
        """Run make install at provided project path.

        If virtual env is activated, remove it from PATH in order to ensure make
        install proper execution. For more information, see issue:
        https://github.com/rszamszur/fastapi-mvc/issues/37

        Args:
            project_path(str): Project path in which execute make install.

        Raises:
            subprocess.CalledProcessError: If spawned proces finishes with an
                error.

        """
        cls._log.info(
            "Run make install for project: {0:s}".format(project_path)
        )
        env = os.environ.copy()

        if "VIRTUAL_ENV" in env:
            cls._log.info("Activated virtual env detected.")

            venv_path = "{venv}/bin".format(venv=env["VIRTUAL_ENV"])
            del env["VIRTUAL_ENV"]

            env["PATH"] = env["PATH"].replace(venv_path, "").strip(":")

        try:
            subprocess.run(["make", "install"], cwd=project_path, env=env)
        except subprocess.CalledProcessError as ex:
            cls._log.exception(
                "Proces finished with an exception.",
                exc_info=(type(ex), ex, ex.__traceback__),
            )
            raise ex
