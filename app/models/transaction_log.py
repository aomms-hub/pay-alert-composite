from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TransactionLog(BaseModel):
    id: int
    amount: float
    source: str
    sound_url: Optional[str]
    note: Optional[str]
    timestamp: datetime