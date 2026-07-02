from datetime import date

from pydantic import BaseModel


# 일기 조회 Response
class DiaryResponse(BaseModel):
    diaryId: str
    content: str
    recordDate: date