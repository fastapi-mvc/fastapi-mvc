"""Command-line interface - core implementations.

Resources:
    1. `Click documentation`_

.. _Click documentation:
    https://click.palletsprojects.com/en/8.1.x/

"""
from typing import Dict, Any, List
from collections import defaultdict

import click


class ClickAliasedCommand(click.Command):
    """Defines base class for all concrete fastapi-mvc CLI commands.

    Args:
        alias (str): Given command alias.
        *args (list): Parent class constructor args.
        **kwargs (dict): Parent class constructor kwargs.

    Attributes:
        alias (str): Given command alias.

    Resources:
        1. `click.Command class documentation`_

    .. _click.Command class documentation:
        https://click.palletsprojects.com/en/8.1.x/api/#click.Command

    """

    def __init__(self, alias: str = "", *args: Any, **kwargs: Any):
        """Initialize Command class object instance."""
        super().__init__(*args, **kwargs)
        self.alias = alias


class ClickAliasedGroup(click.Group):
    """Custom click.Group class implementation.

    Attributes:
        aliases (typing.Dict[str, str]): Map of command aliases to their names.

    Resources:
        1. `click.Group class documentation`_

    .. _click.Group class documentation:
        https://click.palletsprojects.com/en/8.1.x/api/#click.Group

    """

    def __init__(self, *args: Any, **kwargs: Any):
        """Initialize ClickAliasedGroup class object instance."""
        super().__init__(*args, **kwargs)
        self.aliases: Dict[str, str] = dict()

    def add_command(self, cmd: click.Command, name: str | None = None) -> None:
        """Register another Command class object instance with this group.

        If the name is not provided, the name of the command is used.

        Args:
            cmd (Command): Command class object instance to register.
            name (typing.Optional[str]): Given command name.

        """
        super().add_command(cmd, name)
        name = name or cmd.name
        alias = getattr(cmd, "alias", None)

        if name and alias:
            self.aliases[alias] = name

    def get_command(self, ctx: click.Context, cmd_name: str) -> click.Command | None:
        """Return Command class object instance.

        Given a context and a command name or alias, this returns a ``Command`` class
        object instance if it exists.

        Args:
            ctx (click.Context): Click Context class object instance.
            cmd_name (str): Chosen command name.

        Returns:
            Command: Class object instance for given command name.

        """
        cmd_name = self.aliases.get(cmd_name, cmd_name)
        return super().get_command(ctx, cmd_name)

    def format_commands(
        self, ctx: click.Context, formatter: click.HelpFormatter
    ) -> None:
        """Write all the commands into the formatter if they exist.

        Args:
            ctx (click.Context): Click Context class object instance.
            formatter (click.HelpFormatter): Click HelpFormatter class object instance.

        """
        commands = []

        for subcommand in self.list_commands(ctx):
            cmd = self.get_command(ctx, subcommand)

            if cmd is None:
                continue
            if cmd.hidden:
                continue

            if hasattr(cmd, "alias") and cmd.alias:
                subcommand = f"{subcommand} ({cmd.alias})"

            commands.append((subcommand, cmd))

        if len(commands):
            limit = formatter.width - 6 - max(len(cmd[0]) for cmd in commands)

            rows = []
            for subcommand, cmd in commands:
                help = cmd.get_short_help_str(limit)
                rows.append((subcommand, help))

            if rows:
                with formatter.section("Commands"):
                    formatter.write_dl(rows)


class GeneratorCommand(ClickAliasedCommand):
    """Defines base class for all concrete fastapi-mvc generators.

    Args:
        category (str): Name under which generator should be printed in
            ``fastapi-mvc generate`` CLI command help page.

    Attributes:
        category (str): Name under which generator should be printed in
            ``fastapi-mvc generate`` CLI command help page.

    """

    def __init__(self, category: str = "Other", *args: Any, **kwargs: Any):
        """Initialize Generator class object instance."""
        super().__init__(*args, **kwargs)
        self.category = category

    def format_epilog(self, ctx: click.Context, formatter: click.HelpFormatter) -> None:
        """Write the epilog into the formatter if it exists.

        Args:
            ctx (click.Context): Click Context class object instance.
            formatter (click.HelpFormatter): Click HelpFormatter class object instance.

        """
        if self.epilog:
            formatter.write_paragraph()
            formatter.write(self.epilog)


class GeneratorsMultiCommand(click.MultiCommand):
    """Custom click.MultiCommand class implementation.

    Args:
        generators (typing.Dict[str, Generator]): Dictionary containing all available
            fastapi-mvc generators.
        generators_aliases (typing.Dict[str, str]): Map of generator aliases to their
            names.
        *args (list): Parent class constructor args.
        **kwargs (dict): Parent class constructor kwargs.

    Attributes:
        generators (typing.Dict[str, Generator]): Dictionary containing all available
            fastapi-mvc generators.
        generators_aliases (typing.Dict[str, str]): Map of generator aliases to their
            names.

    Resources:
        1. `click.MultiCommand class documentation`_

    .. _click.MultiCommand class documentation:
        https://click.palletsprojects.com/en/8.1.x/api/#click.MultiCommand

    """

    def __init__(
        self,
        generators: Dict[str, click.Command],
        alias: str = "",
        *args: Any,
        **kwargs: Any,
    ):
        """Initialize GeneratorsMultiCommand class object instance."""
        super().__init__(*args, **kwargs)
        self.generators = generators
        self.generators_aliases = dict()

        for name, gen in self.generators.items():
            if hasattr(gen, "alias") and gen.alias:
                self.generators_aliases[gen.alias] = name

        self.alias = alias

    def format_commands(
        self, ctx: click.Context, formatter: click.HelpFormatter
    ) -> None:
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

            if cmd.hidden:
                continue

            if hasattr(cmd, "alias") and cmd.alias:
                subcommand = f"{subcommand} ({cmd.alias})"

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

    def list_commands(self, ctx: click.Context) -> List[str]:
        """Return a list of subcommand names in the order they should appear.

        Args:
            ctx (click.Context): Click Context class object instance.

        Returns:
            list: List of subcommand names in the order they should appear.

        """
        return list(self.generators.keys())

    def get_command(self, ctx: click.Context, name: str) -> click.Command:
        """Return GeneratorCommand class object instance.

        Given a context and a command name or alias, this returns a ``GeneratorCommand``
        class object instance if it exists or aborts the execution of the program.

        Args:
            ctx (click.Context): Click Context class object instance.
            name (str): Chosen generator name.

        Returns:
            Generator: Class object instance for given command name.

        """
        name = self.generators_aliases.get(name, name)

        if name not in self.generators:
            ctx.fail(f"No such generator '{name}'.")

        return self.generators[name]
