from pydantic import BaseModel
from app.constants.response import Responses
from config import SERVICE_NAME

class CommonStatus(BaseModel):
    code: str
    message: str
    namespace: str

    @classmethod
    def from_enum(cls, enum_member: Responses, namespace: str = SERVICE_NAME):
        return cls(
            code=enum_member.code,
            message=enum_member.message,
            namespace=namespace
        )
