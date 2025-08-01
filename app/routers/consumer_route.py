from fastapi import APIRouter
from app.models.common_response import CommonResponse, CommonStatus
from app.constants.response import Responses
from app.consumer.rabbit_consumer import RabbitClient
import logging

rabbit_client = RabbitClient()
router = APIRouter(prefix="/consumer", tags=["Consumer"])


@router.post("/start")
async def start_consume():
    if rabbit_client.is_running():
        return {"status": "already consuming"}

    await rabbit_client.start()
    logging.info("🚀 Consumer task started in background")
    return CommonResponse(status=CommonStatus.from_enum(Responses.SUCCESS))


@router.get("/status")
async def consumer_status():
    return CommonResponse(
        status=CommonStatus.from_enum(Responses.SUCCESS),
        data={"running": rabbit_client.is_running()}
    )
