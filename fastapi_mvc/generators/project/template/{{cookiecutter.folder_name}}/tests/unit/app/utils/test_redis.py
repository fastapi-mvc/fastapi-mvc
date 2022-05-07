import mock
import pytest
from aioredis import Redis
from aioredis.exceptions import RedisError
from {{cookiecutter.package_name}}.app.utils import RedisClient
from {{cookiecutter.package_name}}.config import redis as redis_conf


# monkey patch for allowing MagicMock to be used with await
# https://stackoverflow.com/a/51399767/10566747
async def async_magic():
    pass


mock.MagicMock.__await__ = lambda x: async_magic().__await__()


def test_open_redis_client():
    RedisClient.open_redis_client()
    assert isinstance(RedisClient.redis_client, Redis)
    RedisClient.redis_client = None

    redis_conf.REDIS_USERNAME = "John"
    redis_conf.REDIS_PASSWORD = "Secret"
    redis_conf.REDIS_USE_SENTINEL = True
    RedisClient.open_redis_client()
    assert isinstance(RedisClient.redis_client, Redis)
    RedisClient.redis_client = None


@pytest.mark.asyncio
async def test_ping():
    RedisClient.redis_client = mock.MagicMock()
    await RedisClient.ping()
    RedisClient.redis_client.ping.assert_called_once()


@pytest.mark.asyncio
async def test_ping_exception():
    RedisClient.redis_client = mock.MagicMock()
    RedisClient.redis_client.ping.side_effect = RedisError("Mock error")
    assert await RedisClient.ping() is False


@pytest.mark.asyncio
async def test_set():
    RedisClient.redis_client = mock.MagicMock()
    await RedisClient.set("key", "value")
    RedisClient.redis_client.set.assert_called_once_with("key", "value")


@pytest.mark.asyncio
async def test_set_exception():
    RedisClient.redis_client = mock.MagicMock()
    RedisClient.redis_client.set.side_effect = RedisError("Mock error")
    with pytest.raises(RedisError):
        await RedisClient.set("key", "value")


@pytest.mark.asyncio
async def test_rpush():
    RedisClient.redis_client = mock.MagicMock()
    await RedisClient.rpush("key", "value")
    RedisClient.redis_client.rpush.assert_called_once_with("key", "value")


@pytest.mark.asyncio
async def test_rpush_exception():
    RedisClient.redis_client = mock.MagicMock()
    RedisClient.redis_client.rpush.side_effect = RedisError("Mock error")
    with pytest.raises(RedisError):
        await RedisClient.rpush("key", "value")


@pytest.mark.asyncio
async def test_exists():
    RedisClient.redis_client = mock.MagicMock()
    await RedisClient.exists("key")
    RedisClient.redis_client.exists.assert_called_once_with("key")


@pytest.mark.asyncio
async def test_exists_exception():
    RedisClient.redis_client = mock.MagicMock()
    RedisClient.redis_client.exists.side_effect = RedisError("Mock error")
    with pytest.raises(RedisError):
        await RedisClient.exists("key")


@pytest.mark.asyncio
async def test_get():
    RedisClient.redis_client = mock.MagicMock()
    await RedisClient.get("key")
    RedisClient.redis_client.get.assert_called_once_with("key")


@pytest.mark.asyncio
async def test_get_exception():
    RedisClient.redis_client = mock.MagicMock()
    RedisClient.redis_client.get.side_effect = RedisError("Mock error")
    with pytest.raises(RedisError):
        await RedisClient.get("key")


@pytest.mark.asyncio
async def test_lrange():
    RedisClient.redis_client = mock.MagicMock()
    await RedisClient.lrange("key", 1, -1)
    RedisClient.redis_client.lrange.assert_called_once_with("key", 1, -1)


@pytest.mark.asyncio
async def test_lrange_exception():
    RedisClient.redis_client = mock.MagicMock()
    RedisClient.redis_client.lrange.side_effect = RedisError("Mock error")
    with pytest.raises(RedisError):
        await RedisClient.lrange("key", 1, -1)
