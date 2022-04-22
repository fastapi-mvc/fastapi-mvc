"""{{ cookiecutter.controller_name.capitalize().replace('_', ' ') }} controller implementation."""
import logging

from fastapi import APIRouter


router = APIRouter(
    prefix="/{{ cookiecutter.controller_name }}"
)
log = logging.getLogger(__name__)
{%- for endpoint, method in cookiecutter.controller_endpoints.items() %}


@router.{{ method }}(
    "/{{ endpoint }}",
    status_code=200,
    # Decorator options:
    # https://fastapi.tiangolo.com/tutorial/path-operation-configuration/
)
async def {{ endpoint }}():
    # Implement endpoint logic here.
    return {"hello": "world"}


{%- endfor %}
{%- raw %}

{% endraw %}