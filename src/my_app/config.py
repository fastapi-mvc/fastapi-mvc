import pathlib
import sys

# Use the standard library tomllib if available (Python 3.11+),
# otherwise fall back to the 'toml' package.
if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import toml as tomllib
    except ImportError:
        # This is a hard dependency for older Python versions.
        # The user needs a clear message if it's not installed.
        raise ImportError(
            "The 'toml' package is required for Python < 3.11. "
            "Please install it with: pip install toml"
        )


CONFIG_FILE_PATH = pathlib.Path("config.toml")


class ConfigError(Exception):
    """A specific exception for configuration-related problems."""
    pass


def load_app_config() -> dict:
    """
    Loads the application configuration from the 'config.toml' file.

    This function provides a user-friendly error message if the configuration
    file is missing, malformed, or cannot be read.

    Returns:
        A dictionary containing the parsed configuration.

    Raises:
        ConfigError: If any issue occurs during file loading or parsing.
    """
    try:
        with open(CONFIG_FILE_PATH, "rb") as f:
            return tomllib.load(f)
    except Exception as e:
        # Instead of letting a generic error like FileNotFoundError or a
        # TomlDecodeError bubble up, we catch it and raise our own
        # specific, more helpful exception.
        error_message = (
            f"Failed to load configuration from '{CONFIG_FILE_PATH}'.\n\n"
            "Please make sure the file exists in the correct location and is a "
            "valid TOML file.\n\n"
            f"Reason: {e.__class__.__name__}: {e}"
        )
        raise ConfigError(error_message) from e