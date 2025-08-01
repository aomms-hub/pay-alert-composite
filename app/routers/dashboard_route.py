from fastapi import APIRouter
from app.service import transaction_log_service
from typing import List
from app.models.transaction_log import TransactionLog, TransactionLogCreate
from app.models.common_response import CommonResponse, CommonStatus
from app.constants.response import Responses

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/transaction_log_by_id", response_model=CommonResponse[TransactionLog])
async def get_transaction_log_by_id(transaction_id: int):
    return CommonResponse(
        status=CommonStatus.from_enum(Responses.SUCCESS),
        data=await transaction_log_service.get_transaction_log_by_id(transaction_id)
    )


@router.get("/transaction_log_list", response_model=CommonResponse[List[TransactionLog]])
async def get_transaction_log_list():
    return CommonResponse(
        status=CommonStatus.from_enum(Responses.SUCCESS),
        data=await transaction_log_service.get_transaction_log_list()
    )


@router.get("/transaction_log_by_amount", response_model=CommonResponse[List[TransactionLog]])
async def get_transaction_log_by_amount(amount: float):
    return CommonResponse(
        status=CommonStatus.from_enum(Responses.SUCCESS),
        data=await transaction_log_service.get_transaction_log_by_amount(amount)
    )

@router.post("/transaction_log", response_model=CommonResponse[int])
async def insert_transaction_log(log: TransactionLogCreate):
    return CommonResponse(
        status=CommonStatus.from_enum(Responses.SUCCESS),
        data=await transaction_log_service.insert_transaction_log(log)
    )

@router.get("/transaction_log_summarize", response_model=CommonResponse[float])
async def get_sum_transaction_log():
    return CommonResponse(
        status=CommonStatus.from_enum(Responses.SUCCESS),
        data=await transaction_log_service.get_total_transaction_amount()
    )
