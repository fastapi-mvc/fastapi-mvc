"""Command-line interface - new command."""
import click
from fastapi_mvc import Borg
from fastapi_mvc.cli.click_custom import GeneratorCommand
from fastapi_mvc.commands import RunGenerator
from fastapi_mvc.generators import ProjectGenerator


@click.pass_context
def invoke_generator(ctx, **params):
    """Invoke project generator.

    Args:
        ctx (click.Context): Click Context class object instance.
        params (typing.Dict[str, typing.Any]): Map of command option and
            argument names to their parsed values.

    """
    borg = Borg()

    generator = ctx.command.generator_cls()

    borg.enqueue(RunGenerator(generator=generator, options=params))
    borg.execute()


def get_new_cmd():
    """Return command-line interface new command.

    Returns:
        GeneratorCommand: Class object instance.

    """
    return GeneratorCommand(
        generator_cls=ProjectGenerator,
        callback=invoke_generator,
    )
