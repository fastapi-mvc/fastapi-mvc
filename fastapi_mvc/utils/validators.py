"""Fastapi-mvc validators.

Attributes:
    log (logging.Logger): Logger class object instance.

"""
from typing import Dict, Any
import os
import logging


log = logging.getLogger(__name__)


def ensure_permissions(path: str, r: bool = True, w: bool = False, x: bool = False) -> None:
    """Ensure correct permissions to given path.

    Args:
        path (str): Given path to check.
        r (bool): Check read ok.
        w (bool): Check write ok.
        x (bool): Check executable ok.

    Raises:
        SystemExit: If path has insufficient permissions.

    """
    if not os.path.exists(path):
        log.error(f"Path: '{path}' does not exist.")
        raise SystemExit(1)

    if r and not os.access(path, os.R_OK):
        log.error(f"Path: '{path}' is not readable.")
        raise SystemExit(1)

    if w and not os.access(path, os.W_OK):
        log.error(f"Path: '{path}' is not writable.")
        raise SystemExit(1)

    if x and not os.access(path, os.X_OK):
        log.error(f"Path: '{path}' is not executable.")
        raise SystemExit(1)


def ensure_project_data(project_data: Dict[str, Any]) -> None:
    """Ensure necessary fastapi-mvc project data existence.

    Args:
        project_data: Given fastapi-mvc answers file data.

    Raises:
        SystemExit: If project data is empty or is missing required values.

    """
    if not project_data or "package_name" not in project_data:
        log.error(
            "Not a fastapi-mvc project. Try 'fastapi-mvc new --help' for "
            "details how to create one."
        )
        raise SystemExit(1)
