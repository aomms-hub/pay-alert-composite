from typing import Generic, TypeVar, Optional
from pydantic import BaseModel
from app.models.common_status import CommonStatus

T = TypeVar("T")

class CommonResponse(BaseModel, Generic[T]):
    status: CommonStatus
    data: Optional[T] = None
