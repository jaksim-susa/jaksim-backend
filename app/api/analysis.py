from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.models.user import User
from app.services.analysis import get_summary, get_weekly, get_reasons
from app.services.gemini import get_briefing, get_insight

router = APIRouter()


@router.get("/summary")
async def get_summary_route(
    current_user: User = Depends(get_current_user)
):
    return await get_summary(str(current_user.id))


@router.get("/weekly")
async def get_weekly_route(
    current_user: User = Depends(get_current_user)
):
    return await get_weekly(str(current_user.id))


@router.get("/reasons")
async def get_reasons_route(
    current_user: User = Depends(get_current_user)
):
    return await get_reasons(str(current_user.id))


@router.get("/briefing")
async def get_briefing_route(
    current_user: User = Depends(get_current_user)
):
    content = await get_briefing(str(current_user.id))
    return {"content": content}


@router.post("/insight")
async def get_insight_route(
    current_user: User = Depends(get_current_user)
):
    content = await get_insight(str(current_user.id))
    return {"content": content}