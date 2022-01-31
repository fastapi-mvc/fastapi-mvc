import pytest
import aiohttp
from aioresponses import aioresponses
from {{cookiecutter.package_name}}.app.utils import AiohttpClient


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "status, headers, raise_for_status",
    [
        (200, None, True),
        (201, {"foo": "bar"}, False),
        (404, None, False),
        (500, {"API": "KEY"}, False),
    ],
)
async def test_get(status, headers, raise_for_status):
    with aioresponses() as mock:
        mock.get(
            "http://example.com/api",
            status=status,
            payload=dict(master="exploder"),
        )
        AiohttpClient.get_aiohttp_client()
        response = await AiohttpClient.get(
            "http://example.com/api",
            headers=headers,
            raise_for_status=raise_for_status,
        )

        assert response.status == status
        assert await response.json() == {"master": "exploder"}
        if headers:
            assert response.request_info.headers == headers


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "status, headers",
    [
        (404, None),
        (500, {"API": "KEY"}),
    ],
)
async def test_get_with_raise(status, headers):
    with aioresponses() as mock:
        mock.get(
            "http://example.com/api",
            status=status,
            payload=dict(master="exploder"),
        )
        AiohttpClient.get_aiohttp_client()
        with pytest.raises(aiohttp.ClientError):
            await AiohttpClient.get(
                "http://example.com/api",
                headers=headers,
                raise_for_status=True,
            )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "status, headers, raise_for_status",
    [
        (200, None, True),
        (201, {"foo": "bar"}, True),
        (404, None, False),
        (500, {"API": "KEY"}, False),
    ],
)
async def test_delete(status, headers, raise_for_status):
    with aioresponses() as mock:
        mock.delete(
            "http://example.com/api",
            status=status,
            payload=dict(master="exploder"),
        )
        AiohttpClient.get_aiohttp_client()
        response = await AiohttpClient.delete(
            "http://example.com/api",
            headers=headers,
            raise_for_status=raise_for_status,
        )

        assert response.status == status
        assert await response.json() == {"master": "exploder"}
        if headers:
            assert response.request_info.headers == headers


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "status, headers",
    [
        (404, None),
        (500, {"API": "KEY"}),
    ],
)
async def test_delete_with_raise(status, headers):
    with aioresponses() as mock:
        mock.delete(
            "http://example.com/api",
            status=status,
            payload=dict(master="exploder"),
        )
        AiohttpClient.get_aiohttp_client()
        with pytest.raises(aiohttp.ClientError):
            await AiohttpClient.delete(
                "http://example.com/api",
                headers=headers,
                raise_for_status=True,
            )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "status, data, headers, raise_for_status",
    [
        (200, None, None, True),
        (201, {1: 2}, {"foo": "bar"}, True),
        (404, "payload", None, False),
        (500, None, {"API": "KEY"}, False),
    ],
)
async def test_post(status, data, headers, raise_for_status):
    with aioresponses() as mock:
        mock.post(
            "http://example.com/api",
            status=status,
            payload=dict(master="exploder"),
        )
        AiohttpClient.get_aiohttp_client()
        response = await AiohttpClient.post(
            "http://example.com/api",
            data=data,
            headers=headers,
            raise_for_status=raise_for_status,
        )

        assert response.status == status
        assert await response.json() == {"master": "exploder"}
        if headers:
            assert response.request_info.headers == headers


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "status, data, headers",
    [
        (404, "payload", None),
        (500, None, {"API": "KEY"}),
    ],
)
async def test_post_with_raise(status, data, headers):
    with aioresponses() as mock:
        mock.post(
            "http://example.com/api",
            status=status,
            payload=dict(master="exploder"),
        )
        AiohttpClient.get_aiohttp_client()
        with pytest.raises(aiohttp.ClientError):
            await AiohttpClient.post(
                "http://example.com/api",
                data=data,
                headers=headers,
                raise_for_status=True,
            )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "status, data, headers, raise_for_status",
    [
        (200, None, None, True),
        (201, {1: 2}, {"foo": "bar"}, True),
        (404, "payload", None, False),
        (500, None, {"API": "KEY"}, False),
    ],
)
async def test_put(status, data, headers, raise_for_status):
    with aioresponses() as mock:
        mock.put(
            "http://example.com/api",
            status=status,
            payload=dict(master="exploder"),
        )
        AiohttpClient.get_aiohttp_client()
        response = await AiohttpClient.put(
            "http://example.com/api",
            data=data,
            headers=headers,
            raise_for_status=raise_for_status,
        )

        assert response.status == status
        assert await response.json() == {"master": "exploder"}
        if headers:
            assert response.request_info.headers == headers


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "status, data, headers",
    [
        (404, "payload", None),
        (500, None, {"API": "KEY"}),
    ],
)
async def test_put_with_raise(status, data, headers):
    with aioresponses() as mock:
        mock.put(
            "http://example.com/api",
            status=status,
            payload=dict(master="exploder"),
        )
        AiohttpClient.get_aiohttp_client()
        with pytest.raises(aiohttp.ClientError):
            await AiohttpClient.put(
                "http://example.com/api",
                data=data,
                headers=headers,
                raise_for_status=True,
            )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "status, data, headers, raise_for_status",
    [
        (200, None, None, True),
        (201, {1: 2}, {"foo": "bar"}, True),
        (404, "payload", None, False),
        (500, None, {"API": "KEY"}, False),
    ],
)
async def test_patch(status, data, headers, raise_for_status):
    with aioresponses() as mock:
        mock.patch(
            "http://example.com/api",
            status=status,
            payload=dict(master="exploder"),
        )
        AiohttpClient.get_aiohttp_client()
        response = await AiohttpClient.patch(
            "http://example.com/api",
            data=data,
            headers=headers,
            raise_for_status=raise_for_status,
        )

        assert response.status == status
        assert await response.json() == {"master": "exploder"}
        if headers:
            assert response.request_info.headers == headers


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "status, data, headers",
    [
        (404, "payload", None),
        (500, None, {"API": "KEY"}),
    ],
)
async def test_patch_with_raise(status, data, headers):
    with aioresponses() as mock:
        mock.patch(
            "http://example.com/api",
            status=status,
            payload=dict(master="exploder"),
        )
        AiohttpClient.get_aiohttp_client()
        with pytest.raises(aiohttp.ClientError):
            await AiohttpClient.patch(
                "http://example.com/api",
                data=data,
                headers=headers,
                raise_for_status=True,
            )


@pytest.mark.asyncio
async def test_close_aiohttp_client():
    await AiohttpClient.close_aiohttp_client()
    assert AiohttpClient.aiohttp_client is None


@pytest.mark.asyncio
async def test_get_aiohttp_client():
    AiohttpClient.get_aiohttp_client()
    assert isinstance(AiohttpClient.aiohttp_client, aiohttp.ClientSession)
