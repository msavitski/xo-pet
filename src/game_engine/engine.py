import logging
from redis_instance import load_redis_driver

logger = logging.getLogger(__name__)


class GameEngine:
    def __init__(self):
        redis_driver = load_redis_driver()