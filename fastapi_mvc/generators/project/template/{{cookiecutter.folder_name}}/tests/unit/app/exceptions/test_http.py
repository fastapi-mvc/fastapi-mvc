import pytest
import mock
from {{cookiecutter.package_name}}.app.exceptions import (
    HTTPException,
    http_exception_handler,
)


@pytest.mark.parametrize(
    "status_code, content, headers",
    [
        (400, "test msg", None),
        (403, "test msg", [{"key": 123, "key2": 123.123, "foo": "bar"}]),
        (
            404,
            {"key": 123, "key2": 123.123, "foo": "bar"},
            {"key": {"foo": "bar"}, "key2": [1, 2, 3]},
        ),
    ],
)
def test_exception(status_code, content, headers):
    ex = HTTPException(
        status_code=status_code,
        content=content,
        headers=headers,
    )

    assert issubclass(type(ex), Exception)
    assert ex.status_code == status_code
    assert ex.content == content
    assert ex.headers == headers

    ex_eval = eval(repr(ex))
    assert ex_eval.status_code == ex.status_code
    assert ex_eval.content == ex.content
    assert ex_eval.headers == ex.headers
    assert isinstance(ex_eval, HTTPException)


@pytest.mark.asyncio
@mock.patch("{{cookiecutter.package_name}}.app.exceptions.http.JSONResponse")
async def test_exception_handler(json_mock):
    req_mock = mock.MagicMock()
    ex = HTTPException(
        502, [{"key": 123, "key2": 123.123, "foo": "bar"}], {"foo": "bar"}
    )
    await http_exception_handler(req_mock, ex)
    json_mock.assert_called_once_with(
        status_code=502,
        content=[{"key": 123, "key2": 123.123, "foo": "bar"}],
        headers={"foo": "bar"},
    )
