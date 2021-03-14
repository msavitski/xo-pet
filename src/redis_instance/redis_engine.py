import os
import logging
import redis

logger = logging.getLogger(__name__)


def load_redis_driver():
    """
    Loads redis driver object using environment variables
    Returns
    -------
    RedisDriver - driver for redis image data cache
    """
    redis_url = os.environ.get("REDIS_URL", "redis")
    redis_port = int(os.environ.get("REDIS_PORT", "6379"))
    redis_pass = os.environ["REDIS_PASS"]
    return RedisDriver(redis_url, redis_port, redis_pass)


class RedisDriver:
    """
    Driver for game moving cache
    """

    def __init__(self, host, port, password, db=0):
        """
        Parameters
        ----------
        host (str) - redis service host
        port (int) - redis service port
        password (str) - password for redis
        db (int) - int, determining redis db (from 0 to 15)
        """
        self.connector = redis.Redis(host=host, port=port, password=password, db=db)
        self.default_expiration_s = 3600
