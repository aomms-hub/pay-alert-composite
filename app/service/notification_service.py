from typing import Optional
from app.client.websocket_manager import manager
from app.client.amount_tts_service_client import send_amount, TTSResponse
from app.service.transaction_log_service import insert_transaction_log
from app.models.transaction_log import TransactionLogCreate
from pydantic import BaseModel
from datetime import datetime
from zoneinfo import ZoneInfo
from config import TIME_ZONE
import logging
import re
import json


class NotificationRequest(BaseModel):
    message: str
    title: str
    timestamp: str


async def notify(request: NotificationRequest):
    timestamp = datetime.now(ZoneInfo(TIME_ZONE))
    amount = extract_exact_amount(request.message)
    tts_response = await send_amount(amount)
    await notify_new_transaction(
        amount=amount,
        timestamp=timestamp.isoformat(),
        note=None,
        sound_url=tts_response.audio_url,
    )
    await insert_transaction_log(
        build_transaction_log(source=request.title, tts_response=tts_response, timestamp=timestamp))
    logging.info("url response from tts:" + tts_response.audio_url)


async def notify_new_transaction(amount: str, timestamp: str, note: Optional[str], sound_url: str):
    message = json.dumps({
        "amount": amount,
        "timestamp": timestamp,
        "note": note,
        "sound_url": sound_url,
    })
    await manager.broadcast(message)


def extract_exact_amount(message: str) -> str:
    match = re.search(r"\b\d{1,12}\.\d{2}\b", message)
    if match:
        return match.group(0)
    raise ValueError("invalid amount message")


def build_transaction_log(source: str, tts_response: TTSResponse, timestamp: datetime):
    return TransactionLogCreate(
        amount=float(tts_response.amount),
        source=source,
        timestamp=timestamp,
        note=None,
        sound_url=tts_response.audio_url
    )
