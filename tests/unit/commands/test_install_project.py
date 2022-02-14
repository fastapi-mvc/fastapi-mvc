import mock
import pytest
from fastapi_mvc.commands import InstallProject


@pytest.mark.parametrize(
    "app_path",
    [
        "foobar",
        "/tmp/test-app",
        "/path/to/my/awesome-project_mark15"
    ]
)
@mock.patch("fastapi_mvc.commands.install_project.ShellUtils")
def test_execute(utils_mock, app_path):
    command = InstallProject(app_path=app_path)
    command.execute()

    utils_mock.run_shell.assert_called_once_with(
        cmd=["make", "install"], cwd=app_path
    )
