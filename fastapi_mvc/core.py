"""Fastapi-mvc core implementations.

Attributes:
    VERSION (str): Fastapi-mvc version.
    ANSWERS_FILE (str): Relative path to copier answers file.

Resources:
    1. `Click documentation`_
    2. `Copier documentation`_

.. _Click documentation:
    https://click.palletsprojects.com/en/8.1.x/

.. _Copier documentation:
    https://copier.readthedocs.io/en/v6.2.0

"""
import os
from collections import defaultdict

import click
import copier
from copier.tools import Style, printf
from copier.user_data import load_answersfile_data


# CONSTANTS
VERSION = "0.18.0"
ANSWERS_FILE = ".fastapi-mvc.yml"


class Command(click.Command):
    """Defines base class for all concrete fastapi-mvc CLI commands.

    Attributes:
        project_data (typing.Optional[typing.Dict[str, typing.Any]): Map of copier
            answers file questions to their parsed values.

    Resources:
        1. `click.Command class documentation`_

    .. _click.Command class documentation:
        https://click.palletsprojects.com/en/8.1.x/api/#click.Command

    """

    def __init__(self, *args, **kwargs):
        """Initialize Command class object instance."""
        super().__init__(*args, **kwargs)
        self.project_data = None

    @property
    def poetry_path(self):
        """Get Poetry binary abspath.

        Returns:
            str: Poetry binary abspath.

        """
        if os.getenv("POETRY_BINARY"):
            return os.getenv("POETRY_BINARY")

        poetry_home = os.getenv(
            "POETRY_HOME", f"{os.getenv('HOME')}/.local/share/pypoetry"
        )
        return f"{poetry_home}/venv/bin/poetry"

    def ensure_project_data(self):
        """Ensure necessary project data existence.

        Run ``copier.user_data.load_answersfile_data`` method, and ensure existence of
        required values.

        Raises:
            SystemExit: If project data is empty or is missing required values.

        """
        self.project_data = load_answersfile_data(
            dst_path=os.getcwd(),
            answers_file=ANSWERS_FILE,
        )

        if not self.project_data or "package_name" not in self.project_data:
            click.secho(
                "Not a fastapi-mvc project. Try 'fastapi-mvc new --help' for "
                "details how to create one.",
                fg="red",
                err=True,
            )
            raise SystemExit(1)


class Generator(Command):
    """Defines base class for all concrete fastapi-mvc generators.

    Args:
        template (str): Copier template source. Can be repository URL or local path.
        vcs_ref (typing.Optional[str]): The branch, tag or commit ID to checkout after
            clone. Provided template is a repostiory URL.
        category (str): Name under which generator should be printed in
            ``fastapi-mvc generate`` CLI command help page.

    Attributes:
        template (str): Copier template source. Can be repository URL or local path.
        vcs_ref (typing.Optional[str]): The branch, tag or commit ID to checkout after
            clone. Provided template is a repostiory URL.
        category (str): Name under which generator should be printed in
            ``fastapi-mvc generate`` CLI command help page.

    Resources:
        1. `click.Command class documentation`_

    .. _click.Command class documentation:
        https://click.palletsprojects.com/en/8.1.x/api/#click.Command

    """

    def __init__(self, template, vcs_ref=None, category="Other", *args, **kwargs):
        """Initialize Generator class object instance."""
        super().__init__(*args, **kwargs)
        self.template = template
        self.vcs_ref = vcs_ref
        self.category = category

    def format_epilog(self, ctx, formatter):
        """Write the epilog into the formatter if it exists.

        Args:
            ctx (click.Context): Click Context class object instance.
            formatter (click.HelpFormatter): Click HelpFormatter class object instance.

        """
        if self.epilog:
            formatter.write_paragraph()
            formatter.write(self.epilog)

    def copier_printf(self, action, msg="", style=None, **kwargs):
        """Define wrapper for ``copier.printf`` method.

        Args:
            action (str): Given action value, ex: run, create, etc.
            msg (str): Given messsage to print.
            style (copier.tools.Style): Style to color action with.

        """
        if style:
            style = getattr(Style, style)

        printf(
            action=action,
            msg=msg,
            style=style,
            **kwargs,
        )

    def run_auto(self, dst_path=".", data=None, answers_file=ANSWERS_FILE, **kwargs):
        """Define wrapper for ``copier.run_auto`` method.

        Args:
            dst_path (str | pathlib.Path): Destination path where to render the project.
            data (typing.Optional[typing.Dict[str, typing.Any]): Answers to the
                questionary defined in the template.
            answers_file (str): Indicates the path for the answers file. The path must
                be relative to dst_path.

        """
        copier.run_auto(
            src_path=self.template,
            dst_path=dst_path,
            vcs_ref=self.vcs_ref,
            answers_file=answers_file,
            data=data,
            **kwargs,
        )

    def run_copy(self, dst_path=".", data=None, answers_file=ANSWERS_FILE, **kwargs):
        """Define wrapper for ``copier.run_copy`` method.

        Args:
            dst_path (str | pathlib.Path): Destination path where to render the project.
            data (typing.Optional[typing.Dict[str, typing.Any]): Answers to the
                questionary defined in the template.
            answers_file (str): Indicates the path for the answers file. The path must
                be relative to dst_path.

        """
        copier.run_copy(
            src_path=self.template,
            dst_path=dst_path,
            vcs_ref=self.vcs_ref,
            answers_file=answers_file,
            data=data,
            **kwargs,
        )

    def run_update(self, dst_path=".", data=None, answers_file=ANSWERS_FILE, **kwargs):
        """Define wrapper for ``copier.run_update`` method.

        Args:
            dst_path (str | pathlib.Path): Destination path where to render the project.
            data (typing.Optional[typing.Dict[str, typing.Any]): Answers to the
                questionary defined in the template.
            answers_file (str): Indicates the path for the answers file. The path must
                be relative to dst_path.

        """
        copier.run_update(
            dst_path=dst_path,
            vcs_ref=self.vcs_ref,
            answers_file=answers_file,
            data=data,
            **kwargs,
        )

    def insert_router_import(self, controller_name):
        """Insert import and router entry into ``app/router.py`` file.

        Args:
            controller_name (str): Given controller name.

        """
        package_name = self.project_data["package_name"]
        router = os.path.join(os.getcwd(), f"{package_name}/app/router.py")
        import_str = f"from {package_name}.app.controllers import {controller_name}\n"

        with open(router, "r") as f:
            lines = f.readlines()

        if import_str in lines:
            return

        for i in range(len(lines)):
            if lines[i].strip() == "from fastapi import APIRouter":
                index = i + 1
                break
        else:
            index = 0

        lines.insert(index, import_str)
        lines.append(f"root_api_router.include_router({controller_name}.router)\n")

        with open(router, "w") as f:
            f.writelines(lines)


class GeneratorsMultiCommand(click.MultiCommand):
    """Custom click.MultiCommand class implementation.

    Args:
        generators (typing.Dict[str, Generator]): Dictionary containing all available
            fastapi-mvc generators.
        *args (list): Parent class constructor args.
        **kwargs (dict): Parent class constructor kwargs.

    Attributes:
        generators (typing.Dict[str, Generator]): Dictionary containing all available
            fastapi-mvc generators.

    Resources:
        1. `click.MultiCommand class documentation`_

    .. _click.MultiCommand class documentation:
        https://click.palletsprojects.com/en/8.1.x/api/#click.MultiCommand

    """

    def __init__(self, generators, *args, **kwargs):
        """Initialize GeneratorsMultiCommand class object instance."""
        super().__init__(*args, **kwargs)
        self.generators = generators

    def format_commands(self, ctx, formatter):
        """Write all the generators into the formatter if they exist.

        Extra format methods for multi methods that adds all the generators after the
        options.

        Args:
            ctx (click.Context): Click Context class object instance.
            formatter (click.HelpFormatter): Click HelpFormatter class object instance.

        """
        commands = []
        for subcommand in self.list_commands(ctx):
            cmd = self.get_command(ctx, subcommand)
            commands.append((subcommand, cmd))

        if commands:
            limit = formatter.width - 6 - max(len(cmd[0]) for cmd in commands)

            rows = defaultdict(list)

            for subcommand, cmd in commands:
                help = cmd.get_short_help_str(limit)

                category = getattr(cmd, "category", "Other")
                rows[category].append((subcommand, help))

            formatter.write_paragraph()
            formatter.write("Please choose a generator below.")
            formatter.write_paragraph()

            with formatter.section("Builtins"):
                formatter.write_dl(rows.pop("Builtins"))

            for key, value in rows.items():
                with formatter.section(key):
                    formatter.write_dl(value)

    def list_commands(self, ctx):
        """Return a list of subcommand names in the order they should appear.

        Args:
            ctx (click.Context): Click Context class object instance.

        Returns:
            list: List of subcommand names in the order they should appear.

        """
        return self.generators.keys()

    def get_command(self, ctx, name):
        """Return GeneratorCommand class object instance.

        Given a context and a command name, this returns a ``GeneratorCommand`` class
        object instance if it exists or aborts the execution of the program.

        Args:
            ctx (click.Context): Click Context class object instance.
            name (str): Chosen generator name.

        Returns:
            Generator: Class object instance for given command name.

        """
        if name not in self.generators:
            ctx.fail(f"No such generator '{name}'.")

        return self.generators[name]
