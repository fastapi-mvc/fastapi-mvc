"""Command-line interface - generate command."""
import click
from fastapi_mvc import Borg
from fastapi_mvc.commands import RunGenerator
from fastapi_mvc.cli.click_custom import GeneratorsMultiCommand


cmd_short_help = "Run chosen fastapi-mvc generator."
cmd_help = """\
The 'fastapi-mvc generate' commands runs a generator of your choice for a
fastapi-mvc project at the current working directory.
"""


@click.pass_context
def invoke_generator(ctx, **params):
    """Invoke generator associated with invoked generate subcommand.

    Args:
        ctx (click.Context): Click Context class object instance.
        params (typing.Dict[str, typing.Any]): Map of command option and
            argument names to their parsed values.

    """
    borg = Borg()
    borg.require_project()

    generator = ctx.command.generator_cls(borg.parser)

    borg.enqueue(RunGenerator(generator=generator, options=params))
    borg.execute()


def get_generate_cmd():
    """Return command-line interface generate command.

    Returns:
        GeneratorsMultiCommand: Class object instance.

    """
    borg = Borg()
    borg.load_generators()

    return GeneratorsMultiCommand(
        name="generate",
        subcommand_metavar="GENERATOR [ARGS]...",
        generators=borg.generators,
        command_callback=invoke_generator,
        short_help=cmd_short_help,
        help=cmd_help,
    )
