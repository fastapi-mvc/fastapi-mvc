"""Command-line interface - utilities."""
import os

import click


def validate_directory(ctx, param, value):
    """Verify if given path value is writable and parent directory exists.

    Args:
        ctx (click.Context): Click Context object instance.
        param (click.Option): Click Option object instance.
        value (str): Click Option value.

    Returns:
        str: Original value.

    Raises:
        click.BadParameter: If given path value is not writable or parent
            directory does not exist.

    """
    if not param.required and not value:
        return value

    dirname = os.path.dirname(value)

    if not os.path.exists(dirname):
        raise click.BadParameter(f"Directory '{dirname}' does not exist.")
    elif not os.access(dirname, os.W_OK):
        raise click.BadParameter(f"Directory '{dirname}' is not writable.")

    return value
