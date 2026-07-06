from datetime import datetime, timezone
from beanie import Document, PydanticObjectId
from pydantic import Field


class AiInsight(Document):
    user_id: PydanticObjectId
    type: str                    # briefing / insight
    content: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    class Settings:
        name = "ai_insights"