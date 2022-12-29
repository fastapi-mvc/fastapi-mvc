import logging

from fastapi_mvc.utils import global_except_hook


class TestGlobalExceptHook:

    def test_should_format_issue_template(self, caplog):
        # given
        caplog.set_level(logging.DEBUG)
        ex = Exception("Oh no! Something went wrong :(")

        # when
        global_except_hook(type(ex), ex, ex.__traceback__)

        # then
        assert len(caplog.records) == 2
        assert caplog.records[0].message == "Unhandled exception occurred during RunTime."
        assert caplog.records[0].exc_info == (type(ex), ex, ex.__traceback__)
        assert "**Describe the bug**" in caplog.records[1].message

    def test_should_format_hint_template(self, caplog):
        # given
        caplog.set_level(logging.INFO)
        ex = Exception("Oh no! Something went wrong :(")

        # when
        global_except_hook(type(ex), ex, ex.__traceback__)

        # then
        assert len(caplog.records) == 2
        assert caplog.records[0].message == "Unhandled exception occurred during RunTime."
        assert caplog.records[0].exc_info == (type(ex), ex, ex.__traceback__)
        assert "Hint:" in caplog.records[1].message
