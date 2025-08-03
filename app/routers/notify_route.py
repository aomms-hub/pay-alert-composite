import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.models.common_response import CommonResponse, CommonStatus
from app.constants.response import Responses
from app.service.notification_service import notify
from pydantic import BaseModel
from app.client.websocket_manager import manager

router = APIRouter(prefix="/notification", tags=["notification"])

class NotificationRequest(BaseModel):
    message: str
    title: str
    timestamp: str


@router.post("/")
async def notification(request: NotificationRequest):
    logging.info("incoming request /notify:" + str(request))
    return CommonResponse(
        status=CommonStatus.from_enum(Responses.SUCCESS),
        data=await notify(request)
    )

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
