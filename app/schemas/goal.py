from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel


# 목표 생성 Request
class GoalCreateRequest(BaseModel):
    title: str
    startDate: Optional[date] = None
    endDate: Optional[date] = None


# 목표 생성 Response
class GoalCreateResponse(BaseModel):
    goalId: str
    title: str
    startDate: Optional[date] = None
    endDate: Optional[date] = None
    createdAt: datetime


# 목표 조회 Response
class GoalResponse(BaseModel):
    goalId: str
    title: str
    startDate: Optional[date] = None
    endDate: Optional[date] = None
    isActive: bool
    createdAt: datetime


class GoalListResponse(BaseModel):
    goals: List[GoalResponse]


# 목표 수정 Request
class GoalUpdateRequest(BaseModel):
    title: str
    startDate: Optional[date] = None
    endDate: Optional[date] = None