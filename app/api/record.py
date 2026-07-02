from datetime import date

from fastapi import APIRouter, Depends
from app.schemas.record import RecordCreateRequest, RecordCreateResponse, RecordListResponse
from app.services.record import create_record, get_records
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/", response_model=RecordCreateResponse)
async def create_record_route(
    request: RecordCreateRequest,
    current_user: User = Depends(get_current_user)
):
    return await create_record(str(current_user.id), request)


@router.get("/{date}", response_model=RecordListResponse)
async def get_records_route(
    date: date, 
    current_user: User = Depends(get_current_user)
):
    return await get_records(str(current_user.id), date)