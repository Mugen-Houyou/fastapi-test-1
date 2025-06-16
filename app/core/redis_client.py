import redis.asyncio as redis
from app.core.config import settings

redis_client = redis.from_url(
    settings.REDIS_URL,
    password=settings.REDIS_AUTH_PASSWORD,
    decode_responses=True
)
