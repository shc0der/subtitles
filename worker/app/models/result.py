
from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel

from app.models.status import Status

Data = TypeVar("Data", bound=Any)


class Result(BaseModel, Generic[Data]):
    data: Optional[Data] = None
    message: Optional[str] = None
    status: Status = Status.success

    def is_successful(self) -> bool:
        return self.status == Status.success

    @classmethod
    def failure(cls, message: str) -> 'Result':
        return cls(message=message, status=Status.error)

    @classmethod
    def success(cls, data: Optional[Data]) -> 'Result':
        return cls(data=data, status=Status.success)
