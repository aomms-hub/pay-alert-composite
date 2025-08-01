from fastapi import APIRouter
from app.service import transaction_log_service
from typing import List
from app.models.transaction_log import TransactionLog, TransactionLogCreate

router = APIRouter(prefix="/dashboard")


@router.get("/transaction_log_by_id", response_model=TransactionLog)
async def get_transaction_log_by_id(transaction_id: int):
    return await transaction_log_service.get_transaction_log_by_id(transaction_id)


@router.get("/transaction_log_list", response_model=List[TransactionLog])
async def get_transaction_log_list():
    return await transaction_log_service.get_transaction_log_list()


@router.get("/transaction_log_by_amount", response_model=List[TransactionLog])
async def get_transaction_log_by_amount(amount: float):
    return await transaction_log_service.get_transaction_log_by_amount(amount)


@router.post("/transaction_log", response_model=TransactionLog)
async def insert_transaction_log(log: TransactionLogCreate):
    id = await transaction_log_service.insert_transaction_log(log)
    return id


@router.get("/transaction_log_summarize")
async def get_sum_transaction_log():
    total = await transaction_log_service.get_total_transaction_amount()
    return {"total_amount": total}
