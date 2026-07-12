from pydantic import BaseModel


class TokenRefreshResponse(BaseModel):
    accessToken: str


class KakaoLoginRequest(BaseModel):
    code: str


class Token(BaseModel):
    accessToken: str
    userId: str
    nickname: str
    theme: str
    isNewUser: bool
    hasGoal: bool


class SignupRequest(BaseModel):
    email: str
    password: str
    nickname: str