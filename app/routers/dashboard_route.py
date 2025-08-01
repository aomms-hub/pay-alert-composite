from fastapi import APIRouter
from app.service.transaction_log_service import get_transaction_log_list
from typing import List
from app.models.transaction_log import TransactionLog

router = APIRouter(prefix="/dashboard")

@router.get("/transaction_log_list", response_model=List[TransactionLog])
async def list_transactions():
    return await get_transaction_log_list()
