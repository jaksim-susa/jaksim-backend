from beanie import Document
from pydantic import Field
from typing import Optional
from datetime import datetime

class User(Document):
    email: Optional[str] = None
    password: Optional[str] = None
    kakao_id: Optional[str] = None
    nickname: str
    theme: Optional[str] = "light"
    refresh_token: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "users"