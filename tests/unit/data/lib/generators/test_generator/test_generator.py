"""FastAPI MVC test_generator generator implementation."""
import os

from cookiecutter.main import cookiecutter
from fastapi_mvc.generators import Generator


class TestGeneratorGenerator(Generator):

    name = "test_generator"
    template = os.path.abspath(
        os.path.join(
            os.path.abspath(__file__),
            "../template",
        )
    )
    usage = os.path.join(template, "USAGE")

    def __init__(self, parser, project_root):
        Generator.__init__(self, parser, project_root)

    def new(self, name, skip):
        self._context["test_generator_name"] = name
        self._log.debug("Cookiecutter context: {0}".format(self._context))

        cookiecutter(
            self.__class__.template,
            extra_context=self._context,
            output_dir=os.path.abspath(
                os.path.join(
                    self._project_root,
                    "../",
                )
            ),
            no_input=True,
            skip_if_file_exists=skip,
        )

    def destroy(self, **kwargs):
        raise NotImplementedError
