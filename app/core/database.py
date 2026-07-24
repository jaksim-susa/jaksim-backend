from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.core.config import settings
from app.models.ai_insight import AiInsight
from app.models.user import User
from app.models.goal import Goal
from app.models.record import Record
from app.models.diary import Diary

async def init_db():
    client = AsyncIOMotorClient(settings.DOCUMENT_DB_CONNECTION_STR)
    await init_beanie(
        database=client[settings.DOCUMENT_DATABASE_NAME],
        document_models=[
            User,
            Goal,
            Record,
            Diary,
            AiInsight
            ]
    )