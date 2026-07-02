from fastapi import APIRouter, Depends
from app.schemas.record import RecordCreateRequest, RecordCreateResponse
from app.services.record import create_record
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/", response_model=RecordCreateResponse)
async def create_record_route(
    request: RecordCreateRequest,
    current_user: User = Depends(get_current_user)
):
    return await create_record(str(current_user.id), request)