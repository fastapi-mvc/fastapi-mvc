# -*- coding: utf-8 -*-
"""Aiohttp client class utility."""
import logging
import asyncio
from dataclasses import dataclass
from typing import Optional
from socket import AF_INET

import aiohttp
from pydantic import BaseModel


SIZE_POOL_AIOHTTP = 100


class AiohttpClient(object):
    """Aiohttp session client utility.

    Utility class for handling HTTP async request for whole FastAPI application
    scope.

    Attributes:
        sem (asyncio.Semaphore, optional): Semaphore value.
        aiohttp_client (aiohttp.ClientSession, optional): Aiohttp client session
            object instance.

    """

    sem: Optional[asyncio.Semaphore] = None
    aiohttp_client: Optional[aiohttp.ClientSession] = None
    log: logging.Logger = logging.getLogger(__name__)

    @classmethod
    def get_aiohttp_client(cls):
        """Create aiohttp client session object instance.

        Returns:
            aiohttp.ClientSession: ClientSession object instance.

        """
        if cls.aiohttp_client is None:
            cls.log.debug("Initialize AiohttpClient session.")
            timeout = aiohttp.ClientTimeout(total=2)
            connector = aiohttp.TCPConnector(
                family=AF_INET,
                limit_per_host=SIZE_POOL_AIOHTTP,
            )
            cls.aiohttp_client = aiohttp.ClientSession(
                timeout=timeout,
                connector=connector,
            )

        return cls.aiohttp_client

    @classmethod
    async def close_aiohttp_client(cls):
        """Close aiohttp client session."""
        if cls.aiohttp_client:
            cls.log.debug("Close AiohttpClient session.")
            await cls.aiohttp_client.close()
            cls.aiohttp_client = None

    @classmethod
    async def get(cls, url):
        """Execute HTTP GET request.

        Args:
            url (str): HTTP GET request endpoint.

        Returns:
            response: HTTP GET request response. Either aiohttp.ClientResponse
                object instance, or if timeout occured returns CustomResponse
                object instance.

        """
        client = cls.get_aiohttp_client()

        try:
            cls.log.debug("Started GET {}".format(url))
            return await client.get(url)
        except asyncio.TimeoutError:
            cls.log.warning("Completed 408 Request Timeout")
            return CustomResponse(
                status=408, content={"detail": "Request Timeout"}
            )


@dataclass(init=False)
class CustomResponse(BaseModel):
    """Custom response model class.

    This utility helps to unify responses by keeping object-like attribute
    calling for classes and methods which utilize AiohttpClient.

    Attributes:
        status (int): Uses int(v) to coerce types to an int.
        content (dict): dict(v) is used to attempt to convert a dictionary.

    Raises:
        pydantic.error_wrappers.ValidationError: If any of provided attribute
            doesn't pass type validation.

    """

    status: int
    content: dict
