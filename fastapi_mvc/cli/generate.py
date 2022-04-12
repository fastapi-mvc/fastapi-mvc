"""FastAPI MVC CLI generate command implementation."""
import os

import click
from fastapi_mvc.generators.loader import load_generators


generators = load_generators()


class MyCLI(click.MultiCommand):

    def list_commands(self, ctx):
        return generators.keys()

    def get_command(self, ctx, name):
        params = []
        epilog = None
        generator = generators[name]

        for arg in generator.cli_arguments:
            params.append(click.Argument(**arg))

        for opt in generator.cli_options:
            params.append(click.Option(**opt))

        if os.path.isfile(generator.usage):
            with open(generator.usage, "r") as f:
                epilog = f.read()

        return click.Command(
            name,
            params=params,
            callback=invoke_generator,
            epilog=epilog,
        )


@click.command(cls=MyCLI)
def generate():
    pass


@click.pass_context
def invoke_generator(ctx, **options):
    print(ctx.command.name)
    print(options)
