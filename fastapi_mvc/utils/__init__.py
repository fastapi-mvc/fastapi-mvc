"""fastapi-mvc."""
from fastapi_mvc.utils.shell import ShellUtils
from fastapi_mvc.utils.excepthook import global_except_hook


__all__ = (
    ShellUtils,
    global_except_hook,
)
