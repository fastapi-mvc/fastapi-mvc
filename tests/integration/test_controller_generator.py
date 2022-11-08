import os

from fastapi_mvc.generators import controller


def assert_paths(paths, condition):
    for path in paths:
        assert condition(path)


def test_controller(cli_runner, fake_project, monkeypatch):
    monkeypatch.chdir(fake_project)
    result = cli_runner.invoke(
        controller,
        ["--skip-routes", "stock_market", "ticker", "buy:post", "sell:delete"],
    )
    assert result.exit_code == 0

    paths = [
        "test_project/app/controllers/stock_market.py",
        "tests/unit/app/controllers/test_stock_market.py",
    ]

    assert_paths(paths, condition=lambda x: os.path.isfile(x))
