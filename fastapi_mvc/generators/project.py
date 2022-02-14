"""FastAPI MVC new project generator implementation."""
import os
import logging

from cookiecutter.main import cookiecutter
from cookiecutter.exceptions import OutputDirExistsException


class ProjectGenerator(object):
    """Project generator class definition."""

    def __init__(self):
        """Initialize ProjectGenerator class object instance."""
        self._log = logging.getLogger(self.__class__.__name__)
        self._log.debug("Initialize fastapi-mvc project generator.")
        self._template_dir = os.path.abspath(
            os.path.join(
                os.path.abspath(__file__),
                "../../template",
            )
        )

    def new(self, context, output_dir):
        """Generate a new fastapi-mvc project from cookiecutter template.

        Args:
            context(dict): Cookiecutter template context dictionary.
            output_dir(str): Directory in which the project is to be created.

        Raises:
            OutputDirExistsException: If provided output directory already
                exists.

        """
        self._log.debug(
            "Begin generating a new project at path: {0:s}".format(output_dir)
        )
        self._log.debug("Cookiecutter context: {0}".format(context))

        try:
            cookiecutter(
                self._template_dir,
                extra_context=context,
                no_input=True,
                output_dir=output_dir,
            )
        except OutputDirExistsException as ex:
            self._log.error(ex)
            raise ex
