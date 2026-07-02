from datetime import datetime, date, timezone
from typing import Optional
from beanie import Document, PydanticObjectId
from pydantic import Field


class Record(Document):
    user_id: PydanticObjectId
    goal_id: PydanticObjectId
    record_date: date
    status: str                          # success / fail
    reason_text: Optional[str] = None
    reason_category: Optional[str] = None
    day_of_week: Optional[int] = None    # 0월 ~ 6일
    hour_logged: Optional[int] = None    # 기록한 시간
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "records"