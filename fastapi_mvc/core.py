import os
from collections import defaultdict

import click
import copier
from copier.tools import Style, printf
from copier.user_data import load_answersfile_data


# CONSTANTS
VERSION = "0.17.0"
ANSWERS_FILE = ".fastapi-mvc.yml"


class Command(click.Command):
    def __init__(self, *args, **kwargs):
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
    def __init__(self, template, vcs_ref=None, category="Other", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.template = template
        self.vcs_ref = vcs_ref
        self.category = category

    def format_epilog(self, ctx, formatter):
        """Write the epilog into the formatter if it exists.
        Args:
            ctx (click.Context): Click Context class object instance.
            formatter (click.HelpFormatter): Click HelpFormatter class object
                instance.
        """
        if self.epilog:
            formatter.write_paragraph()
            formatter.write(self.epilog)

    def copier_printf(self, action, msg="", style=None, **kwargs):
        if style:
            style = getattr(Style, style)

        printf(
            action=action,
            msg=msg,
            style=style,
            **kwargs,
        )

    def run_auto(self, dst_path=".", data=None, **kwargs):
        copier.run_auto(
            src_path=self.template,
            dst_path=dst_path,
            vcs_ref=self.vcs_ref,
            answers_file=ANSWERS_FILE,
            data=data,
            **kwargs,
        )

    def run_copy(self, dst_path=".", data=None, **kwargs):
        copier.run_copy(
            src_path=self.template,
            dst_path=dst_path,
            vcs_ref=self.vcs_ref,
            answers_file=ANSWERS_FILE,
            data=data,
            **kwargs,
        )

    def run_update(self, dst_path=".", data=None, **kwargs):
        copier.run_update(
            dst_path=dst_path,
            vcs_ref=self.vcs_ref,
            answers_file=ANSWERS_FILE,
            data=data,
            **kwargs,
        )

    def insert_router_import(self, controller_name):
        """Add import and router entry to config/router.rb if not skipped."""
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
        generators (typing.Dict[str, Generator]): Dictionary containing all
            available fastapi-mvc generators.
        command_callback (typing.Callable[[...], typing.Any]): The callback to
            invoke by the GeneratorCommand.
        *args (list): Parent class constructor args.
        **kwargs (dict): Parent class constructor kwargs.

    Attributes:
        generators (typing.Dict[str, Generator]): Dictionary containing all
            available fastapi-mvc generators.
        command_callback (typing.Callable[[...], typing.Any]): The callback to
            invoke by the GeneratorCommand.

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

        Extra format methods for multi methods that adds all the generators
        after the options.

        Args:
            ctx (click.Context): Click Context class object instance.
            formatter (click.HelpFormatter): Click HelpFormatter class object
                instance.

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

        Given a context and a command name, this returns a ``GeneratorCommand``
        class object instance if it exists or aborts the execution of the
        program.

        Args:
            ctx (click.Context): Click Context class object instance.
            name (str): Chosen generator name.

        Returns:
            GeneratorCommand: Class object instance for given command
                name.

        """
        if name not in self.generators:
            ctx.fail(f"No such generator '{name}'.")

        return self.generators[name]
