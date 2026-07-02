from datetime import datetime, date, timezone
from typing import Optional
from beanie import Document, PydanticObjectId
from pydantic import Field


class Diary(Document):
    user_id: PydanticObjectId
    diary_date: date
    content: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "diaries"