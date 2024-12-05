from fastapi import APIRouter
from fastapi import status, Response
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from starlette.responses import JSONResponse

from app.db_models.models import Group
from app.di.db_di import get_async_session

from app.pd_models.group_name import GroupName

group_router = APIRouter(prefix="/groups")


@group_router.get("/get_one/{group_id}")
async def get_group_by_id(group_id: int, session: AsyncSession = Depends(get_async_session)) -> JSONResponse:
    response = await session.execute(select(Group.name).filter(Group.id == group_id))
    r = response.mappings().first()
    if r is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"name": None})
    return JSONResponse(status_code=status.HTTP_200_OK, content={"name": r.get("name")})


@group_router.get("/get_all/invalidated")
async def get_all_groups(session: AsyncSession = Depends(get_async_session)) -> JSONResponse:
    group_list = await session.execute(select(Group.name).filter(Group.is_validated == False))
    group_list = list(group_list.mappings().all())
    group_list_r = []
    for i in group_list:
        group_list_r.append(i.get("name"))
    return JSONResponse(status_code=status.HTTP_200_OK, content={"group_list": group_list_r})


@group_router.get("/get_all/validated")
async def get_all_groups(session: AsyncSession = Depends(get_async_session)) -> JSONResponse:
    group_list = await session.execute(select(Group.name).filter(Group.is_validated == True))
    group_list = list(group_list.mappings().all())
    group_list_r = []
    for i in group_list:
        group_list_r.append(i.get("name"))
    return JSONResponse(status_code=status.HTTP_200_OK, content={"group_list": group_list_r})


@group_router.post("/")
async def create_new_group(group_name: GroupName, session: AsyncSession = Depends(get_async_session)) -> JSONResponse:
    try:
        matches = await session.execute(select(Group.name)
                                        .filter(func.lower(Group.name) == group_name.group_name.lower()))
        matches = matches.mappings().first()
        if matches is None:
            session.add(Group(name=group_name.group_name))
            await session.flush()
            group_id = await session.execute(select(Group.id).filter(Group.name == group_name.group_name))
            group_id = group_id.mappings().first()
            await session.commit()
            return JSONResponse(status_code=status.HTTP_200_OK, content={"group_id": group_id.get("id"),
                                                                         "detail": "Новая группа добавлена"})
        else:
            return JSONResponse(status_code=status.HTTP_200_OK, content={"group_id": None,
                                                                         "detail": "Такая группа уже существует"})
    except Exception as ex:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"group_id": -1,
                                                                                        "detail": ex.__str__()})
