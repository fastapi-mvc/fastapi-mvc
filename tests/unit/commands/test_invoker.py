import mock
import pytest
from fastapi_mvc.commands import Invoker, Command


@pytest.fixture
def invoker():
    yield Invoker()


def test_invoker(invoker):
    command_1 = mock.Mock(spec=Command)
    command_2 = mock.Mock(spec=Command)
    command_3 = mock.Mock(spec=Command)
    command_4 = mock.Mock()

    invoker.on_start = command_1
    invoker.on_finish = command_2
    assert invoker.on_start == command_1
    assert invoker.on_finish == command_2
    invoker.execute()

    invoker.on_start = command_3
    invoker.on_finish = None
    assert invoker.on_start == command_3
    invoker.execute()

    invoker.on_finish = command_4
    assert invoker.on_finish == command_4
    invoker.execute()

    command_1.execute.assert_called_once()
    command_2.execute.assert_called_once()
    assert command_3.execute.call_count == 2
    command_4.assert_not_called()
