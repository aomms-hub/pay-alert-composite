from enum import Enum

class Responses(Enum):
    SUCCESS = ("200-000", "SUCCESS")
    NOT_FOUND = ("404-001", "RESOURCE NOT FOUND")
    INTERNAL_ERROR = ("500-000", "INTERNAL SERVER ERROR")

    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message