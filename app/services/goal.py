from datetime import date, datetime, timezone
from beanie import PydanticObjectId
from fastapi import HTTPException, status
from app.models.goal import Goal
from app.models.record import Record
from app.schemas.base import MessageResponse
from app.schemas.goal import GoalCreateRequest, GoalCreateResponse, GoalListResponse, GoalResponse, GoalUpdateRequest
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


async def update_goal(user_id: str, goal_id: str, request: GoalUpdateRequest) -> GoalResponse:
    # 1. 목표 존재 여부 확인
    goal = await Goal.get(PydanticObjectId(goal_id))
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="목표를 찾을 수 없어요."
        )

    # 2. 본인 목표인지 확인
    if str(goal.user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="본인 목표만 수정할 수 있어요."
        )

    # 3. 목표 업데이트
    await goal.update({
        "$set": {
            "title": request.title,
            "start_date": request.startDate,
            "end_date": request.endDate,
            "updated_at": datetime.now(timezone.utc)
        }
    })

    return GoalResponse(
        goalId=str(goal.id),
        title=request.title,
        startDate=request.startDate,
        endDate=request.endDate,
        isActive=calculate_is_active(goal),
        createdAt=to_kst(goal.created_at),
    )


async def delete_goal(user_id: str, goal_id: str) -> MessageResponse:
    # 1. 목표 존재 여부 확인
    goal = await Goal.get(PydanticObjectId(goal_id))
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="목표를 찾을 수 없어요."
        )

    # 2. 본인 목표인지 확인
    if str(goal.user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="본인 목표만 삭제할 수 있어요."
        )

    # 3. 관련 기록 전체 삭제
    await Record.find(
        Record.goal_id == PydanticObjectId(goal_id)
    ).delete()

    # 4. 목표 삭제
    await goal.delete()

    return MessageResponse(message="목표가 삭제되었어요.")