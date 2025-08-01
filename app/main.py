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


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logging.info("App starting up...")
        cache_status("inactive")
        await database.connect()
        yield
    except Exception as e:
        logging.error(f"Error in lifespan startup: {e}")
        raise e
    finally:
        logging.info("App shutting down...")
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


@app.post("/database/disconnect")
async def disconnect_database():
    await database.disconnect()
    return CommonResponse(
        status=CommonStatus.from_enum(Responses.SUCCESS)
    )
