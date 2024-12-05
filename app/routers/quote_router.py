from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import JSONResponse

from app.db_models.models import Quote, Group, Song
from app.di.db_di import get_async_session
from app.pd_models.group_name import GroupName
from app.pd_models.quote_text import QuoteText
from app.pd_models.song_name import SongName

quote_router = APIRouter(prefix="/quotes")


@quote_router.get("/{quote_id}")
async def get_quote_text_by_id(quote_id: int, session: AsyncSession = Depends(get_async_session)):
    quote = await session.execute(select(Quote.text).filter(Quote.id == quote_id))
    quote = quote.mappings().first()
    if quote is None:
        response = JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"text": None})
    else:
        response = JSONResponse(status_code=status.HTTP_200_OK, content={"text": quote.get("text")})
    return response


@quote_router.post("/")
async def create_quote(quote_text: QuoteText, group_name: GroupName, song_name: SongName,
                       session: AsyncSession = Depends(get_async_session)):
    try:
        group_id = await session.execute(select(Group.id).filter(Group.name == group_name.group_name))
        group_id = group_id.mappings().first()
        if group_id is None:
            session.add(Group(name=group_name.group_name))
            await session.flush()

            group_id = await session.execute(select(Group.id).filter(Group.name == group_name.group_name))
            group_id = group_id.mappings().first().get("id")

            session.add(Song(group_id=group_id, name=song_name.song_name))
            await session.flush()

            song_id = await session.execute(select(Song.id).filter(Song.name == song_name.song_name))
            song_id = song_id.mappings().first().get("id")

            await session.flush()
            session.add(Quote(song_id=song_id, text=quote_text.quote_text))
            await session.commit()
            return JSONResponse(status_code=status.HTTP_200_OK, content={"text": quote_text.quote_text,
                                                                         "detail": None})
    except Exception as ex:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"text": quote_text.quote_text,
                                                                                        "detail": ex.__str__()})


@quote_router.get("/next/{current_id}")
async def get_next_quote(current_id: int, session: AsyncSession = Depends(get_async_session)):
    next_quote_id = await session.execute(select(Quote.id, Quote.text, Quote.song_id).filter(Quote.id > current_id))
    next_quote_id = next_quote_id.mappings().first()
    next_quote_text = next_quote_id.get("text")

    if next_quote_id is None:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"text": None,
                                                                     "detail": "Конец списка"})

    next_quote_song_id = next_quote_id.get("song_id")
    next_quote_group_id = await session.execute(select(Song.group_id).filter(Song.id == next_quote_song_id))
    next_quote_group_id = next_quote_group_id.mappings().first().get("group_id")

    next_quote_group_name = await session.execute(select(Group.name).filter(Group.id == next_quote_group_id))
    next_quote_group_name = next_quote_group_name.mappings().first().get("name")

    next_quote_song_name = await session.execute(select(Song.name).filter(Song.id == next_quote_song_id))
    next_quote_song_name = next_quote_song_name.mappings().first().get("name")

    next_quote_likes = await session.execute(select(Quote.likes).filter(Quote.id == next_quote_id))
    next_quote_likes = next_quote_likes.mappings().first()

    next_quote_dislikes = await session.execute(select(Quote.dislikes).filter(Quote.id == next_quote_id))
    next_quote_dislikes = next_quote_dislikes.mappings().first()

    return JSONResponse(status_code=status.HTTP_200_OK, content={"quote_text": next_quote_text,
                                                                 "quote_group": next_quote_group_name,
                                                                 "quote_song": next_quote_song_name,
                                                                 "quote_likes": next_quote_likes,
                                                                 "quote_dislikes": next_quote_dislikes,
                                                                 "detail": None})