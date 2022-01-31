# -*- coding: utf-8 -*-
"""Application Web Server Gateway Interface - gunicorn."""
import os
import sys
import logging

from gunicorn.app.base import Application
from {{cookiecutter.package_name}}.app.asgi import get_app


log = logging.getLogger(__name__)


class ApplicationLoader(Application):
    """Bypasses the class `WSGIApplication."""

    def init(self, parser, opts, args):
        """Class ApplicationLoader object constructor."""
        self.cfg.set("default_proc_name", args[0])

    def load(self):
        """Load application."""
        return get_app()


def run_wsgi(host, port, workers, daemon=False, env=(), config=None, pid=None):
    """Run gunicorn WSGI with ASGI workers."""
    log.info("Start gunicorn WSGI with ASGI workers.")

    if not config:
        config = os.path.join(
            os.path.dirname(__file__), "config/gunicorn.conf.py"
        )

    sys.argv = [
        "--gunicorn",
        "-c",
        config,
        "-w",
        workers,
        "-b {host}:{port}".format(
            host=host,
            port=port,
        ),
    ]

    if daemon:
        sys.argv.append("--daemon")

    for var in env:
        sys.argv.append("--env")
        sys.argv.append(var)

    if pid:
        sys.argv.append("--pid")
        sys.argv.append(pid)

    sys.argv.append("{{cookiecutter.package_name}}.app.asgi:application")

    ApplicationLoader().run()


if __name__ == "__main__":
    run_wsgi(
        host=os.getenv("FASTAPI_HOST", "127.0.0.1"),
        port=os.getenv("FASTAPI_PORT", "8000"),
        workers=int(os.getenv("FASTAPI_WORKERS", 2)),
    )
