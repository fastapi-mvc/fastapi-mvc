import mock
from fastapi_mvc.commands import Command


@mock.patch.multiple(
    "fastapi_mvc.commands.base.Command",
    __abstractmethods__=set()
)
def test_returns_1():
    command = Command()
    command.execute()
    assert isinstance(command, Command)
