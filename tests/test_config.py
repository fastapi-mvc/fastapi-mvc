import pytest
from pathlib import Path

# Assuming the project structure has a config module like this:
# src/
#   your_project/
#     config.py  (contains load_config and ConfigError)
from your_project.config import load_config, ConfigError


def test_load_config_with_missing_key_raises_helpful_error(tmp_path: Path):
    """
    Verify that loading a config with a missing required field
    raises a ConfigError with a user-friendly message.

    This is crucial for a good onboarding experience. If a user forgets
    a key, we should tell them exactly what's missing and where.
    """
    # GIVEN an invalid config file that's missing a required key
    invalid_config_content = """
[tool.your_project]
# The 'api_key' is deliberately missing to trigger the error.
user = "test_user"
"""
    config_file = tmp_path / "pyproject.toml"
    config_file.write_text(invalid_config_content)

    # WHEN we attempt to load this broken configuration
    # THEN a ConfigError should be raised with a specific, helpful message
    with pytest.raises(ConfigError) as exc_info:
        load_config(config_file)

    # Assert that the error message clearly identifies the missing key and section
    error_message = str(exc_info.value)
    assert "Missing required key: 'api_key'" in error_message
    assert "in the [tool.your_project] section" in error_message