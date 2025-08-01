import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.service.redis_service import cache_status
from app.client.db_client import database

from app.consumer.rabbit_consumer import RabbitClient
from app.routers import consumer_route, dashboard_route

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

rabbit_client = RabbitClient()

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logging.info("Starting lifespan...")
        await rabbit_client.connect()
        logging.info("Connected to RabbitMQ.")
        await database.connect()
        yield
    except Exception as e:
        logging.error(f"Error in lifespan startup: {e}")
        raise e
    finally:
        await database.disconnect()
        logging.info("Database connection closed.")
        await rabbit_client.close()
        cache_status("inactive")
        logging.info("RabbitMQ connection closed.")

app = FastAPI(lifespan=lifespan)
app.include_router(consumer_route.router)
app.include_router(dashboard_route.router)

@app.get("/")
async def root():
    return {"message": "🚀 Pay Alert Composite is alive!"}