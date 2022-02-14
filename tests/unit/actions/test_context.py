import mock
from fastapi_mvc.actions import Context


def test_context():
    action_1 = mock.Mock()
    action_2 = mock.Mock()
    action_3 = mock.Mock()

    ctx = Context(action_1)
    assert ctx.action == action_1
    ctx.execute("test arg", 123, foo="bar", param="value")

    ctx.action = action_2
    assert ctx.action == action_2
    ctx.execute([1, 2, 3])

    ctx.action = action_3
    assert ctx.action == action_3
    ctx.execute(order=66)

    action_1.execute.assert_called_once_with(
        "test arg", 123, foo="bar", param="value"
    )
    action_2.execute.assert_called_once()
    action_3.execute.assert_called_once_with(order=66)
