"""FastAPI MVC generator generator implementation."""
import os
import sys

from cookiecutter.main import cookiecutter
from fastapi_mvc.generators import Generator


class GeneratorGenerator(Generator):

    __slots__ = "_builtins"

    name = "generator"
    template = os.path.abspath(
        os.path.join(
            os.path.abspath(__file__),
            "../template",
        )
    )
    usage = os.path.join(template, "USAGE")

    def __init__(self, parser, project_root):
        Generator.__init__(self, parser, project_root)
        self._builtins = ["controller", "generator"]

    def new(self, name, skip):
        if name in self._builtins:
            self._log.error("Shadows built-in generator: {0:s}".format(name))
            sys.exit(1)

        self._context["generator_name"] = name

        words = name.replace("-", " ").replace("_", " ").split()
        class_name = ''.join(w.capitalize() for w in words)

        self._context["class_name"] = "{0:s}Generator".format(
            class_name
        )

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
            overwrite_if_exists=True,
            skip_if_file_exists=skip,
        )

    def destroy(self, **kwargs):
        raise NotImplementedError
