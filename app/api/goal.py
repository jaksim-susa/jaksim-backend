from fastapi import APIRouter, Depends, Response

from app.core.security import get_current_user
from app.models.user import User
from app.schemas.base import MessageResponse
from app.schemas.goal import GoalCreateRequest, GoalCreateResponse, GoalListResponse, GoalResponse, GoalUpdateRequest
from app.services.goal import create_goal, delete_goal, get_goals, update_goal


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


@router.put("/{goal_id}", response_model=GoalResponse)
async def update_goal_route(
    goal_id: str,
    request: GoalUpdateRequest,
    current_user: User = Depends(get_current_user)
):
    return await update_goal(str(current_user.id), goal_id, request)


@router.delete("/{goal_id}", response_model=MessageResponse)
async def delete_goal_route(
    goal_id: str,
    current_user: User = Depends(get_current_user)
):
    return await delete_goal(str(current_user.id), goal_id)