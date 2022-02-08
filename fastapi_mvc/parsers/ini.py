"""FastAPI MVC ini parser implementation."""
import os
import logging
import configparser


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
        self._log.info("Initialize fastapi-mvc.ini parser.")
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

        self._log.info("Begin parsing: {0:s}".format(self._ini_file))
        self._config = configparser.ConfigParser()
        self._config.read(self._ini_file)

    @property
    def package_name(self):
        """Package name property.

        Returns:
            Package name read from a fastapi-mvc.ini file.

        """
        return self._config["project"]["package_name"]


class IniParserError(Exception):
    """Custom IniParser exception class definition."""

    pass
