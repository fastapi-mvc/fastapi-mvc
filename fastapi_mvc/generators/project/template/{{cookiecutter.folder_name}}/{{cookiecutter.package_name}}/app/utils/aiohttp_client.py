"""Aiohttp client class utility."""
import logging
import asyncio
from typing import Optional
from socket import AF_INET

import aiohttp


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
    async def get(cls, url, headers=None, raise_for_status=False):
        """Execute HTTP GET request.

        Args:
            url (str): HTTP GET request endpoint.
            headers (dict): Optional HTTP Headers to send with the request.
            raise_for_status (bool): Automatically call
                ClientResponse.raise_for_status() for response if set to True.

        Returns:
            response: HTTP GET request response - aiohttp.ClientResponse
                object instance.

        """
        client = cls.get_aiohttp_client()

        cls.log.debug(f"Started GET {url}")
        response = await client.get(
            url,
            headers=headers,
            raise_for_status=raise_for_status,
        )

        return response

    @classmethod
    async def post(cls, url, data=None, headers=None, raise_for_status=False):
        """Execute HTTP POST request.

        Args:
            url (str): HTTP POST request endpoint.
            data (any): The data to send in the body of the request. This can
                be a FormData object or anything that can be passed into
                FormData, e.g. a dictionary, bytes, or file-like object.
            headers (dict): Optional HTTP Headers to send with the request.
            raise_for_status (bool): Automatically call
                ClientResponse.raise_for_status() for response if set to True.

        Returns:
            response: HTTP POST request response - aiohttp.ClientResponse
                object instance.

        """
        client = cls.get_aiohttp_client()

        cls.log.debug(f"Started POST: {url}")
        response = await client.post(
            url,
            data=data,
            headers=headers,
            raise_for_status=raise_for_status,
        )

        return response

    @classmethod
    async def put(cls, url, data=None, headers=None, raise_for_status=False):
        """Execute HTTP PUT request.

        Args:
            url (str): HTTP PUT request endpoint.
            data (any): The data to send in the body of the request. This can
                be a FormData object or anything that can be passed into
                FormData, e.g. a dictionary, bytes, or file-like object.
            headers (dict): Optional HTTP Headers to send with the request.
            raise_for_status (bool): Automatically call
                ClientResponse.raise_for_status() for response if set to True.

        Returns:
            response: HTTP PUT request response - aiohttp.ClientResponse
                object instance.

        """
        client = cls.get_aiohttp_client()

        cls.log.debug(f"Started PUT: {url}")
        response = await client.put(
            url,
            data=data,
            headers=headers,
            raise_for_status=raise_for_status,
        )

        return response

    @classmethod
    async def delete(cls, url, headers=None, raise_for_status=False):
        """Execute HTTP DELETE request.

        Args:
            url (str): HTTP DELETE request endpoint.
            headers (dict): Optional HTTP Headers to send with the request.
            raise_for_status (bool): Automatically call
                ClientResponse.raise_for_status() for response if set to True.

        Returns:
            response: HTTP DELETE request response - aiohttp.ClientResponse
                object instance.

        """
        client = cls.get_aiohttp_client()

        cls.log.debug(f"Started DELETE: {url}")
        response = await client.delete(
            url,
            headers=headers,
            raise_for_status=raise_for_status,
        )

        return response

    @classmethod
    async def patch(cls, url, data=None, headers=None, raise_for_status=False):
        """Execute HTTP PATCH request.

        Args:
            url (str): HTTP PATCH request endpoint.
            data (any): The data to send in the body of the request. This can
                be a FormData object or anything that can be passed into
                FormData, e.g. a dictionary, bytes, or file-like object.
            headers (dict): Optional HTTP Headers to send with the request.
            raise_for_status (bool): Automatically call
                ClientResponse.raise_for_status() for response if set to True.

        Returns:
            response: HTTP PATCH request response - aiohttp.ClientResponse
                object instance.

        """
        client = cls.get_aiohttp_client()

        cls.log.debug(f"Started PATCH: {url}")
        response = await client.patch(
            url,
            data=data,
            headers=headers,
            raise_for_status=raise_for_status,
        )

        return response
