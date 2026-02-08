"""Fastapi-mvc utilities - generators.

Attributes:
    log (logging.Logger): Logger class object instance.

"""

from typing import Dict, Any, Optional
import os
import logging

from copier.user_data import load_answersfile_data
from fastapi_mvc.constants import ANSWERS_FILE

log = logging.getLogger(__name__)


def load_answers_file(
    project_root: Optional[str] = None, answers_file: str = ANSWERS_FILE
) -> Dict[str, Any]:
    """Define wrapper for Copier `load_answersfile_data` method.

    Load answers data from a `$project_root/$answers_file` file if it exists.

    Args:
        project_root (typing.Optional[str]): Given fastapi-mvc project root path.
        answers_file (str): Given name of Copier answers_file relative to project root.

    Returns:
        typing.Dict[str, typing.Any]: Loaded answers data.

    """
    return load_answersfile_data(
        dst_path=project_root or os.getcwd(),
        answers_file=answers_file,
    )


def ensure_permissions(
    path: str, r: bool = True, w: bool = False, x: bool = False
) -> None:
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


def require_fastapi_mvc_project() -> Dict[str, Any]:
    """Ensure valid fastapi-mvc project, and return loaded project data.

    Returns:
        typing.Dict[str, Any]: Loaded fastapi-mvc project answers data.

    Raises:
        SystemExit: If project data is empty or is missing required values.

    """
    project_data = load_answers_file()
    keys = [
        "_commit",
        "_src_path",
        "project_name",
    ]

    if not project_data:
        log.error(
            "Not a fastapi-mvc project. Try 'fastapi-mvc new --help' for "
            "details how to create one."
        )
        raise SystemExit(1)
    elif not all(el in project_data for el in keys):
        log.error(f"Answers file: {ANSWERS_FILE} is missing required values.")
        raise SystemExit(1)

    project_data["package_name"] = (
        project_data["project_name"].lower().replace(" ", "_").replace("-", "_")
    )

    return project_data
