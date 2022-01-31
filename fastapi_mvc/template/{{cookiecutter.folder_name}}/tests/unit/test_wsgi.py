import sys
import os

import mock
import pytest
from {{cookiecutter.package_name}}.wsgi import run_wsgi


default_config = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../../{{cookiecutter.package_name}}/config/gunicorn.conf.py"
    )
)


@mock.patch("{{cookiecutter.package_name}}.wsgi.ApplicationLoader")
@pytest.mark.parametrize(
    "kwargs, expected",
    [
        (
            {"host": "localhost", "port": "5555", "workers": "2"},
            [
                "--gunicorn",
                "-c",
                default_config,
                "-w",
                "2",
                "-b localhost:5555",
                "{{cookiecutter.package_name}}.app.asgi:application",
            ],
        ),
        (
            {
                "host": "0.0.0.0",
                "port": "80",
                "workers": "2",
                "daemon": True,
                "config": "/custom/gunicorn.conf.py",
                "env": ("FOO=BAR", "USE_FORCE=True"),
                "pid": "/path/to/file.pid",
            },
            [
                "--gunicorn",
                "-c",
                "/custom/gunicorn.conf.py",
                "-w",
                "2",
                "-b 0.0.0.0:80",
                "--daemon",
                "--env",
                "FOO=BAR",
                "--env",
                "USE_FORCE=True",
                "--pid",
                "/path/to/file.pid",
                "{{cookiecutter.package_name}}.app.asgi:application",
            ],
        ),
    ],
)
def test_run_wsgi(loader_mock, kwargs, expected):
    run_wsgi(**kwargs)
    loader_mock.assert_called_once()
    assert sys.argv == expected
