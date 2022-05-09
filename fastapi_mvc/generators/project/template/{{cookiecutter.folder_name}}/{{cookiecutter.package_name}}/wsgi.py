"""Application Web Server Gateway Interface - gunicorn."""
import logging

from gunicorn.app.base import BaseApplication
from {{cookiecutter.package_name}}.config import gunicorn


class ApplicationLoader(BaseApplication):

    def __init__(self, application, overrides=None):
        if not overrides:
            overrides = dict()

        self._overrides = overrides
        self._application = application
        super().__init__()

    def _set_cfg(self, cfg):
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
        self.logger = logging.getLogger(self.__class__.__name__)
        cfg = vars(gunicorn)

        self._set_cfg(cfg)
        self.init()

    def init(self, parser=None, opts=None, args=None):
        self.cfg.set("default_proc_name", "test-project")
        self._set_cfg(self._overrides)

    def load(self):
        """Load application."""
        return self._application
