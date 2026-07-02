from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel


# 기록 생성 Request
class RecordCreateRequest(BaseModel):
    goalId: str
    status: str                          # success / fail
    reasonText: Optional[str] = None


# 기록 생성 Response
class RecordCreateResponse(BaseModel):
    recordId: str
    goalId: str
    status: str
    reasonText: Optional[str] = None
    reasonCategory: Optional[str] = None
    recordDate: date
    createdAt: datetime