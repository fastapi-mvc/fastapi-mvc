"""Command-line interface - generate command.

Attributes:
    cmd_help (str): The help string to use for this command.
    cmd_short_help (str): The short help to use for this command. This is shown on the
        command listing of the parent command.

"""
from fastapi_mvc import GeneratorsMultiCommand
from fastapi_mvc.generators import load_generators


cmd_short_help = "Run chosen fastapi-mvc generator."
cmd_help = """\
The 'fastapi-mvc generate' commands runs a generator of your choice for a
fastapi-mvc project at the current working directory.
"""


def get_generate_cmd():
    """Return command-line interface generate command.

    Returns:
        GeneratorsMultiCommand: Class object instance.

    """
    return GeneratorsMultiCommand(
        name="generate",
        subcommand_metavar="GENERATOR [ARGS]...",
        generators=load_generators(),
        short_help=cmd_short_help,
        help=cmd_help,
    )
