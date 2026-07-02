from datetime import datetime, date, timezone
from typing import Optional
from beanie import Document, PydanticObjectId
from pydantic import Field


class Goal(Document):
    user_id: PydanticObjectId
    title: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "goals"