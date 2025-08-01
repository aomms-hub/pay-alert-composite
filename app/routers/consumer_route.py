from fastapi import APIRouter, BackgroundTasks
from app.consumer.rabbit_consumer import RabbitClient
import logging

rabbit_client = RabbitClient()
router = APIRouter(prefix="/consumer")


@router.post("/start")
async def start_consume(background_tasks: BackgroundTasks):
    if rabbit_client.is_running():
        return {"status": "already consuming"}

    background_tasks.add_task(rabbit_client.start)
    logging.info("🚀 Consumer task started in background")
    return {"status": "consumer started"}


@router.get("/status")
async def consumer_status():
    return {"running": rabbit_client.is_running()}
