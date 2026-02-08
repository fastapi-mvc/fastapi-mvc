import os
import copy
from datetime import datetime
from unittest import mock

import pytest
from fastapi_mvc.constants import VERSION
from fastapi_mvc.cli.new import new
from fastapi_mvc.constants import ANSWERS_FILE, COPIER_PROJECT


DIR = os.getcwd()


class TestCliNewCommand:

    @pytest.fixture
    def patched_new(self):
        cmd = copy.deepcopy(new)
        shell_patch = mock.patch("fastapi_mvc.cli.new.run_shell")
        git_patch = mock.patch(
            "fastapi_mvc.cli.new.get_git_user_info",
            return_value=("John Doe", "example@email.com"),
        )
        which_patch = mock.patch("fastapi_mvc.cli.new.shutil.which")
        copier_patch = mock.patch("fastapi_mvc.cli.new.copier")
        cmd.run_shell = shell_patch.start()
        cmd.get_git_user_info = git_patch.start()
        cmd.shutil_which = which_patch.start()
        cmd.copier = copier_patch.start()
        yield cmd
        shell_patch.stop()
        git_patch.stop()
        which_patch.stop()
        copier_patch.stop()
        del cmd

    def test_should_exit_zero_when_invoked_with_help(self, cli_runner):
        # given / when
        result = cli_runner.invoke(new, ["--help"])

        # then
        assert result.exit_code == 0

    def test_should_exit_error_when_invoked_with_invalid_option(self, cli_runner):
        # given / when
        result = cli_runner.invoke(new, ["--not_exists"])

        # then
        assert result.exit_code == 2

    def test_should_exit_zero_and_call_copier_with_defaults(self, patched_new, cli_runner):
        # given / when
        result = cli_runner.invoke(patched_new, ["test-project"])

        # then
        assert result.exit_code == 0
        patched_new.run_shell.assert_has_calls(
            [
                mock.call(cmd=["git", "init"], cwd=f"{DIR}/test-project"),
                mock.call(cmd=["make", "install"], cwd=f"{DIR}/test-project"),
            ]
        )
        patched_new.shutil_which.assert_called_once_with("make")
        patched_new.copier.run_copy.assert_called_once_with(
            src_path=COPIER_PROJECT.template,
            vcs_ref=COPIER_PROJECT.vcs_ref,
            dst_path=f"{DIR}/test-project",
            answers_file=ANSWERS_FILE,
            user_defaults={
                "project_name": "test-project",
                "author": "John Doe",
                "email": "example@email.com",
                "copyright_date": datetime.today().year,
                "fastapi_mvc_version": VERSION,
                "nix": True,
                "redis": True,
                "aiohttp": True,
                "github_actions": True,
                "helm": True,
                "license": "MIT",
                "repo_url": "https://your.repo.url.here",
                "container_image_name": "test-project",
                "chart_name": "test-project",
                "script_name": "test-project",
                "project_description": "This project was generated with fastapi-mvc.",
                "version": "0.1.0",
            },
            unsafe=True,
        )

    @pytest.mark.parametrize(
        "args, expected",
        [
            (
                    [
                        "-R",
                        "-A",
                        "-H",
                        "-G",
                        "-N",
                        "--license",
                        "LGPLv3+",
                        "--repo-url",
                        "https://github.com/gandalf/gondorapi",
                        "test-project",
                    ],
                    {
                        "src_path": COPIER_PROJECT.template,
                        "vcs_ref": COPIER_PROJECT.vcs_ref,
                        "dst_path": f"{DIR}/test-project",
                        "answers_file": ANSWERS_FILE,
                        "user_defaults": {
                            "project_name": "test-project",
                            "author": "John Doe",
                            "email": "example@email.com",
                            "copyright_date": datetime.today().year,
                            "fastapi_mvc_version": VERSION,
                            "nix": False,
                            "redis": False,
                            "aiohttp": False,
                            "github_actions": False,
                            "helm": False,
                            "license": "LGPLv3+",
                            "repo_url": "https://github.com/gandalf/gondorapi",
                            "container_image_name": "test-project",
                            "chart_name": "test-project",
                            "script_name": "test-project",
                            "project_description": "This project was generated with fastapi-mvc.",
                            "version": "0.1.0",
                        },
                        "unsafe": True,
                    },
            ),
            (
                    [
                        "--no-interaction",
                        "--repo-url",
                        "https://thethingyouallbeenwaitingfor.trustme",
                        "--use-repo",
                        "https://howtomambo.git",
                        "--use-version",
                        "0.1.0",
                        f"{DIR}/Mambo_No6",
                    ],
                    {
                        "src_path": "https://howtomambo.git",
                        "vcs_ref": "0.1.0",
                        "answers_file": ANSWERS_FILE,
                        "dst_path": f"{DIR}/Mambo_No6",
                        "data": {
                            "project_name": "Mambo_No6",
                            "author": "John Doe",
                            "email": "example@email.com",
                            "copyright_date": datetime.today().year,
                            "fastapi_mvc_version": VERSION,
                            "nix": True,
                            "redis": True,
                            "aiohttp": True,
                            "github_actions": True,
                            "helm": True,
                            "license": "MIT",
                            "repo_url": "https://thethingyouallbeenwaitingfor.trustme",
                            "container_image_name": "Mambo_No6",
                            "chart_name": "Mambo_No6",
                            "script_name": "Mambo_No6",
                            "project_description": "This project was generated with fastapi-mvc.",
                            "version": "0.1.0",
                        },
                        "overwrite": True,
                        "unsafe": True,
                    },
            ),
            (
                    ["."],
                    {
                        "src_path": COPIER_PROJECT.template,
                        "vcs_ref": COPIER_PROJECT.vcs_ref,
                        "answers_file": ANSWERS_FILE,
                        "dst_path": f"{DIR}",
                        "user_defaults": {
                            "project_name": os.path.basename(DIR),
                            "author": "John Doe",
                            "email": "example@email.com",
                            "copyright_date": datetime.today().year,
                            "fastapi_mvc_version": VERSION,
                            "nix": True,
                            "redis": True,
                            "aiohttp": True,
                            "github_actions": True,
                            "helm": True,
                            "license": "MIT",
                            "repo_url": "https://your.repo.url.here",
                            "container_image_name": os.path.basename(DIR),
                            "chart_name": os.path.basename(DIR),
                            "script_name": os.path.basename(DIR),
                            "project_description": "This project was generated with fastapi-mvc.",
                            "version": "0.1.0",
                        },
                        "unsafe": True,
                    }
            ),
        ],
    )
    def test_should_exit_zero_and_call_copier_with_parsed_arguments(self, patched_new, cli_runner, args, expected):
        # given / when
        result = cli_runner.invoke(patched_new, args)

        # then
        assert result.exit_code == 0
        patched_new.copier.run_copy.assert_called_once_with(**expected)

    def test_should_skip_make_if_not_present(self, patched_new, cli_runner):
        # given / when
        patched_new.shutil_which.return_value = False
        result = cli_runner.invoke(patched_new, ["test-project"])

        # then
        assert result.exit_code == 0
        patched_new.run_shell.assert_called_once_with(
            cmd=["git", "init"], cwd=f"{DIR}/test-project"
        )
        patched_new.shutil_which.assert_called_once_with("make")
