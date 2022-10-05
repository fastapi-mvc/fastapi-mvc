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
        template (str): **(class variable)** A URL to a git repository
            containing fastapi-mvc project template.
        usage (typing.Optional[str]): **(class variable)** Path to generator
            usage file, that will be printed at the end of its CLI command help
            page.
        category (str): **(class variable)** Name under which generator should
            be printed in ``fastapi-mvc generate`` CLI command help page.
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
    template = "https://github.com/fastapi-mvc/cookiecutter.git"
    template_version = "0.3.0"
    usage = os.path.abspath(
        os.path.join(
            os.path.abspath(__file__),
            "../USAGE",
        )
    )
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
            param_decls=["-I", "--skip-install"],
            help="Do not run make install.",
            is_flag=True,
        ),
        click.Option(
            param_decls=["-N", "--skip-nix"],
            help="Skip nix expression files.",
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
            help="New project repository url.",
            type=click.STRING,
            envvar="REPO_URL",
            default="https://your.repo.url.here",
        ),
        click.Option(
            param_decls=["--template-version"],
            help="The branch, tag or commit ID to checkout after clone.",
            type=click.STRING,
            default=template_version,
            show_default=True,
        ),
        click.Option(
            param_decls=["--override-template"],
            help="Overrides fastapi-mvc cookiecutter template repository.",
            type=click.STRING,
        ),
    ]
    cli_short_help = "Create a new FastAPI application."
    cli_help = """\
    The 'fastapi-mvc new' command creates a new FastAPI application with a
    default directory structure and configuration at the path you specify.

    Default Project template used: https://github.com/fastapi-mvc/cookiecutter

    """

    @staticmethod
    def _get_value(value):
        """Parse boolean value to yes/no string for cookiecutter context.

        Args:
            value (bool): Given value.

        Returns:
            str: Parsed value.

        """
        if value:
            return "no"
        else:
            return "yes"

    def new(
        self,
        app_path,
        skip_redis,
        skip_aiohttp,
        skip_actions,
        skip_helm,
        skip_install,
        skip_nix,
        license,
        repo_url,
        template_version,
        override_template,
    ):
        """Generate a new fastapi-mvc project.

        Args:
            app_path (str): Given new project path.
            skip_redis (bool): If true skip Redis files.
            skip_aiohttp (bool): If true skip aiohttp utility files.
            skip_actions (bool): If true skip GitHub actions files.
            skip_helm (bool): If true skip Helm chart files.
            skip_install (bool): If true skip ``make install`` once project is
                generated.
            skip_nix (bool): If true skip nix expression files.
            license (str): Project license.
            repo_url (str): Project repository url.
            template_version (str): Project template version - the branch, tag
                or commit ID to checkout after clone.
            override_template (str): Overrides fastapi-mvc cookiecutter template
                repository.

        """
        if override_template:
            self._log.info(
                f"Using custom project template repository: {override_template}"
            )
            template = override_template
        else:
            template = self.template

        self._log.info(f"Creating a new fastapi-mvc project: {app_path}")
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
            "helm": self._get_value(skip_helm),
            "nix": self._get_value(skip_nix),
            "author": author,
            "email": email,
            "license": license,
            "repo_url": repo_url,
            "year": datetime.today().year,
            "fastapi_mvc_version": __version__,
        }

        self._log.debug(f"Cookiecutter context: {context}")

        try:
            cookiecutter(
                template,
                checkout=template_version,
                extra_context=context,
                no_input=True,
                output_dir=output_dir,
            )
        except OutputDirExistsException as ex:
            self._log.error(ex)
            raise SystemExit(1)

        if not skip_install:
            self._log.info("Executing shell command:  ['make', 'install']")
            ShellUtils.run_shell(cmd=["make", "install"], cwd=app_path)

    def destroy(self, **kwargs):
        """Not yet implemented.

        Args:
            **kwargs(dict): Abstract methods kwargs.

        """
        raise NotImplementedError
