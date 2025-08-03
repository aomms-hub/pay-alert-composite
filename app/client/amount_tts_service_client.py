import httpx
import logging
from config import GENERATE_AMOUNT_TTS_PATH, AMOUNT_TTS_SERVICE_URL
from pydantic import BaseModel

class TTSResponse(BaseModel):
    from_cache: bool
    amount: str
    audio_url: str

async def send_amount(amount: str) -> TTSResponse:
    url = f"{AMOUNT_TTS_SERVICE_URL}{GENERATE_AMOUNT_TTS_PATH}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params={"amount": amount})
            response.raise_for_status()
        logging.info(f"✅ Sent amount to TTS service: {response.status_code}")
        return TTSResponse(**response.json())
    except Exception as e:
        logging.error(f"❌ Failed to send amount to TTS service: {e}")
        raise
