import os

from fastapi_mvc.generators import ScriptGenerator


def assert_paths(paths, condition):
    for path in paths:
        assert condition(path)


def test_script(cli_runner, fake_project, monkeypatch):
    monkeypatch.chdir(fake_project)
    result = cli_runner.invoke(
        ScriptGenerator,
        ["--use-nix", "my-script.sh"],
    )
    assert result.exit_code == 0

    paths = [
        "my-script.sh",
    ]

    assert_paths(paths, condition=lambda x: os.path.isfile(x))
    assert_paths(paths, condition=lambda x: os.access(x, os.X_OK))
