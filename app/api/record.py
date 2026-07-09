from datetime import date

from fastapi import APIRouter, Depends
from app.schemas.base import MessageResponse
from app.schemas.record import RecordAllListResponse, RecordCreateRequest, RecordCreateResponse, RecordListResponse, RecordUpdateRequest, RecordUpdateResponse
from app.services.record import create_record, delete_record, get_all_records, get_records, update_record
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("", response_model=RecordCreateResponse)
async def create_record_route(
    request: RecordCreateRequest,
    current_user: User = Depends(get_current_user)
):
    return await create_record(str(current_user.id), request)


@router.get("", response_model=RecordAllListResponse)
async def get_all_records_route(
    current_user: User = Depends(get_current_user)
):
    return await get_all_records(str(current_user.id))


@router.get("/{date}", response_model=RecordListResponse)
async def get_records_route(
    date: date, 
    current_user: User = Depends(get_current_user)
):
    return await get_records(str(current_user.id), date)


@router.put("/{record_id}", response_model=RecordUpdateResponse)
async def update_record_route(
    record_id: str,
    request: RecordUpdateRequest,
    current_user: User = Depends(get_current_user)
):
    return await update_record(str(current_user.id), record_id, request)


@router.delete("/{record_id}", response_model=MessageResponse)
async def delete_record_route(
    record_id: str,
    current_user: User = Depends(get_current_user)
):
    return await delete_record(str(current_user.id), record_id)