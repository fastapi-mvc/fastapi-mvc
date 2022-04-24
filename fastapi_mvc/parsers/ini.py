"""FastAPI MVC ini parser implementation."""
import os
import logging
import configparser


class IniParser(object):
    """Project fastapi-mvc.ini file parser class definition.

    Attributes:
        _log (logging.Logger): Logger class object instance.
        _project_root (str): A fastapi-mvc project root path.
        _config (ConfigParser): Parserd fastapi-mvc.ini ConfigParser class
            object instance.

    Args:
        project_root (str): A fastapi-mvc project root path.

    Raises:
        FileNotFoundError: If fastapi-mvc.ini does not exist.
        IsADirectoryError: If fastapi-mvc.ini is a directory.
        PermissionError: If fastapi-mvc.ini is not readable.

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
        """Object instance project root path property.

        Returns:
            str: Path to project root from which `fastapi-mvc.ini` was parsed.

        """
        return self._project_root

    @property
    def folder_name(self):
        """Object instance folder name property.

        Returns:
            str: Folder name value read from a fastapi-mvc.ini file.

        """
        return self._config["project"]["folder_name"]

    @property
    def package_name(self):
        """Object instance package name property.

        Returns:
            str: Package name value read from a fastapi-mvc.ini file.

        """
        return self._config["project"]["package_name"]

    @property
    def script_name(self):
        """Object instance script name property.

        Returns:
            str: Script name value read from a fastapi-mvc.ini file.

        """
        return self._config["project"]["script_name"]

    @property
    def redis(self):
        """Object instance Redis property.

        Returns:
            str: Redis value read from a fastapi-mvc.ini file.

        """
        return self._config["project"]["redis"]

    @property
    def github_actions(self):
        """Object instance GitHub actions property.

        Returns:
            str: GitHub actions value read from a fastapi-mvc.ini file.

        """
        return self._config["project"]["github_actions"]

    @property
    def aiohttp(self):
        """Object instance Aiohttp property.

        Returns:
            str: Aiohttp value read from a fastapi-mvc.ini file.

        """
        return self._config["project"]["aiohttp"]

    @property
    def vagrantfile(self):
        """Object instance Vagrantfile property.

        Returns:
            str: Vagrantfile value read from a fastapi-mvc.ini file.

        """
        return self._config["project"]["vagrantfile"]

    @property
    def helm(self):
        """Object instance Helm property.

        Returns:
            str: Helm value read from a fastapi-mvc.ini file.

        """
        return self._config["project"]["helm"]

    @property
    def version(self):
        """Object instance fastapi-mvc version property.

        Returns:
            str: Fastapi-mvc version value read from a fastapi-mvc.ini file.

        """
        return self._config["fastapi-mvc"]["version"]
