from app.client.db_client import database
from app.models.transaction_log import TransactionLog

async def save_transaction(tx: TransactionLog):
    query = """
    INSERT INTO transaction_log (amount, source, sound_url, note, timestamp)
    VALUES (:amount, :source, :sound_url, :note, :timestamp)
    RETURNING id;
    """
    values = tx.dict(exclude={"id"})
    transaction_id = await database.execute(query=query, values=values)
    return transaction_id

async def get_transaction_log_list(limit: int = 50):
    query = "SELECT * FROM transaction_log ORDER BY timestamp DESC LIMIT :limit"
    return await database.fetch_all(query=query, values={"limit": limit})
