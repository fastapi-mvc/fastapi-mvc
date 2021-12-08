import mock
import pytest
from aioredis import Redis
from fastapi_mvc_template.app.utils import RedisClient


# monkey patch for allowing MagicMock to be used with await
# https://stackoverflow.com/a/51399767/10566747
async def async_magic():
    pass

mock.MagicMock.__await__ = lambda x: async_magic().__await__()


def test_open_redis_client():
    RedisClient.open_redis_client()
    assert isinstance(RedisClient.redis_client, Redis)


@pytest.mark.asyncio
async def test_ping():
    RedisClient.redis_client = mock.MagicMock()
    await RedisClient.ping()
    RedisClient.redis_client.ping.assert_called_once()


@pytest.mark.asyncio
async def test_set():
    RedisClient.redis_client = mock.MagicMock()
    await RedisClient.set("key", "value")
    RedisClient.redis_client.set.assert_called_once_with("key", "value")


@pytest.mark.asyncio
async def test_rpush():
    RedisClient.redis_client = mock.MagicMock()
    await RedisClient.rpush("key", "value")
    RedisClient.redis_client.rpush.assert_called_once_with("key", "value")


@pytest.mark.asyncio
async def test_exists():
    RedisClient.redis_client = mock.MagicMock()
    await RedisClient.exists("key")
    RedisClient.redis_client.exists.assert_called_once_with("key")


@pytest.mark.asyncio
async def test_get():
    RedisClient.redis_client = mock.MagicMock()
    await RedisClient.get("key")
    RedisClient.redis_client.get.assert_called_once_with("key")


@pytest.mark.asyncio
async def test_lrange():
    RedisClient.redis_client = mock.MagicMock()
    await RedisClient.lrange("key", 1, -1)
    RedisClient.redis_client.lrange.assert_called_once_with("key", 1, -1)
