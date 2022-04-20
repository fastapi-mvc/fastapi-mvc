"""FastAPI MVC CLI generate command implementation."""
import os

import click
from fastapi_mvc import Borg
from fastapi_mvc.commands import Generate


class GeneratorCommand(click.Command):

    def format_epilog(self, ctx, formatter):
        """Writes the epilog into the formatter if it exists.

        Args:
            ctx(click.Context): Click Context class object instance.
            formatter(click.HelpFormatter): Click HelpFormatter class object
                instance.

        """
        if self.epilog:
            formatter.write_paragraph()
            formatter.write(self.epilog)

    def invoke(self, ctx):
        """Given a context, this invokes the attached callback (if it exists)
        in the right way.
        """
        Generate(
            generator=self.callback,
            options=ctx.params,
        ).execute()


class DynamicMultiCommand(click.MultiCommand):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._generators = None
        self._parser = None

    @property
    def generators(self):
        if not self._generators:
            borg = Borg()
            borg.load_generators()
            self._generators = borg.generators
            self._parser = borg.parser

        return self._generators

    def format_commands(self, ctx, formatter):
        """Writes all the generators into the formatter if they exist.

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
            # What is this, the tool lied about a command.  Ignore it
            if cmd is None:
                continue
            if cmd.hidden:
                continue

            commands.append((subcommand, cmd))

        # allow for 3 times the default spacing
        if len(commands):
            limit = formatter.width - 6 - max(len(cmd[0]) for cmd in commands)

            rows = []
            for subcommand, cmd in commands:
                help = cmd.get_short_help_str(limit)
                rows.append((subcommand, help))

            if rows:
                with formatter.section("Generators"):
                    formatter.write_dl(rows)

    def list_commands(self, ctx):
        """Returns a list of subcommand names in the order they should appear.

        Args:
            ctx (click.Context): Click Context class object instance.

        Returns:
            list: List of subcommand names in the order they should appear.

        """
        return self.generators.keys()

    def get_command(self, ctx, name):
        """Returns GeneratorCommand object instance.

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
            callback=generator(self._parser),
            epilog=epilog,
        )


@click.command(
    cls=DynamicMultiCommand,
    subcommand_metavar="GENERATOR [ARGS]...",
)
def generate():
    pass
