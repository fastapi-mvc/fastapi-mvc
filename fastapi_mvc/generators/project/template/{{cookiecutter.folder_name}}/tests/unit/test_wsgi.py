import mock
import pytest
from gunicorn.app.base import BaseApplication
from gunicorn.errors import ConfigError
from {{cookiecutter.package_name}} import ApplicationLoader


@mock.patch.object(BaseApplication, "run")
def test_wsgi_conf_defaults(run_mock):
    app = mock.Mock()
    wsgi = ApplicationLoader(app)
    assert wsgi.load() == app
    assert wsgi.cfg.worker_class_str == "uvicorn.workers.UvicornWorker"

    assert wsgi.cfg.address == [("127.0.0.1", 8000)]
    assert wsgi.cfg.env == {}

    assert wsgi.cfg.settings["bind"].value == ["127.0.0.1:8000"]
    assert wsgi.cfg.settings["raw_env"].value == []
    assert wsgi.cfg.settings["workers"].value == 2
    assert not wsgi.cfg.settings["daemon"].value
    assert not wsgi.cfg.settings["pidfile"].value

    wsgi.run()
    run_mock.assert_called_once()


@mock.patch.object(BaseApplication, "run")
def test_wsgi_cli_overrides(run_mock):
    app = mock.Mock()
    wsgi = ApplicationLoader(
        application=app,
        overrides={
            "raw_env": ("FOOBAR=123",),
            "bind": "0.0.0.0:3000",
            "workers": 3,
            "daemon": True,
            "pidfile": "/tmp/api.pid"
        }
    )
    # Test unused patched method for coverage sake.
    wsgi.init(None, None, None)

    assert wsgi.cfg.address == [("0.0.0.0", 3000)]
    assert wsgi.cfg.env == {"FOOBAR": "123"}

    assert wsgi.cfg.settings["bind"].value == ["0.0.0.0:3000"]
    assert wsgi.cfg.settings["raw_env"].value == ["FOOBAR=123"]
    assert wsgi.cfg.settings["workers"].value == 3
    assert wsgi.cfg.settings["daemon"].value
    assert wsgi.cfg.settings["pidfile"].value == "/tmp/api.pid"

    wsgi.run()
    run_mock.assert_called_once()


def test_wsgi_bad_config():
    app = mock.Mock()
    with pytest.raises(SystemExit):
        ApplicationLoader(
            application=app,
            overrides={
                "unknown": True,
                "workers": None,
            }
        )
