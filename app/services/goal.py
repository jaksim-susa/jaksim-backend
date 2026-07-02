from datetime import date
from beanie import PydanticObjectId
from app.models.goal import Goal
from app.schemas.goal import GoalCreateRequest, GoalCreateResponse, GoalListResponse, GoalResponse
from app.utils.date import to_kst


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
        createdAt=to_kst(new_goal.created_at),
    )


def calculate_is_active(goal: Goal) -> bool:
    return calculate_is_active_on_date(goal, date.today())


def calculate_is_active_on_date(goal: Goal, target_date: date) -> bool:
    # 시작 날짜 없으면 생성일 기준
    start = goal.start_date if goal.start_date else goal.created_at.date()

    # 시작 전
    if start > target_date:
        return False

    # end_date 없으면 무기한 진행중
    if not goal.end_date:
        return True

    # end_date 있으면 해당 날짜랑 비교
    end = goal.end_date if isinstance(goal.end_date, date) else goal.end_date.date()
    return end >= target_date


async def get_goals(user_id: str) -> GoalListResponse:
    goals = await Goal.find(Goal.user_id == PydanticObjectId(user_id)).to_list()

    return GoalListResponse(
        goals=[
            GoalResponse(
                goalId=str(goal.id),
                title=goal.title,
                startDate=goal.start_date.isoformat() if goal.start_date else None,
                endDate=goal.end_date.isoformat() if goal.end_date else None,
                isActive=calculate_is_active(goal),
                createdAt=to_kst(goal.created_at),
            )

            for goal in goals
        ]
    )