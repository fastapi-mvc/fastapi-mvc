# -*- coding: utf-8 -*-
"""Ready controller."""
import logging

from fastapi import APIRouter
from fastapi_mvc_template.app.models.ready import ReadyResponse

router = APIRouter()
log = logging.getLogger(__name__)


@router.get(
    "/ready",
    tags=["ready"],
    response_model=ReadyResponse,
    summary="Simple health check."
)
async def readiness_check():
    """Run basic application health check.

    If application is up and running then this endpoint will return simple
    response with status ok. Otherwise app will be unavailable or an internal
    server error will be returned.
    \f

    Returns:
        response (ReadyResponse): ReadyResponse model object instance.

    """
    log.info("Started GET /ready")
    return ReadyResponse(status="ok")
