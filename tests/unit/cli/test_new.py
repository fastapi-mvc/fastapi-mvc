import mock
import pytest
from fastapi_mvc.cli.new import get_new_cmd
from fastapi_mvc.generators import ProjectGenerator


@mock.patch("fastapi_mvc.cli.new.Borg")
def test_new_help(borg_mock, cli_runner):
    result = cli_runner.invoke(get_new_cmd(), ["--help"])
    assert result.exit_code == 0
    borg_mock.assert_not_called()


@mock.patch("fastapi_mvc.cli.new.Borg")
def test_new_invalid_options(borg_mock, cli_runner):
    result = cli_runner.invoke(get_new_cmd(), ["--not_exists"])
    assert result.exit_code == 2
    borg_mock.assert_not_called()


@mock.patch("fastapi_mvc.cli.new.RunGenerator")
@mock.patch("fastapi_mvc.cli.new.Borg")
def test_new_default_values(borg_mock, run_mock, cli_runner, mock_project_gen):
    with mock.patch("fastapi_mvc.cli.new.ProjectGenerator", new=mock_project_gen):
        result = cli_runner.invoke(get_new_cmd(), ["test-project"])
        assert result.exit_code == 0

    borg_mock.assert_called_once()
    run_mock.assert_called_once_with(
        generator=mock_project_gen.return_value,
        options={
            "app_path": "test-project",
            "skip_redis": False,
            "skip_aiohttp": False,
            "skip_helm": False,
            "skip_nix": False,
            "skip_actions": False,
            "skip_install": False,
            "license": "MIT",
            "repo_url": "https://your.repo.url.here",
            "template_version": ProjectGenerator.template_version,
            "override_template": None,
        },
    )

    borg_mock.return_value.enqueue.assert_called_once_with(run_mock.return_value)
    borg_mock.return_value.execute.assert_called_once()


@pytest.mark.parametrize(
    "args, expected",
    [
        (
            [
                "-R",
                "-A",
                "-H",
                "-G",
                "-I",
                "-N",
                "--license",
                "LGPLv3+",
                "--repo-url",
                "https://github.com/gandalf/gondorapi",
                "test-project",
            ],
            {
                "app_path": "test-project",
                "skip_redis": True,
                "skip_aiohttp": True,
                "skip_helm": True,
                "skip_actions": True,
                "skip_install": True,
                "skip_nix": True,
                "license": "LGPLv3+",
                "repo_url": "https://github.com/gandalf/gondorapi",
                "template_version": ProjectGenerator.template_version,
                "override_template": None,
            },
        ),
        (
            [
                "--skip-redis",
                "--skip-aiohttp",
                "--skip-helm",
                "--skip-actions",
                "--skip-install",
                "--skip-nix",
                "--license",
                "LGPLv3+",
                "--repo-url",
                "https://github.com/gandalf/gondorapi",
                "/home/gandalf/repos/you-shall-not-pass",
                "--template-version",
                "0.1.0",
                "--override-template",
                "https://github.com/gandalf/gondortemplate",
            ],
            {
                "app_path": "/home/gandalf/repos/you-shall-not-pass",
                "skip_redis": True,
                "skip_aiohttp": True,
                "skip_helm": True,
                "skip_actions": True,
                "skip_install": True,
                "skip_nix": True,
                "license": "LGPLv3+",
                "repo_url": "https://github.com/gandalf/gondorapi",
                "template_version": "0.1.0",
                "override_template": "https://github.com/gandalf/gondortemplate",
            },
        ),
    ],
)
@mock.patch("fastapi_mvc.cli.new.RunGenerator")
@mock.patch("fastapi_mvc.cli.new.Borg")
def test_new_with_options(
    borg_mock, run_mock, cli_runner, mock_project_gen, args, expected
):
    with mock.patch("fastapi_mvc.cli.new.ProjectGenerator", new=mock_project_gen):
        result = cli_runner.invoke(get_new_cmd(), args)
        assert result.exit_code == 0

    borg_mock.assert_called_once()
    run_mock.assert_called_once_with(
        generator=mock_project_gen.return_value,
        options=expected,
    )

    borg_mock.return_value.enqueue.assert_called_once_with(run_mock.return_value)
    borg_mock.return_value.execute.assert_called_once()
