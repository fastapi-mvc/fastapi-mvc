"""Redis client class utility."""
import logging

import aioredis
import aioredis.sentinel
from aioredis.exceptions import RedisError
from {{cookiecutter.package_name}}.config import redis as redis_conf


class RedisClient(object):
    """Define Redis utility.

    Utility class for handling Redis database connection and operations.

    Attributes:
        redis_client (aioredis.Redis, optional): Redis client object instance.
        log (logging.Logger): Logging handler for this class.
        base_redis_init_kwargs (dict): Common kwargs regardless other Redis
            configuration
        connection_kwargs (dict, optional): Extra kwargs for Redis object init.

    """

    redis_client: aioredis.Redis = None
    log: logging.Logger = logging.getLogger(__name__)
    base_redis_init_kwargs: dict = {
        "encoding": "utf-8",
        "port": redis_conf.REDIS_PORT,
    }
    connection_kwargs: dict = {}

    @classmethod
    def open_redis_client(cls):
        """Create Redis client session object instance.

        Based on configuration create either Redis client or Redis Sentinel.

        Returns:
            aioredis.Redis: Redis object instance.

        """
        if cls.redis_client is None:
            cls.log.debug("Initialize Redis client.")
            if redis_conf.REDIS_USERNAME and redis_conf.REDIS_PASSWORD:
                cls.connection_kwargs = {
                    "username": redis_conf.REDIS_USERNAME,
                    "password": redis_conf.REDIS_PASSWORD,
                }

            if redis_conf.REDIS_USE_SENTINEL:
                sentinel = aioredis.sentinel.Sentinel(
                    [(redis_conf.REDIS_HOST, redis_conf.REDIS_PORT)],
                    sentinel_kwargs=cls.connection_kwargs,
                )
                cls.redis_client = sentinel.master_for("mymaster")
            else:
                cls.base_redis_init_kwargs.update(cls.connection_kwargs)
                cls.redis_client = aioredis.from_url(
                    "redis://{0:s}".format(redis_conf.REDIS_HOST),
                    **cls.base_redis_init_kwargs,
                )

        return cls.redis_client

    @classmethod
    async def close_redis_client(cls):
        """Close Redis client."""
        if cls.redis_client:
            cls.log.debug("Closing Redis client")
            await cls.redis_client.close()

    @classmethod
    async def ping(cls):
        """Execute Redis PING command.

        Ping the Redis server.

        Returns:
            response: Boolean, whether Redis client could ping Redis server.

        Raises:
            aioredis.RedisError: If Redis client failed while executing command.

        """
        # Note: Not sure if this shouldn't be deep copy instead?
        redis_client = cls.redis_client

        cls.log.debug("Preform Redis PING command")
        try:
            return await redis_client.ping()
        except RedisError as ex:
            cls.log.exception(
                "Redis PING command finished with exception",
                exc_info=(type(ex), ex, ex.__traceback__),
            )
            return False

    @classmethod
    async def set(cls, key, value):
        """Execute Redis SET command.

        Set key to hold the string value. If key already holds a value, it is
        overwritten, regardless of its type.

        Args:
            key (str): Redis db key.
            value (str): Value to be set.

        Returns:
            response: Redis SET command response, for more info
                look: https://redis.io/commands/set#return-value

        Raises:
            aioredis.RedisError: If Redis client failed while executing command.

        """
        redis_client = cls.redis_client

        cls.log.debug(
            "Preform Redis SET command, key: {}, value: {}".format(key, value)
        )
        try:
            await redis_client.set(key, value)
        except RedisError as ex:
            cls.log.exception(
                "Redis SET command finished with exception",
                exc_info=(type(ex), ex, ex.__traceback__),
            )
            raise ex

    @classmethod
    async def rpush(cls, key, value):
        """Execute Redis RPUSH command.

        Insert all the specified values at the tail of the list stored at key.
        If key does not exist, it is created as empty list before performing
        the push operation. When key holds a value that is not a list, an
        error is returned.

        Args:
            key (str): Redis db key.
            value (str, list): Single or multiple values to append.

        Returns:
            response: Length of the list after the push operation.

        Raises:
            aioredis.RedisError: If Redis client failed while executing command.

        """
        redis_client = cls.redis_client

        cls.log.debug(
            "Preform Redis RPUSH command, key: {}, value: {}".format(key, value)
        )
        try:
            await redis_client.rpush(key, value)
        except RedisError as ex:
            cls.log.exception(
                "Redis RPUSH command finished with exception",
                exc_info=(type(ex), ex, ex.__traceback__),
            )
            raise ex

    @classmethod
    async def exists(cls, key):
        """Execute Redis EXISTS command.

        Returns if key exists.

        Args:
            key (str): Redis db key.

        Returns:
            response: Boolean whether key exists in Redis db.

        Raises:
            aioredis.RedisError: If Redis client failed while executing command.

        """
        redis_client = cls.redis_client

        cls.log.debug(
            "Preform Redis EXISTS command, key: {}, exists".format(key)
        )
        try:
            return await redis_client.exists(key)
        except RedisError as ex:
            cls.log.exception(
                "Redis EXISTS command finished with exception",
                exc_info=(type(ex), ex, ex.__traceback__),
            )
            raise ex

    @classmethod
    async def get(cls, key):
        """Execute Redis GET command.

        Get the value of key. If the key does not exist the special value None
        is returned. An error is returned if the value stored at key is not a
        string, because GET only handles string values.

        Args:
            key (str): Redis db key.

        Returns:
            response: Value of key.

        Raises:
            aioredis.RedisError: If Redis client failed while executing command.

        """
        redis_client = cls.redis_client

        cls.log.debug("Preform Redis GET command, key: {}".format(key))
        try:
            return await redis_client.get(key)
        except RedisError as ex:
            cls.log.exception(
                "Redis GET command finished with exception",
                exc_info=(type(ex), ex, ex.__traceback__),
            )
            raise ex

    @classmethod
    async def lrange(cls, key, start, end):
        """Execute Redis LRANGE command.

        Returns the specified elements of the list stored at key. The offsets
        start and stop are zero-based indexes, with 0 being the first element
        of the list (the head of the list), 1 being the next element and so on.
        These offsets can also be negative numbers indicating offsets starting
        at the end of the list. For example, -1 is the last element of the
        list, -2 the penultimate, and so on.

        Args:
            key (str): Redis db key.
            start (int): Start offset value.
            end (int): End offset value.

        Returns:
            response: Returns the specified elements of the list stored at key.

        Raises:
            aioredis.RedisError: If Redis client failed while executing command.

        """
        redis_client = cls.redis_client

        cls.log.debug(
            "Preform Redis LRANGE command, key: {}, start: {}, end: {}".format(
                key,
                start,
                end,
            )
        )
        try:
            return await redis_client.lrange(key, start, end)
        except RedisError as ex:
            cls.log.exception(
                "Redis LRANGE command finished with exception",
                exc_info=(type(ex), ex, ex.__traceback__),
            )
            raise ex
