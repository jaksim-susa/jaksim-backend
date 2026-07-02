from datetime import date
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
    createdAt: str


# 목표 조회 Response
class GoalResponse(BaseModel):
    goalId: str
    title: str
    startDate: Optional[str] = None
    endDate: Optional[str] = None
    isActive: bool
    createdAt: str


class GoalListResponse(BaseModel):
    goals: List[GoalResponse]