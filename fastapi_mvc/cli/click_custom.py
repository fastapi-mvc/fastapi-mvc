"""Custom Click implementations."""
from collections import defaultdict

import click


class GeneratorCommand(click.Command):
    """Defines CLI command based on concrete Generator class.

    Args:
        generator_cls (Generator): Concrete Generator class associated with this
            CLI command.
        callback (typing.Callable[[...], typing.Any]): The callback to invoke.

    Attributes:
        generator_cls (Generator): Concrete Generator class associated with this
            CLI command.

    Resources:
        1. `click.Command class documentation`_

    .. _click.Command class documentation:
        https://click.palletsprojects.com/en/8.1.x/api/#click.Command

    """

    def __init__(self, generator_cls, callback):
        """Initialize GeneratorCommand class object instance."""
        super().__init__(
            name=generator_cls.name,
            params=[
                *generator_cls.cli_arguments,
                *generator_cls.cli_options,
            ],
            epilog=generator_cls.read_usage(),
            help=generator_cls.cli_help,
            short_help=generator_cls.cli_short_help,
            deprecated=generator_cls.cli_deprecated,
            callback=callback,
        )
        self.generator_cls = generator_cls

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

    def __init__(self, generators, command_callback, *args, **kwargs):
        """Initialize GeneratorsMultiCommand class object instance."""
        super().__init__(*args, **kwargs)
        self.generators = generators
        self.command_callback = command_callback

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

                category = getattr(cmd.generator_cls, "category", "Other")
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
            ctx.fail("No such generator '{gen}'.".format(gen=name))

        return GeneratorCommand(
            generator_cls=self.generators[name],
            callback=self.command_callback,
        )
