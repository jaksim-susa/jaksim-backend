from pydantic import BaseModel


class KakaoLoginRequest(BaseModel):
    code: str


class Token(BaseModel):
    accessToken: str
    nickname: str
    theme: str
    isNewUser: bool
    hasGoal: bool