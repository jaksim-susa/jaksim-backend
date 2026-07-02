from datetime import date
from beanie import PydanticObjectId
from app.models.goal import Goal
from app.schemas.goal import GoalCreateRequest, GoalCreateResponse


async def create_goal(user_id: str, request: GoalCreateRequest) -> GoalCreateResponse:
    start_date = request.startDate or date.today()

    new_goal = Goal(
        user_id=PydanticObjectId(user_id),
        title=request.title,
        start_date=start_date,
        end_date=request.endDate,
    )

    await new_goal.insert()

    return GoalCreateResponse(
        goalId=str(new_goal.id),
        title=new_goal.title,
        startDate=new_goal.start_date,
        endDate=new_goal.end_date,
        createdAt=new_goal.created_at.isoformat(),
    )