from pydantic import BaseModel

from app.client.amount_tts_service_client import send_amount


async def notify(message: dict):
    tts_response = await send_amount(message['amount'])
    print(tts_response)
