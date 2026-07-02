from fastapi import APIRouter, Request, Response
from app.schemas.base import MessageResponse
from app.schemas.user import KakaoLoginRequest, Token
from app.services.auth import kakao_login, logout

router = APIRouter()

@router.post("/login", response_model=Token)
async def kakao_login_route(request: KakaoLoginRequest, response: Response):
    return await kakao_login(request.code, response)


@router.post("/logout", response_model=MessageResponse)
async def logout_route(response: Response, request: Request):
    return await logout(response, request)