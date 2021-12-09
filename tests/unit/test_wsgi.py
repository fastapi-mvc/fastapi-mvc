import sys
import os

import mock
from fastapi_mvc_template.wsgi import run_wsgi


@mock.patch("fastapi_mvc_template.wsgi.ApplicationLoader")
def test_run_wsgi(loader_mock):
    run_wsgi("localhost", "5555", "2")
    loader_mock.assert_called_once()
    assert sys.argv == [
        "--gunicorn",
        "-c",
        os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "../../fastapi_mvc_template/config/gunicorn.conf.py"
            )
        ),
        "-w",
        "2",
        "-b localhost:5555",
        "fastapi_mvc_template.app.asgi:application"
    ]
