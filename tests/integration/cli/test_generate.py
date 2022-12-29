import os

from fastapi_mvc.cli.generate import get_generate_cmd


class TestCliGenerateCommand:

    def test_should_generate_from_custom_generator(self, cli_runner, monkeypatch, default_project):
        # given
        monkeypatch.chdir(default_project)

        # when
        result = cli_runner.invoke(get_generate_cmd(), ["generator", "dummy"])
        result2 = cli_runner.invoke(get_generate_cmd(), ["dummy", "HelloWorld"])

        # then
        assert result.exit_code == 0
        assert result2.exit_code == 0
        assert os.path.isfile(f"{default_project}/default_project/hello_world.py")