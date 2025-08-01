import aio_pika
import asyncio
import json
import time
from config import RABBITMQ_URL, EXCHANGE_NAME, ROUTING_KEY, QUEUE_NAME
from app.service.notification_service import notify
from app.service.redis_service import cache_status

class RabbitClient:
    def __init__(self, url: str = RABBITMQ_URL, idle_timeout=300):
        self.url = url
        self.connection = None
        self.channel = None
        self.exchange = None
        self.queue = None
        self.consumer_tag = None
        self.idle_timeout = idle_timeout
        self.idle_task = None
        self.last_activity = time.time()
        self.running = False

    async def connect(self):
        if self.connection and not self.connection.is_closed:
            return
        self.connection = await aio_pika.connect_robust(self.url)
        self.channel = await self.connection.channel()
        self.exchange = await self.channel.declare_exchange(
            EXCHANGE_NAME, aio_pika.ExchangeType.DIRECT, durable=True
        )
        self.queue = await self.channel.declare_queue(QUEUE_NAME, durable=True)
        await self.queue.bind(self.exchange, routing_key=ROUTING_KEY)

    async def on_message(self, message: aio_pika.IncomingMessage):
        async with message.process():
            self.last_activity = time.time()
            data = json.loads(message.body.decode())
            print(f"📢 Received message: {data}")
            await notify(data)

    async def start(self):
        if self.running:
            print("⚠️ Already consuming.")
            return

        await self.connect()
        self.running = True
        self.last_activity = time.time()
        self.consumer_tag = await self.queue.consume(self.on_message)
        cache_status("active")
        print("🚀 Start consuming messages...")

        self.idle_task = asyncio.create_task(self._idle_watcher())

    async def _idle_watcher(self):
        try:
            while self.running:
                await asyncio.sleep(10)
                if time.time() - self.last_activity > self.idle_timeout:
                    print(f"😴 Idle timeout {self.idle_timeout}s reached. Closing connection...")
                    await self.close()
        except asyncio.CancelledError:
            pass

    def is_running(self):
        return self.running

    async def close(self):
        if self.running:
            self.running = False
            if self.consumer_tag and self.queue:
                await self.queue.cancel(self.consumer_tag)
                self.consumer_tag = None
            if self.connection and not self.connection.is_closed:
                await self.connection.close()
            if self.idle_task:
                self.idle_task.cancel()
                self.idle_task = None
            print("🔌 RabbitMQ connection closed.")
            self.connection = None
            self.channel = None
            self.exchange = None
            self.queue = None
            cache_status("inactive")
