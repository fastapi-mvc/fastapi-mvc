"""Fastapi-mvc utilities.

The ``fastapi-mvc.utils`` submodule implements generic utilities for the need of
the package.

"""
from fastapi_mvc.utils.shell import run_shell, get_git_user_info
from fastapi_mvc.utils.excepthook import global_except_hook


__all__ = ("run_shell", "get_git_user_info", "global_except_hook")
