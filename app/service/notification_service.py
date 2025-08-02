from app.client.amount_tts_service_client import send_amount
from app.service.transaction_log_service import insert_transaction_log
from app.models.transaction_log import TransactionLogCreate


async def notify(message: dict):
    tts_response = await send_amount(message['amount'])
    transaction_log = TransactionLogCreate(
        amount=message['amount'],
        source=message['source'],
        timestamp=message['timestamp'],
        note=None,
        sound_url=tts_response.audio_url
    )
    await insert_transaction_log(transaction_log)
    print(tts_response)
