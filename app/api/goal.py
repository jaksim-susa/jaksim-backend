from fastapi import APIRouter, Depends, Response

from app.core.security import get_current_user
from app.models.user import User
from app.schemas.goal import GoalCreateRequest, GoalCreateResponse, GoalListResponse
from app.services.goal import create_goal, get_goals


router = APIRouter()


@router.post("", response_model=GoalCreateResponse)
async def create_goal_route(
    request: GoalCreateRequest,
    current_user: User = Depends(get_current_user)
):
    return await create_goal(str(current_user.id), request)


@router.get("/me", response_model=GoalListResponse)
async def get_goals_route(
    current_user: User = Depends(get_current_user)
):
    return await get_goals(str(current_user.id))