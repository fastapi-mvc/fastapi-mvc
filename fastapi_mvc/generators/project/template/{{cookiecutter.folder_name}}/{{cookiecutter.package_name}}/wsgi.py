"""Application Web Server Gateway Interface - gunicorn."""
import logging

from gunicorn.app.base import BaseApplication
from {{cookiecutter.package_name}}.config import gunicorn


class ApplicationLoader(BaseApplication):
    """Define gunicorn interface for any given web framework.

    Args:
        application (typing.Any): Any given web framework application object
            instance.
        overrides (typing.Optional[typing.Dict[str, typing.Any]]): Map of
            gunicorn settings to override.

    Attributes:
        _application (typing.Any): Any given web framework application object
            instance.
        _overrides (typing.Optional[typing.Dict[str, typing.Any]]): Map of
            gunicorn settings to override.

    """

    def __init__(self, application, overrides=None):
        """Initialize ApplicationLoader class object instance."""
        if not overrides:
            overrides = dict()

        self._overrides = overrides
        self._application = application
        super().__init__()

    def _set_cfg(self, cfg):
        """Set gunicorn config given map of setting names to their values.

        Args:
            cfg (typing.Dict[str, typing.Any]): Map of gunicorn setting names to
                their values.

        Raises:
            Exception: Raised on config error.

        """
        for k, v in cfg.items():
            # Ignore unknown names
            if k not in self.cfg.settings:
                continue

            try:
                self.cfg.set(k.lower(), v)
            except Exception as ex:
                self.logger.error(
                    "Invalid value for {key}: {val}".format(key=k, val=v)
                )
                raise ex

    def load_config(self):
        """Load gunicorn configuration."""
        self.logger = logging.getLogger(self.__class__.__name__)
        self.cfg.set("default_proc_name", "{{cookiecutter.folder_name}}")

        cfg = vars(gunicorn)
        cfg.update(self._overrides)

        self._set_cfg(cfg)

    def init(self, parser, opts, args):
        """Patch required but not needed base class method."""
        pass

    def load(self):
        """Load WSGI application."""
        return self._application
