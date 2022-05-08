import pytest
from pydantic.error_wrappers import ValidationError
from {{cookiecutter.package_name}}.app.views import ReadyResponse


@pytest.mark.parametrize(
    "value",
    [
        "ok",
        "Another string",
        "ąŻŹÐĄŁĘ®ŒĘŚÐ",
        15,
        False,
    ],
)
def test_ready_response(value):
    ready = ReadyResponse(status=value)

    schema = ready.schema()
    assert schema["description"] == "Ready response model."

    response = ready.dict()
    assert response["status"] == str(value)


@pytest.mark.parametrize(
    "value",
    [
        ({"status": "ok"}),
        ([123, "ok"]),
        (["ok", "ready"]),
    ],
)
def test_ready_response_invalid(value):
    with pytest.raises(ValidationError):
        ReadyResponse(status=value)
