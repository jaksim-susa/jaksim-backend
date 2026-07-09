from datetime import datetime, timezone, date
from beanie import PydanticObjectId
from fastapi import HTTPException, status
from app.core.config import settings
from app.models.diary import Diary
from app.models.record import Record
from app.models.goal import Goal
from app.schemas.diary import DiaryResponse
from app.schemas.record import RecordAllListResponse, RecordCreateRequest, RecordCreateResponse, RecordListDayResponse, RecordListGoalResponse, RecordListResponse, RecordResponse, RecordUpdateRequest, RecordUpdateResponse
from app.services.goal import calculate_is_active_on_date
from app.utils.date import to_kst
from google import genai

async def create_record(user_id: str, request: RecordCreateRequest) -> RecordCreateResponse:
    # 1. 목표 존재 여부 확인
    goal = await Goal.get(PydanticObjectId(request.goalId))
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="설정된 목표가 없어요."
        )

    # 2. 오늘 기록 중복 확인 (KST 기준)
    today = to_kst(datetime.now(timezone.utc)).date()  # ← 수정
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

    # 3. AI 분류
    reason_category = None
    if request.status == "fail" and request.reasonText:
        reason_category = await classify_reason(request.reasonText)

    # 4. day_of_week, hour_logged 자동 계산
    now_kst = to_kst(datetime.now(timezone.utc))
    day_of_week = now_kst.weekday()
    hour_logged = now_kst.hour

    # 5. 기록 저장
    new_record = Record(
        user_id=PydanticObjectId(user_id),
        goal_id=PydanticObjectId(request.goalId),
        record_date=today,   # ← KST 기준 날짜
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


client = genai.Client(api_key=settings.GOOGLE_API_KEY)
CLASSIFY_MODEL = "gemini-2.5-flash"

async def classify_reason(reason_text: str) -> str:
    try:
        response = client.models.generate_content(
            model=CLASSIFY_MODEL,
            contents=f"""다음 실패 이유를 아래 카테고리 중 하나로 분류해줘.
                        카테고리: 피로, 시간부족, 동기저하, 건강, 날씨, 기타

                        카테고리 이름만 답해줘. 다른 말은 하지 마.

                        실패 이유: {reason_text}"""
        )
        return response.text.strip()
    except Exception as e:
        return "기타"


async def get_records(user_id: str, record_date: date) -> RecordListResponse:
    # 1. 활성 목표 전체 조회
    goals = await Goal.find(Goal.user_id == PydanticObjectId(user_id)).to_list()
    active_goals = [g for g in goals if calculate_is_active_on_date(g, record_date)]

    # 2. 해당 날짜 기록 조회
    records = await Record.find(
        Record.user_id == PydanticObjectId(user_id),
        Record.record_date == record_date
    ).to_list()

    # 3. 기록을 goal_id 기준으로 매핑
    record_map = {str(r.goal_id): r for r in records}

    # 4. 일기 조회
    diary = await Diary.find_one(
        Diary.user_id == PydanticObjectId(user_id),
        Diary.diary_date == record_date
    )

    # 5. 목표별로 기록 여부 확인
    result = []
    for goal in active_goals:
        record = record_map.get(str(goal.id))
        result.append(
            RecordResponse(
                recordId=str(record.id) if record else None,
                goalId=str(goal.id),
                goal=goal.title,
                status=record.status if record else None,
                reasonCategory=record.reason_category if record else None,
                reasonText=record.reason_text if record else None,
                recordDate=record_date,
            )
        )

    return RecordListResponse(
        records=result,
        diary=DiaryResponse(
            diaryId=str(diary.id),
            content=diary.content,
            recordDate=diary.diary_date,
        ) if diary else None
    )


async def get_all_records(user_id: str) -> RecordAllListResponse:
    # 1. 전체 기록 조회
    records = await Record.find(
        Record.user_id == PydanticObjectId(user_id)
    ).to_list()

    # 2. 전체 일기 조회
    diaries = await Diary.find(
        Diary.user_id == PydanticObjectId(user_id)
    ).to_list()

    # 3. 전체 목표 조회
    goals = await Goal.find(
        Goal.user_id == PydanticObjectId(user_id)
    ).to_list()

    # 4. 날짜별로 그룹핑
    date_set = set(r.record_date for r in records)

    # 5. 기록 매핑
    record_map = {}  # {(goal_id, date): record}
    for record in records:
        record_map[(str(record.goal_id), record.record_date)] = record

    # 6. 일기 매핑
    diary_map = {d.diary_date: d for d in diaries}

    # 7. 날짜별로 결과 생성
    result = []
    for target_date in sorted(date_set, reverse=True):
        # 해당 날짜 기준 활성 목표 필터링
        active_goals = [g for g in goals if calculate_is_active_on_date(g, target_date)]

        diary = diary_map.get(target_date)

        day_goals = []
        for goal in active_goals:
            record = record_map.get((str(goal.id), target_date))
            day_goals.append(
                RecordListGoalResponse(
                    goalId=str(goal.id),
                    recordId=str(record.id) if record else None,
                    goal=goal.title,
                    status=record.status if record else None,
                    reasonCategory=record.reason_category if record else None,
                )
            )

        result.append(
            RecordListDayResponse(
                date=target_date,
                diary=diary.content if diary else None,
                goals=day_goals,
            )
        )

    return RecordAllListResponse(records=result)


async def update_record(user_id: str, record_id: str, request: RecordUpdateRequest) -> RecordUpdateResponse:
    # 1. 기록 존재 여부 확인
    record = await Record.get(PydanticObjectId(record_id))
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="기록을 찾을 수 없어요."
        )

    # 2. 본인 기록인지 확인
    if str(record.user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="본인 기록만 수정할 수 있어요."
        )

    # 3. status에 따라 처리
    if request.status == "success":
        reason_text = None
        reason_category = None
    else:
        reason_text = request.reasonText
        reason_category = await classify_reason(request.reasonText) if request.reasonText else None

    # 4. 기록 업데이트
    await record.update({
        "$set": {
            "status": request.status,
            "reason_text": reason_text,
            "reason_category": reason_category,
            "updated_at": datetime.now(timezone.utc)
        }
    })

    return RecordUpdateResponse(
        recordId=str(record.id),
        goalId=str(record.goal_id),
        status=request.status,
        reasonText=reason_text,
        reasonCategory=reason_category,
        recordDate=record.record_date,
        createdAt=to_kst(record.created_at),
    )