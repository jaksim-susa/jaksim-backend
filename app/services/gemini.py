from google import genai
from app.core.config import settings
from app.models.ai_insight import AiInsight
from app.models.record import Record
from beanie import PydanticObjectId
from datetime import datetime, timedelta, timezone
from app.utils.date import to_kst
from collections import defaultdict

client = genai.Client(api_key=settings.GOOGLE_API_KEY)
AI_MODEL = "gemini-2.5-flash"


async def get_briefing(user_id: str) -> str:
    today_kst = to_kst(datetime.now(timezone.utc)).date()

    # 오늘 브리핑 있는지 확인
    insights = await AiInsight.find(
        AiInsight.user_id == PydanticObjectId(user_id),
        AiInsight.type == "briefing"
    ).to_list()

    existing = next(
        (i for i in insights if to_kst(i.created_at).date() == today_kst),
        None
    )

    if existing:
        return existing.content


    # 최근 7일 실패 기록 가져오기
    seven_days_ago = to_kst(datetime.now(timezone.utc)).date() - timedelta(days=7)

    records = await Record.find(
        Record.user_id == PydanticObjectId(user_id),
        Record.status == "fail",
        Record.record_date >= seven_days_ago
    ).to_list()

    if not records:
        return "아직 실패 기록이 없어요. 오늘도 목표를 향해 나아가 보세요! 🔍"

    # 실패 이유 수집
    fail_reasons = [r.reason_text for r in records if r.reason_text]
    fail_categories = [r.reason_category for r in records if r.reason_category]

    prompt = f"""
                당신은 습관 형성 전문가입니다.
                사용자의 최근 7일 실패 데이터를 분석해서 오늘 하루 동기부여 메시지를 작성해주세요.

                실패 이유: {fail_reasons}
                실패 카테고리: {fail_categories}

                조건:
                - 2~3문장으로 짧게
                - 따뜻하고 격려하는 톤
                - 구체적인 개선 방안 제시
                - 한국어로 작성
                """

    response = client.models.generate_content(
        model=AI_MODEL,
        contents=prompt
    )
    content = response.text.strip()

    # DB 저장
    await AiInsight(
        user_id=PydanticObjectId(user_id),
        type="briefing",
        content=content,
        date=today_kst
    ).insert()

    return response.text.strip()


async def get_insight(user_id: str) -> str:
    today_kst = to_kst(datetime.now(timezone.utc)).date()

    insights = await AiInsight.find(
        AiInsight.user_id == PydanticObjectId(user_id),
        AiInsight.type == "insight"
    ).to_list()

    existing = next(
        (i for i in insights if to_kst(i.created_at).date() == today_kst),
        None
    )

    if existing:
        return existing.content

    # 전체 기록 가져오기
    records = await Record.find(
        Record.user_id == PydanticObjectId(user_id)
    ).to_list()

    if not records:
        return "아직 분석할 데이터가 없어요. 기록을 쌓아보세요! 📊"

    # 요일별 실패율 계산
    days = ["월", "화", "수", "목", "금", "토", "일"]
    weekly = defaultdict(lambda: {"fail": 0, "total": 0})

    for r in records:
        if r.day_of_week is not None:
            weekly[r.day_of_week]["total"] += 1
            if r.status == "fail":
                weekly[r.day_of_week]["fail"] += 1

    weekly_summary = []
    for i, day in enumerate(days):
        total = weekly[i]["total"]
        fail = weekly[i]["fail"]
        rate = round((fail / total) * 100, 1) if total > 0 else 0
        weekly_summary.append(f"{day}요일 실패율: {rate}%")

    # 실패 키워드 수집
    fail_reasons = [r.reason_text for r in records if r.reason_text and r.status == "fail"]
    fail_categories = [r.reason_category for r in records if r.reason_category and r.status == "fail"]

    prompt = f"""
                당신은 데이터 기반 습관 분석 전문가입니다.
                사용자의 실패 패턴을 분석해서 인사이트를 제공해주세요.

                요일별 실패율:
                {chr(10).join(weekly_summary)}

                실패 이유: {fail_reasons[:10]}
                실패 카테고리: {fail_categories}

                조건:
                - 3~4문장으로
                - 어떤 요일에 왜 실패하는지 패턴 분석
                - 반복되는 키워드 언급
                - 구체적인 개선 방안 제시
                - 한국어로 작성
                """

    response = client.models.generate_content(
        model=AI_MODEL,
        contents=prompt
    )
    content = response.text.strip()

    # DB 저장
    await AiInsight(
        user_id=PydanticObjectId(user_id),
        type="insight",
        content=content,
        date=today_kst
    ).insert()

    return response.text.strip()