from http import HTTPStatus

import pytest
from pydantic.error_wrappers import ValidationError
from {{cookiecutter.package_name}}.app.views.error import ErrorModel, ErrorResponse


@pytest.mark.parametrize(
    "code, message, details",
    [
        (400, "test msg", None),
        ("500", "test msg", [{}]),
        (403, "test msg", [{"key": 123, "key2": 123.123, "foo": "bar"}]),
        (404, "test msg", [{"key": {"foo": "bar"}, "key2": [1, 2, 3]}]),
        ("401", "test msg", None),
    ],
)
def test_error_model(code, message, details):
    error = ErrorModel(code=code, message=message, details=details)

    schema = error.schema()
    assert schema["description"] == "Error model."
    assert schema["properties"]["status"] == {
        "title": "Status",
        "type": "string",
    }
    assert "status" in schema["required"]

    error_response = error.dict()
    assert error_response["code"] == int(code)
    assert error_response["message"] == message
    assert error_response["status"] == HTTPStatus(int(code)).name
    assert error_response["details"] == details


@pytest.mark.parametrize(
    "code, message, details",
    [
        (500, {}, [{}]),
        (403, "test msg", "foobar"),
        (None, None, 123),
        ({}, [], None),
        (False, "test msg", None),
    ],
)
def test_error_model_invalid(code, message, details):
    with pytest.raises(ValidationError):
        ErrorModel(code=code, message=message, details=details)


@pytest.mark.parametrize(
    "code, message, details",
    [
        (400, "test msg", None),
        ("500", "test msg", [{}]),
        (403, "test msg", [{"key": 123, "key2": 123.123, "foo": "bar"}]),
        (404, "test msg", [{"key": {"foo": "bar"}, "key2": [1, 2, 3]}]),
        ("401", "test msg", None),
    ],
)
def test_error_response(code, message, details):
    error = ErrorResponse(code=code, message=message, details=details)

    schema = error.schema()
    assert schema["description"] == "Error response model."

    error_response = error.dict()
    assert error_response["error"]["code"] == int(code)
    assert error_response["error"]["message"] == message
    assert error_response["error"]["status"] == HTTPStatus(int(code)).name
    assert error_response["error"]["details"] == details


@pytest.mark.parametrize(
    "code, message, details",
    [
        (500, {}, [{}]),
        (403, "test msg", "foobar"),
        (None, None, 123),
        ({}, [], None),
        (False, "test msg", None),
    ],
)
def test_error_response_invalid(code, message, details):
    with pytest.raises(ValidationError):
        ErrorResponse(code=code, message=message, details=details)
