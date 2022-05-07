from logging import Logger

import mock
from fastapi_mvc.commands import Command


@mock.patch.multiple("fastapi_mvc.commands.base.Command", __abstractmethods__=set())
def test_base_command():
    command = Command()
    command.execute()
    assert isinstance(command, Command)

    assert not hasattr(command, "__dict__")
    assert hasattr(command, "__slots__")
    assert command.__slots__ == "_log"
    assert isinstance(command._log, Logger)
