from datetime import datetime, timezone, date
from beanie import PydanticObjectId
from fastapi import HTTPException, status
from app.models.record import Record
from app.models.goal import Goal
from app.schemas.record import RecordCreateRequest, RecordCreateResponse
from app.utils.date import to_kst


async def create_record(user_id: str, request: RecordCreateRequest) -> RecordCreateResponse:
    # 1. 목표 존재 여부 확인
    goal = await Goal.get(PydanticObjectId(request.goalId))
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="설정된 목표가 없어요."
        )

    # 2. 오늘 기록 중복 확인
    today = date.today()
    existing_record = await Record.find_one(
        Record.user_id == PydanticObjectId(user_id),
        Record.goal_id == PydanticObjectId(request.goalId),
        Record.record_date == today
    )
    if existing_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="오늘 기록이 이미 존재해요."
        )

    # 3. AI 분류 (status가 fail이면)
    reason_category = None
    if request.status == "fail" and request.reasonText:
        reason_category = await classify_reason(request.reasonText)

    # 4. day_of_week, hour_logged 자동 계산
    now_kst = to_kst(datetime.now(timezone.utc))
    day_of_week = now_kst.weekday()   # KST 기준 요일
    hour_logged = now_kst.hour        # KST 기준 시간
    
    # 5. 기록 저장
    new_record = Record(
        user_id=PydanticObjectId(user_id),
        goal_id=PydanticObjectId(request.goalId),
        record_date=today,
        status=request.status,
        reason_text=request.reasonText,
        reason_category=reason_category,
        day_of_week=day_of_week,
        hour_logged=hour_logged,
    )
    await new_record.insert()

    return RecordCreateResponse(
        recordId=str(new_record.id),
        goalId=str(new_record.goal_id),
        status=new_record.status,
        reasonText=new_record.reason_text,
        reasonCategory=new_record.reason_category,
        recordDate=new_record.record_date,
        createdAt=to_kst(new_record.created_at),
    )


async def classify_reason(reason_text: str) -> str:
    # TODO제미나이 API 호출 (나중에 구현)
    return "미분류"