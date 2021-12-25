import pytest
import aiohttp
from aioresponses import aioresponses
from {{cookiecutter.package_name}}.app.utils import AiohttpClient


@pytest.mark.asyncio
async def test_get():
    with aioresponses() as mock:
        mock.get("http://example.com/api", status=200, payload=dict(time=237))
        AiohttpClient.get_aiohttp_client()
        response = await AiohttpClient.get("http://example.com/api")

        assert response.status == 200
        assert await response.json() == {"time": 237}


@pytest.mark.asyncio
async def test_get_timeout():
    with aioresponses() as mock:
        mock.get("http://example.com/api", timeout=True)
        AiohttpClient.get_aiohttp_client()
        response = await AiohttpClient.get("http://example.com/api")

        assert response.status == 408
        assert response.content == {"detail": "Request Timeout"}


@pytest.mark.asyncio
async def test_close_aiohttp_client():
    await AiohttpClient.close_aiohttp_client()
    assert AiohttpClient.aiohttp_client is None


@pytest.mark.asyncio
async def test_get_aiohttp_client():
    AiohttpClient.get_aiohttp_client()
    assert isinstance(AiohttpClient.aiohttp_client, aiohttp.ClientSession)
