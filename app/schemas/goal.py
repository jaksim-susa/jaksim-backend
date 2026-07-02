from datetime import date
from typing import Optional
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