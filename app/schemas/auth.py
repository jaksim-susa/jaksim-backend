from pydantic import BaseModel


class TokenRefreshResponse(BaseModel):
    accessToken: str