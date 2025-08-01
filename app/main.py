import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.service.redis_service import cache_status
from app.client.db_client import database
from app.models.common_response import CommonResponse, CommonStatus
from app.constants.response import Responses
from app.consumer.rabbit_consumer import RabbitClient
from app.routers import consumer_route, dashboard_route

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

rabbit_client = RabbitClient()
is_sleeping = False

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Starting app...")
    await database.connect()
    await rabbit_client.start()
    yield
    logging.info("Shutting down app...")
    await database.disconnect()
    await rabbit_client.close()


app = FastAPI(lifespan=lifespan)
app.include_router(consumer_route.router)
app.include_router(dashboard_route.router)


@app.get("/")
async def root():
    return CommonResponse(
        status=CommonStatus.from_enum(Responses.SUCCESS),
        data="🚀 Pay Alert Composite is alive!"
    )

@app.post("/service/sleep")
async def sleep_service():
    global is_sleeping
    await database.disconnect()
    is_sleeping = True
    return {"status": "service sleeping"}

@app.get("/service/status")
async def get_status():
    return {"sleeping": is_sleeping}