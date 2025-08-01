from app.client.redis_client import redis_client
from config import SERVICE_NAME, TIME_ZONE
from datetime import datetime
from zoneinfo import ZoneInfo
import json

ttl_seconds = 10 * 60
CONSUMER_STATUS_REDIS_KEY = "consumer:status:"

def cache_status(status: str):
    key = f"{CONSUMER_STATUS_REDIS_KEY}{SERVICE_NAME}"
    message = build_status_message(status)
    redis_client.set(key, json.dumps(message), ex=ttl_seconds)


def build_status_message(status: str) -> dict:
    return {
        "status": status,
        "timestamp": datetime.now(ZoneInfo(TIME_ZONE)).isoformat()
    }