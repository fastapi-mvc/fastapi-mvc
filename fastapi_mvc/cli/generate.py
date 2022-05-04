"""FastAPI MVC CLI generate command implementation."""
import click
from fastapi_mvc import Borg
from fastapi_mvc.commands import Generate
from fastapi_mvc.cli.click_custom import GeneratorsMultiCommand


@click.pass_context
def invoke_generator(ctx, **options):
    """Invoke generator associated with invoked CLI command.

    Args:
        ctx (click.Context): Click Context class object instance.
        options (dict): Generator CLI command options and arguments.

    """
    borg = Borg()
    borg.require_project()

    generator = ctx.command.generator_cls(borg.parser)

    borg.enqueue_command(Generate(generator=generator, options=options))
    borg.execute()


def get_generate_cmd():
    """Get `fastapi-mvc generate` CLI command.

    Returns:
        GeneratorsMultiCommand: GeneratorsMultiCommand class object instance.

    """
    borg = Borg()
    borg.load_generators()

    cmd_help = (
        "The 'fastapi-mvc generate' commands runs a generator of your "
        "choice for a fastapi-mvc project at the current working "
        "directory."
    )

    return GeneratorsMultiCommand(
        name="generate",
        subcommand_metavar="GENERATOR [ARGS]...",
        generators=borg.generators,
        command_callback=invoke_generator,
        short_help="Run chosen fastapi-mvc generator.",
        help=cmd_help,
    )
