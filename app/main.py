import logging
from contextlib import asynccontextmanager
from app.service.redis_service import cache_status

from fastapi import FastAPI, BackgroundTasks

from app.consumer.rabbit_consumer import RabbitClient

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

rabbit_client = RabbitClient()

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logging.info("App starting up...")
        cache_status("inactive")
        yield
    except Exception as e:
        logging.error(f"Error in lifespan startup: {e}")
        raise e
    finally:
        logging.info("App shutting down...")
        cache_status("inactive")

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "🚀 Pay Alert Composite is alive!"}

@app.post("/start_consumer")
async def start_consume(background_tasks: BackgroundTasks):
    if rabbit_client.is_running():
        return {"status": "already consuming"}

    background_tasks.add_task(rabbit_client.start)
    logging.info("🚀 Consumer task started in background")
    return {"status": "consumer started"}

@app.get("/consumer-status")
async def consumer_status():
    return {"running": rabbit_client.is_running()}
