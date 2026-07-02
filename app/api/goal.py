from fastapi import APIRouter, Depends, Response

from app.core.security import get_current_user
from app.schemas.goal import GoalCreateRequest, GoalCreateResponse
from app.services.goal import create_goal


router = APIRouter()


@router.post("/", response_model=GoalCreateResponse)
async def create_goal_route(
    request: GoalCreateRequest,
    current_user=Depends(get_current_user)
):
    return await create_goal(str(current_user.id), request)