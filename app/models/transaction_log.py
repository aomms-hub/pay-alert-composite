from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TransactionLogCreate(BaseModel):
    amount: float
    source: str
    sound_url: Optional[str] = None
    note: Optional[str] = None
    timestamp: datetime

class TransactionLog(TransactionLogCreate):
    id: int
