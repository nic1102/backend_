from fastapi import APIRouter, Depends, Response
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import JSONResponse

from app.db_models.models import Song, Group
from app.di.db_di import get_async_session
from app.pd_models.group_name import GroupName
from app.pd_models.song_name import SongName

song_router = APIRouter(prefix="/songs")


@song_router.get("/get_one/{song_id}")
async def get_song_by_id(song_id: int, session: AsyncSession = Depends(get_async_session)) -> JSONResponse:
    response = await session.execute(select(Song.name).filter(Song.id == song_id))
    r = response.mappings().first()
    if r is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"name": None})
    return JSONResponse(status_code=status.HTTP_200_OK, content={"name": r.get("name")})


@song_router.get("/get_all/{group_name}")
async def get_songs_by_group(group_name: str,
                             session: AsyncSession = Depends(get_async_session)) -> JSONResponse:
    group_id = await session.execute(select(Group.id).filter(Group.name == group_name))
    group_id = group_id.mappings().first().get("id")
    song_list = await session.execute(select(Song.name).filter(Song.group_id == group_id))
    song_list = list(song_list.mappings().all())
    song_list_r = []
    for i in song_list:
        song_list_r.append(i.get("name"))
    return JSONResponse(status_code=status.HTTP_200_OK, content={"song_list": song_list_r})


@song_router.post("/")
async def create_new_song(song_name: SongName, group_name: GroupName,
                          session: AsyncSession = Depends(get_async_session)) -> JSONResponse:
    try:
        matches = await session.execute(select(Song.name).filter(func.lower(Song.name) == song_name.song_name.lower()))
        matches = matches.mappings().first()
        if matches is not None:
            return JSONResponse(status_code=status.HTTP_200_OK, content={"song_id": None,
                                                                         "detail": "Такая песня уже есть"})

        session.add(Group(name=group_name.group_name))
        await session.flush()
        g_id = await session.execute(select(Group.id)
                                     .filter(Group.name == group_name.group_name))
        g_id = g_id.mappings().first().get('id')
        session.add(Song(group_id=g_id, name=song_name.song_name))
        await session.commit()
        return JSONResponse(status_code=status.HTTP_200_OK)
    except Exception as ex:
        await session.rollback()
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"song_id": None,
                                                                                        "detail": ex.__str__()})
