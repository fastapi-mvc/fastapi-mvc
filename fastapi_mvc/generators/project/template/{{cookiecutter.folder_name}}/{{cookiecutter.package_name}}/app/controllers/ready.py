"""Application implementation - Ready controller."""
import logging

from fastapi import APIRouter
from {{cookiecutter.package_name}}.config import settings
{%- if cookiecutter.redis == "yes" %}
from {{cookiecutter.package_name}}.app.utils import RedisClient
from {{cookiecutter.package_name}}.app.views import ReadyResponse, ErrorResponse
from {{cookiecutter.package_name}}.app.exceptions import HTTPException
{%- else %}
from {{cookiecutter.package_name}}.app.views import ReadyResponse
{%- endif %}

router = APIRouter()
log = logging.getLogger(__name__)


@router.get(
    "/ready",
    tags=["ready"],
    response_model=ReadyResponse,
    summary="Simple health check.",
    status_code=200,
    {%- if cookiecutter.redis == "yes" %}
    responses={502: {"model": ErrorResponse}},
    {%- endif %}
)
async def readiness_check():
    """Run basic application health check.

    If the application is up and running then this endpoint will return simple
    response with status ok. Moreover, if it has Redis enabled then connection
    to it will be tested. If Redis ping fails, then this endpoint will return
    502 HTTP error.
    \f

    Returns:
        response (ReadyResponse): ReadyResponse model object instance.

    Raises:
        HTTPException: If applications has enabled Redis and can not connect
            to it. NOTE! This is the custom exception, not to be mistaken with
            FastAPI.HTTPException class.

    """
    log.info("Started GET /ready")
    {%- if cookiecutter.redis == "yes" %}

    if settings.USE_REDIS and not await RedisClient.ping():
        log.error("Could not connect to Redis")
        raise HTTPException(
            status_code=502,
            content=ErrorResponse(
                code=502, message="Could not connect to Redis"
            ).dict(exclude_none=True),
        )

    {%- else %}

    if settings.USE_REDIS:
        log.warning(
            "Redis utility skipped. Please set FASTAPI_USE_REDIS=false"
        )

    {%- endif %}
    return ReadyResponse(status="ok")
