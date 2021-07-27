import pytest
from fastapi_mvc_template.app.models.ready import ReadyResponse
from pydantic.error_wrappers import ValidationError


@pytest.mark.parametrize("value", [
    "ok",
    "Another string",
    "ąŻŹÐĄŁĘ®ŒĘŚÐ",
    15,
    False,
])
def test_ready_response(value):
    ReadyResponse(status=value)


@pytest.mark.parametrize("value", [
    ({"status": "ok"}),
    ([123, "ok"]),
    (["ok", "ready"]),
])
def test_ready_response_invalid(value):
    with pytest.raises(ValidationError):
        ReadyResponse(status=value)
