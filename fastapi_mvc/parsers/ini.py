"""FastAPI MVC ini parser implementation."""
import os
import logging
import configparser

from fastapi_mvc.exceptions import IniParserError


class IniParser(object):
    """Project fastapi-mvc.ini file parser class definition."""

    def __init__(self, project_path):
        """Initialize IniParser class object instance.

        Args:
            project_path(str): A fastapi-mvc project path.

        Raises:
             IniParserError: If fastapi-mvc.ini does not exist or not readable.

        """
        self._log = logging.getLogger(self.__class__.__name__)
        self._log.debug("Initialize fastapi-mvc.ini parser.")
        self._project_path = project_path
        self._ini_file = os.path.join(self._project_path, "fastapi-mvc.ini")

        if not os.path.exists(self._ini_file):
            self._log.error(
                "Not a fastapi-mvc project, fastapi-mvc.ini does not exist."
            )
            raise IniParserError(
                "Not a fastapi-mvc project, fastapi-mvc.ini does not exist."
            )
        elif not os.path.isfile(self._ini_file):
            self._log.error(
                "Not a fastapi-mvc project, fastapi-mvc.ini is not a file."
            )
            raise IniParserError(
                "Not a fastapi-mvc project, fastapi-mvc.ini is not a file."
            )
        elif not os.access(self._ini_file, os.R_OK):
            self._log.error("File fastapi-mvc.ini is not readable.")
            raise IniParserError("File fastapi-mvc.ini is not readable.")

        self._log.debug("Begin parsing: {0:s}".format(self._ini_file))
        self._config = configparser.ConfigParser()
        self._config.read(self._ini_file)

    @property
    def folder_name(self):
        """Class folder name property.

        Returns:
            Folder name value read from a fastapi-mvc.ini file.

        """
        return self._config["project"]["folder_name"]

    @property
    def package_name(self):
        """Class package name property.

        Returns:
            Package name value read from a fastapi-mvc.ini file.

        """
        return self._config["project"]["package_name"]

    @property
    def script_name(self):
        """Class script name property.

        Returns:
            Script name value read from a fastapi-mvc.ini file.

        """
        return self._config["project"]["script_name"]

    @property
    def redis(self):
        """Class Redis property.

        Returns:
            Redis value read from a fastapi-mvc.ini file.

        """
        return self._config["project"]["redis"]

    @property
    def github_actions(self):
        """Class GitHub actions property.

        Returns:
            GitHub actions value read from a fastapi-mvc.ini file.

        """
        return self._config["project"]["github_actions"]

    @property
    def aiohttp(self):
        """Class Aiohttp property.

        Returns:
            Aiohttp value read from a fastapi-mvc.ini file.

        """
        return self._config["project"]["aiohttp"]

    @property
    def vagrantfile(self):
        """Class Vagrantfile property.

        Returns:
            Vagrantfile value read from a fastapi-mvc.ini file.

        """
        return self._config["project"]["vagrantfile"]

    @property
    def helm(self):
        """Class Helm property.

        Returns:
            Helm value read from a fastapi-mvc.ini file.

        """
        return self._config["project"]["helm"]

    @property
    def version(self):
        """Class fastapi-mvc version property.

        Returns:
            Fastapi-mvc version value read from a fastapi-mvc.ini file.

        """
        return self._config["fastapi-mvc"]["version"]
