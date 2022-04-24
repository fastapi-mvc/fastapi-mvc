"""FastAPI MVC CLI generate command implementation."""
import os
from collections import defaultdict

import click
from fastapi_mvc import Borg
from fastapi_mvc.commands import Generate


class GeneratorCommand(click.Command):
    """Custom click.Command class implementation.

    Base class (click.Command) documentation:
    https://click.palletsprojects.com/en/8.0.x/api/#click.Command

    """

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

    def invoke(self, ctx):
        """Invoke generate command with attached generator in callback.

        Args:
            ctx (click.Context): Context class object instance.

        """
        borg = Borg()
        generator = self.callback(parser=borg.parser)

        Generate(
            generator=generator,
            options=ctx.params,
        ).execute()


class DynamicMultiCommand(click.MultiCommand):
    """Custom click.MultiCommand class implementation.

    Base class (click.MultiCommand) documentation:
    https://click.palletsprojects.com/en/8.0.x/api/#click.MultiCommand

    Args:
        *args (list): Base class constructor args.
        **kwargs (dict): Base class constructor kwargs.

    Attributes:
        _generators (dict[str, Generator]): Dictionary containing all available
            fastapi-mvc generator classes.
        _parser (IniParser): IniParser class object instance.

    """

    def __init__(self, *args, **kwargs):
        """Initialize DynamicMultiCommand class object instance."""
        super().__init__(*args, **kwargs)
        self._generators = None

    @property
    def generators(self):
        """Load fastapi-mvc project and generators.

        Returns:
            typing.Dict[str, Generator]: Dictionary containing loaded
                fastapi-mvc generator classes.

        """
        if not self._generators:
            borg = Borg()
            borg.load_generators()
            self._generators = borg.generators

        return self._generators

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

                category = getattr(cmd.callback, "category", "Other")
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
        """Return GeneratorCommand object instance.

        Given a context and a command name, this returns a GeneratorCommand
        object instance if it exists or aborts the execution of the program.

        Args:
            ctx (click.Context): Click Context class object instance.
            name (str): Chosen generator name.

        Returns:
            GeneratorCommand: GeneratorCommand object instance for concrete
                generator name.

        """
        params = []
        epilog = None

        if name not in self.generators:
            ctx.fail("No such generator '{gen}'.".format(gen=name))

        generator = self.generators[name]

        for arg in generator.cli_arguments:
            params.append(click.Argument(**arg))

        for opt in generator.cli_options:
            params.append(click.Option(**opt))

        if os.path.isfile(generator.usage):
            with open(generator.usage, "r") as f:
                epilog = f.read()

        return GeneratorCommand(
            name,
            params=params,
            callback=generator,
            epilog=epilog,
        )


@click.command(
    cls=DynamicMultiCommand,
    subcommand_metavar="GENERATOR [ARGS]...",
)
def generate():
    """Run chosen fastapi-mvc generator.

    The 'fastapi-mvc generate' commands runs a generator of your choice for a
    fastapi-mvc project at the current working directory.
    \f

    """
    pass
