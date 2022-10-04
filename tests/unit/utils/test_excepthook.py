from unittest import mock

from fastapi_mvc.utils import global_except_hook


@mock.patch("fastapi_mvc.utils.excepthook.hint", return_value=mock.Mock)
@mock.patch("fastapi_mvc.utils.excepthook.template", return_value=mock.Mock)
@mock.patch("fastapi_mvc.utils.excepthook.log", return_value=mock.Mock)
def test_excepthook_debug(log_mock, template_mock, hint_mock):
    log_mock.isEnabledFor.return_value = True

    ex = Exception("Oh no! Something went wrong :(")
    global_except_hook(type(ex), ex, ex.__traceback__)

    log_mock.exception.assert_called_once_with(
        "Unhandled exception occurred during RunTime.",
        exc_info=(type(ex), ex, ex.__traceback__),
    )
    log_mock.info.assert_called_once_with(template_mock.format())
    hint_mock.format.assert_not_called()


@mock.patch("fastapi_mvc.utils.excepthook.hint", return_value=mock.Mock)
@mock.patch("fastapi_mvc.utils.excepthook.template", return_value=mock.Mock)
@mock.patch("fastapi_mvc.utils.excepthook.log", return_value=mock.Mock)
def test_excepthook_info(log_mock, template_mock, hint_mock):
    log_mock.isEnabledFor.return_value = False

    ex = Exception("Oh no! Something went wrong :(")
    global_except_hook(type(ex), ex, ex.__traceback__)

    log_mock.exception.assert_called_once_with(
        "Unhandled exception occurred during RunTime.",
        exc_info=(type(ex), ex, ex.__traceback__),
    )
    log_mock.info.assert_called_once_with(hint_mock.format())
    template_mock.format.assert_not_called()
