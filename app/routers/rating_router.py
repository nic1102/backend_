from fastapi import APIRouter, Depends, Response
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.db_models.models import Song, Group
from app.di.db_di import get_async_session
from app.pd_models.group_name import GroupName
from app.pd_models.song_name import SongName

rating_router = APIRouter(prefix="/ratings")

@rating_router.put("/add_like/{quote_id}")
async def add_like_to_quote(quote_id: int, request: Request,
                            session: AsyncSession = Depends(get_async_session),) -> JSONResponse:
    ...