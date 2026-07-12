from fastapi import APIRouter, Request, Response, Depends
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.auth import LoginRequest, SignupRequest, TokenRefreshResponse
from app.schemas.base import MessageResponse
from app.schemas.auth import KakaoLoginRequest, Token
from app.services.auth import email_login, kakao_login, logout, refresh_token, signup

router = APIRouter()

@router.post("/kakao_login", response_model=Token)
async def kakao_login_route(request: KakaoLoginRequest, response: Response):
    return await kakao_login(request.code, response)


@router.post("/logout", response_model=MessageResponse)
async def logout_route(
    request: Request,
    response: Response,
    _: User = Depends(get_current_user)
):
    return await logout(response, request)


@router.post("/token/refresh", response_model=TokenRefreshResponse)
async def refresh_token_route(
    request: Request,
    response: Response
):
    return await refresh_token(request, response)


@router.post("/signup", response_model=MessageResponse)
async def signup_route(request: SignupRequest, response: Response):
    return await signup(request, response)


@router.post("/login", response_model=Token)
async def email_login_route(request: LoginRequest, response: Response):
    return await email_login(request, response)