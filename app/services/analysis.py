from beanie import PydanticObjectId
from app.models.record import Record
from collections import defaultdict


async def get_summary(user_id: str) -> dict:
    records = await Record.find(
        Record.user_id == PydanticObjectId(user_id)
    ).to_list()

    total_success = sum(1 for r in records if r.status == "success")
    total_fail = sum(1 for r in records if r.status == "fail")

    # 날짜별로 그룹핑 (같은 날 여러 목표)
    date_records = defaultdict(list)
    for r in records:
        date_records[r.record_date].append(r)

    # 날짜 정렬
    sorted_dates = sorted(date_records.keys(), reverse=True)

    # 현재 연속 성공일 계산 (하루에 모든 목표 성공해야 연속)
    current_streak = 0
    for d in sorted_dates:
        day_records = date_records[d]
        if all(r.status == "success" for r in day_records):
            current_streak += 1
        else:
            break

    # 최장 연속 성공일 계산
    max_streak = 0
    temp_streak = 0
    for d in sorted(date_records.keys()):
        day_records = date_records[d]
        if all(r.status == "success" for r in day_records):
            temp_streak += 1
            max_streak = max(max_streak, temp_streak)
        else:
            temp_streak = 0

    return {
        "totalSuccess": total_success,
        "totalFail": total_fail,
        "currentStreak": current_streak,
        "maxStreak": max_streak,
    }


async def get_weekly(user_id: str) -> dict:
    records = await Record.find(
        Record.user_id == PydanticObjectId(user_id)
    ).to_list()

    days = ["월", "화", "수", "목", "금", "토", "일"]
    weekly = {i: {"failCount": 0, "totalCount": 0} for i in range(7)}

    for r in records:
        dow = r.day_of_week
        if dow is not None:
            weekly[dow]["totalCount"] += 1
            if r.status == "fail":
                weekly[dow]["failCount"] += 1

    result = []
    for i, day in enumerate(days):
        total = weekly[i]["totalCount"]
        fail = weekly[i]["failCount"]
        fail_rate = round((fail / total) * 100, 1) if total > 0 else 0.0
        result.append({
            "dayOfWeek": i,
            "day": day,
            "failCount": fail,
            "totalCount": total,
            "failRate": fail_rate
        })

    # 가장 실패율 높은 요일
    worst_day = max(result, key=lambda x: x["failRate"])

    return {
        "weekly": result,
        "worstDay": worst_day["day"] if worst_day["failRate"] > 0 else None
    }


async def get_reasons(user_id: str) -> dict:
    records = await Record.find(
        Record.user_id == PydanticObjectId(user_id),
        Record.status == "fail"
    ).to_list()

    total_fail = len(records)

    # 카테고리별 집계
    category_count = defaultdict(int)
    for r in records:
        category = r.reason_category or "기타"
        category_count[category] += 1

    # 정렬 후 TOP3
    sorted_reasons = sorted(
        category_count.items(),
        key=lambda x: x[1],
        reverse=True
    )[:3]

    reasons = []
    for rank, (category, count) in enumerate(sorted_reasons, 1):
        rate = round((count / total_fail) * 100, 1) if total_fail > 0 else 0.0
        reasons.append({
            "rank": rank,
            "reasonCategory": category,
            "count": count,
            "rate": rate
        })

    return {
        "totalFail": total_fail,
        "reasons": reasons
    }