import os
from dotenv import load_dotenv

load_dotenv()

SERVICE_NAME = "pay-alert-composite"
TIME_ZONE = "Asia/Bangkok"

RABBITMQ_URL = os.getenv("RABBITMQ_URL")
REDIS_URL = os.getenv("UPSTASH_REDIS_REST_URL")
DATABASE_URL = os.getenv("POSTGRESQL_URL")

EXCHANGE_NAME = "notification.queue.amount"
ROUTING_KEY = "notify.amount.parsed"
QUEUE_NAME = "noti.amount.in.composite"
# AMOUNT_TTS_SERVICE_URL = "https://amount-tts-service.railway.internal"
AMOUNT_TTS_SERVICE_URL = "https://amount-tts-service-production.up.railway.app"
GENERATE_AMOUNT_TTS_PATH = "/generate_voice"
