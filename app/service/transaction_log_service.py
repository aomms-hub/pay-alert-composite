from app.client.db_client import database
from app.models.transaction_log import TransactionLogCreate
import functools


async def is_database_connected():
    if not database.is_connected:
        await database.connect()

def ensure_db_connection(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        if not database.is_connected:
            await database.connect()
        return await func(*args, **kwargs)
    return wrapper

@ensure_db_connection
async def insert_transaction_log(transaction_log: TransactionLogCreate):
    query = """
    INSERT INTO transaction_log (amount, source, sound_url, note, timestamp)
    VALUES (:amount, :source, :sound_url, :note, :timestamp)
    RETURNING id
    """
    values = {
        "amount": transaction_log.amount,
        "source": transaction_log.source,
        "sound_url": transaction_log.sound_url,
        "note": transaction_log.note,
        "timestamp": transaction_log.timestamp,
    }
    transaction_id = await database.execute(query=query, values=values)
    return transaction_id

@ensure_db_connection
async def get_transaction_log_list(limit: int = 50):
    query = "SELECT * FROM transaction_log ORDER BY timestamp DESC LIMIT :limit"
    return await database.fetch_all(query=query, values={"limit": limit})

@ensure_db_connection
async def get_transaction_log_by_id(transaction_id: int):
    query = "SELECT * FROM transaction_log WHERE transaction_log.id = :transaction_id"
    return await database.fetch_one(query=query, values={"transaction_id": transaction_id})

@ensure_db_connection
async def get_transaction_log_by_amount(amount: float):
    query = "SELECT * FROM transaction_log WHERE transaction_log.amount = :amount ORDER BY timestamp DESC "
    return await database.fetch_all(query=query, values={"amount": amount})

@ensure_db_connection
async def get_total_transaction_amount():
    query = "SELECT SUM(amount) FROM transaction_log"
    result = await database.fetch_one(query)
    return result["sum"]
