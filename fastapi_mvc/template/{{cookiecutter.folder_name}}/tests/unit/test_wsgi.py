import sys
import os

import mock
from {{cookiecutter.package_name}}.wsgi import run_wsgi


@mock.patch("{{cookiecutter.package_name}}.wsgi.ApplicationLoader")
def test_run_wsgi(loader_mock):
    run_wsgi("localhost", "5555", "2")
    loader_mock.assert_called_once()
    assert sys.argv == [
        "--gunicorn",
        "-c",
        os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "../../{{cookiecutter.package_name}}/config/gunicorn.conf.py"
            )
        ),
        "-w",
        "2",
        "-b localhost:5555",
        "{{cookiecutter.package_name}}.app.asgi:application"
    ]
