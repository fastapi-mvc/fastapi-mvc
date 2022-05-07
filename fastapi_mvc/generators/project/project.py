"""Fastapi-mvc generators - project generator."""
import os
from datetime import datetime

import click
from cookiecutter.main import cookiecutter
from cookiecutter.exceptions import OutputDirExistsException
from fastapi_mvc.utils import ShellUtils
from fastapi_mvc.generators import Generator
from fastapi_mvc.version import __version__


class ProjectGenerator(Generator):
    """Define project generator.

    Attributes:
        name (str): **(class variable)** A distinguishable generator name, that
            will be used as subcommand for ``fastapi-mvc generate`` CLI command.
        template (str): **(class variable)**  Path to generator cookiecutter
            template root directory.
        usage (typing.Optional[str]): **(class variable)** Path to generator
            usage file, that will be printed at the end of its CLI command help
            page.
        category (str): (class variable) Name under which generator should be
            printed in ``fastapi-mvc generate`` CLI command help page.
        cli_arguments (typing.List[click.Argument]): **(class variable)** Click
            arguments to register with this generator CLI command.
        cli_options (typing.List[click.Option]): **(class variable)** Click
            options to register with this generator CLI command.
        cli_help (typing.Optional[str]): **(class variable)** The help string to
            use for this generator CLI command.
        cli_short_help (typing.Optional[str]): **(class variable)** The short
            help to use for this generator CLI command. This is shown on the
            command listing of ``fastapi-mvc generate`` command.

    """

    name = "new"
    template = os.path.abspath(
        os.path.join(
            os.path.abspath(__file__),
            "../template",
        )
    )
    usage = None
    category = "Project"
    cli_arguments = [
        click.Argument(
            param_decls=["APP_PATH"],
            nargs=1,
            type=click.Path(exists=False),
            required=True,
        ),
    ]
    cli_options = [
        click.Option(
            param_decls=["-R", "--skip-redis"],
            help="Skip Redis utility files.",
            is_flag=True,
        ),
        click.Option(
            param_decls=["-A", "--skip-aiohttp"],
            help="Skip aiohttp utility files.",
            is_flag=True,
        ),
        click.Option(
            param_decls=["-V", "--skip-vagrantfile"],
            help="Skip Vagrantfile.",
            is_flag=True,
        ),
        click.Option(
            param_decls=["-H", "--skip-helm"],
            help="Skip Helm chart files.",
            is_flag=True,
        ),
        click.Option(
            param_decls=["-G", "--skip-actions"],
            help="Skip GitHub actions files.",
            is_flag=True,
        ),
        click.Option(
            param_decls=["-C", "--skip-codecov"],
            help="Skip codecov in GitHub actions.",
            is_flag=True,
        ),
        click.Option(
            param_decls=["-I", "--skip-install"],
            help="Do not run make install.",
            is_flag=True,
        ),
        click.Option(
            param_decls=["--license"],
            help="Choose license.",
            type=click.Choice(
                [
                    "MIT",
                    "BSD2",
                    "BSD3",
                    "ISC",
                    "Apache2.0",
                    "LGPLv3+",
                    "LGPLv3",
                    "LGPLv2+",
                    "LGPLv2",
                    "no",
                ]
            ),
            default="MIT",
            show_default=True,
            envvar="LICENSE",
        ),
        click.Option(
            param_decls=["--repo-url"],
            help="Repository url.",
            type=click.STRING,
            envvar="REPO_URL",
            default="https://your.repo.url.here",
        )
    ]
    cli_short_help = "Create a new FastAPI application."
    cli_help = """\
    The 'fastapi-mvc new' command creates a new FastAPI application with a
    default directory structure and configuration at the path you specify.
    """

    @staticmethod
    def _get_value(value):
        if value:
            return "no"
        else:
            return "yes"

    def new(self, app_path, skip_redis, skip_aiohttp, skip_actions,
            skip_vagrantfile, skip_helm, skip_install, skip_codecov, license,
            repo_url):
        app_name = os.path.basename(app_path)
        output_dir = os.path.dirname(app_path)

        if not output_dir:
            output_dir = "."

        author, email = ShellUtils.get_git_user_info()

        context = {
            "project_name": app_name,
            "redis": self._get_value(skip_redis),
            "aiohttp": self._get_value(skip_aiohttp),
            "github_actions": self._get_value(skip_actions),
            "vagrantfile": self._get_value(skip_vagrantfile),
            "helm": self._get_value(skip_helm),
            "codecov": self._get_value(skip_codecov),
            "author": author,
            "email": email,
            "license": license,
            "repo_url": repo_url,
            "year": datetime.today().year,
            "fastapi_mvc_version": __version__,
        }

        self._log.info(
            "Begin generating a new project at path: {0:s}".format(output_dir)
        )
        self._log.debug("Cookiecutter context: {0}".format(context))

        try:
            cookiecutter(
                self.template,
                extra_context=context,
                no_input=True,
                output_dir=output_dir,
            )
        except OutputDirExistsException as ex:
            self._log.error(ex)
            raise ex

        if not skip_install:
            ShellUtils.run_shell(cmd=["make", "install"], cwd=app_path)

    def destroy(self, **kwargs):
        """Not yet implemented.

        Args:
            **kwargs(dict): Abstract methods kwargs.

        """
        raise NotImplementedError
