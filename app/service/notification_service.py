from app.client.amount_tts_service_client import send_amount, TTSResponse
from app.service.transaction_log_service import insert_transaction_log
from app.models.transaction_log import TransactionLogCreate


async def notify(message: dict):
    print("message:" + message.get("amount"))
    tts_response = await send_amount(message.get("amount"))
    await insert_transaction_log(build_transaction_log(message, tts_response))
    print(tts_response)


def build_transaction_log(message: dict, tts_response: TTSResponse):
    print(message)
    return TransactionLogCreate(
        amount=float(message.get("amount")),
        source=message.get("source"),
        timestamp=message.get("timestamp"),
        note=None,
        sound_url=tts_response.audio_url
    )
