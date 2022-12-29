import os

from tests.integration.conftest import assert_paths
from fastapi_mvc.generators import ControllerGenerator


class TestControllerGeneratorCli:

    def test_should_generate_controller_using_given_arguments(self, cli_runner, default_project, monkeypatch):
        # given / when
        monkeypatch.chdir(default_project)
        result = cli_runner.invoke(
            ControllerGenerator,
            ["--skip-routes", "stock_market", "ticker", "buy:post", "sell:delete"],
        )

        # then
        assert result.exit_code == 0
        assert_paths(
            [
                f"{default_project}/default_project/app/controllers/stock_market.py",
                f"{default_project}/tests/unit/app/controllers/test_stock_market.py",
            ],
            condition=lambda x: os.path.isfile(x),
        )
