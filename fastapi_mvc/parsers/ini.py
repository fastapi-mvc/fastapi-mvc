"""Fastapi-mvc parsers - ini parser."""
import os
import logging
import configparser


class IniParser(object):
    """Define ``fastapi-mvc.ini`` file parser.

    Attributes:
        _log (logging.Logger): Logger class object instance.
        _project_root (str): A fastapi-mvc project root path.
        _config (ConfigParser): Parserd ``fastapi-mvc.ini`` ConfigParser class
            object instance.

    Args:
        project_root (str): A fastapi-mvc project root path.

    Raises:
        FileNotFoundError: If ``fastapi-mvc.ini`` does not exist.
        IsADirectoryError: If ``fastapi-mvc.ini`` is a directory.
        PermissionError: If ``fastapi-mvc.ini`` is not readable.

    """

    __slots__ = (
        "_log",
        "_project_root",
        "_config",
    )

    def __init__(self, project_root=None):
        """Initialize IniParser class object instance."""
        self._log = logging.getLogger(self.__class__.__name__)
        self._log.debug("Initialize fastapi-mvc.ini parser.")

        if not project_root:
            self._project_root = os.getcwd()
        else:
            self._project_root = project_root

        ini_file = os.path.join(self._project_root, "fastapi-mvc.ini")
        self._log.debug("Begin parsing: {0:s}".format(ini_file))

        if not os.path.exists(ini_file):
            msg = "{0:s}/fastapi-mvc.ini does not exist.".format(
                self._project_root
            )
            self._log.debug(msg)
            raise FileNotFoundError(msg)
        elif not os.path.isfile(ini_file):
            msg = "{0:s}/fastapi-mvc.ini is not a file.".format(
                self._project_root
            )
            self._log.debug(msg)
            raise IsADirectoryError(msg)
        elif not os.access(ini_file, os.R_OK):
            msg = "{0:s}/fastapi-mvc.ini is not readable.".format(
                self._project_root
            )
            self._log.debug(msg)
            raise PermissionError(msg)

        self._config = configparser.ConfigParser()
        self._config.read(ini_file)

    @property
    def project_root(self):
        """Get project root path.

        Returns:
            str: Path to project root from which ``fastapi-mvc.ini`` was parsed.

        """
        return self._project_root

    @property
    def folder_name(self):
        """Get folder name.

        Returns:
            str: Folder name value read from a ``fastapi-mvc.ini`` file.

        """
        return self._config["project"]["folder_name"]

    @property
    def package_name(self):
        """Get package name.

        Returns:
            str: Package name value read from a ``fastapi-mvc.ini`` file.

        """
        return self._config["project"]["package_name"]

    @property
    def script_name(self):
        """Get script name.

        Returns:
            str: Script name value read from a ``fastapi-mvc.ini`` file.

        """
        return self._config["project"]["script_name"]

    @property
    def redis(self):
        """Get Redis value.

        Returns:
            str: Redis value read from a ``fastapi-mvc.ini`` file.

        """
        return self._config["project"]["redis"]

    @property
    def github_actions(self):
        """Get GitHub actions value.

        Returns:
            str: GitHub actions value read from a ``fastapi-mvc.ini`` file.

        """
        return self._config["project"]["github_actions"]

    @property
    def helm(self):
        """Get Helm value.

        Returns:
            str: Helm value read from a ``fastapi-mvc.ini`` file.

        """
        return self._config["project"]["helm"]

    @property
    def chart_name(self):
        """Get Helm chart name.

        Returns:
            str: Chart name value read from a ``fastapi-mvc.ini`` file.

        """
        return self._config["project"]["chart_name"]

    @property
    def version(self):
        """Get fastapi-mvc version.

        Returns:
            str: Fastapi-mvc version value read from a ``fastapi-mvc.ini`` file.

        """
        return self._config["fastapi-mvc"]["version"]
