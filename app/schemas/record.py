from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel

from app.schemas.diary import DiaryResponse


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


class RecordResponse(BaseModel):
    recordId: Optional[str] = None    
    goalId: str                           
    goal: str
    status: Optional[str] = None       
    reasonCategory: Optional[str] = None
    reasonText: Optional[str] = None
    recordDate: date


class RecordListResponse(BaseModel):
    records: List[RecordResponse]
    diary: Optional[DiaryResponse] = None


class RecordListGoalResponse(BaseModel):
    goalId: str
    recordId: Optional[str] = None
    goal: str
    status: Optional[str] = None
    reasonCategory: Optional[str] = None


class RecordListDayResponse(BaseModel):
    date: date
    diary: Optional[str] = None
    goals: List[RecordListGoalResponse]


class RecordAllListResponse(BaseModel):
    records: List[RecordListDayResponse]


class RecordUpdateRequest(BaseModel):
    status: str
    reasonText: Optional[str] = None


class RecordUpdateResponse(BaseModel):
    recordId: str
    goalId: str
    status: str
    reasonText: Optional[str] = None
    reasonCategory: Optional[str] = None
    recordDate: date
    createdAt: datetime