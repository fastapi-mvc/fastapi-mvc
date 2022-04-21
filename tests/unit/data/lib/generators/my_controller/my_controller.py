"""FastAPI MVC my_controller generator implementation."""
import os

from cookiecutter.main import cookiecutter
from fastapi_mvc.generators import Generator


class MyControllerGenerator(Generator):

    name = "my_controller"
    template = os.path.abspath(
        os.path.join(
            os.path.abspath(__file__),
            "../template",
        )
    )
    category = "UnitTests"
    usage = os.path.join(template, "USAGE")

    def __init__(self, parser):
        Generator.__init__(self, parser)

    def new(self, name, skip):
        context = {
            "package_name": self._parser.package_name,
            "folder_name": self._parser.folder_name,
            "my_controller_name": name,
        }

        self._log.debug("Cookiecutter context: {0}".format(context))

        cookiecutter(
            self.__class__.template,
            extra_context=context,
            output_dir=os.path.abspath(
                os.path.join(
                    self._parser.project_root,
                    "../",
                )
            ),
            no_input=True,
            skip_if_file_exists=skip,
        )

    def destroy(self, **kwargs):
        raise NotImplementedError
