import mock
import pytest
from fastapi_mvc.cli.commands.new import new


def test_new_help(cli_runner):
    result = cli_runner.invoke(new, ["--help"])
    assert result.exit_code == 0


def test_new_invalid_options(cli_runner):
    result = cli_runner.invoke(new, ["--not_exists"])
    assert result.exit_code == 2


@mock.patch("fastapi_mvc.cli.commands.new.Context")
def test_new_default_values(context_mock, cli_runner):
    result = cli_runner.invoke(new, ["test-project"])
    assert result.exit_code == 0

    context_mock.return_value.execute.assert_called_once_with(
        app_path="test-project",
        options={
            "skip_redis": False,
            "skip_aiohttp": False,
            "skip_vagrantfile": False,
            "skip_helm": False,
            "skip_actions": False,
            "skip_codecov": False,
            "skip_install": False,
            "license": "MIT",
            "repo_url": "https://your.repo.url.here"
        }
    )


@pytest.mark.parametrize(
    "args, expected",
    [
        (
            [
                "-R",
                "-A",
                "-V",
                "-H",
                "-G",
                "-C",
                "-I",
                "--license",
                "LGPLv3+",
                "--repo-url",
                "https://github.com/gandalf/gondorapi",
                "test-project"
            ],
            {
                "options": {
                    "skip_redis": True,
                    "skip_aiohttp": True,
                    "skip_vagrantfile": True,
                    "skip_helm": True,
                    "skip_actions": True,
                    "skip_codecov": True,
                    "skip_install": True,
                    "license": "LGPLv3+",
                    "repo_url": "https://github.com/gandalf/gondorapi"
                },
                "app_path": "test-project",
            }
        ),
        (
            [
                "--skip-redis",
                "--skip-aiohttp",
                "--skip-vagrantfile",
                "--skip-helm",
                "--skip-actions",
                "--skip-codecov",
                "--skip-install",
                "--license",
                "LGPLv3+",
                "--repo-url",
                "https://github.com/gandalf/gondorapi",
                "/home/gandalf/repos/you-shall-not-pass",
            ],
            {
                "options": {
                    "skip_redis": True,
                    "skip_aiohttp": True,
                    "skip_vagrantfile": True,
                    "skip_helm": True,
                    "skip_actions": True,
                    "skip_codecov": True,
                    "skip_install": True,
                    "license": "LGPLv3+",
                    "repo_url": "https://github.com/gandalf/gondorapi"
                },
                "app_path": "/home/gandalf/repos/you-shall-not-pass",
            }
        )
    ]
)
@mock.patch("fastapi_mvc.cli.commands.new.Context")
def test_new_with_options(context_mock, cli_runner, args, expected):
    result = cli_runner.invoke(new, args)
    assert result.exit_code == 0

    context_mock.return_value.execute.assert_called_once_with(**expected)
