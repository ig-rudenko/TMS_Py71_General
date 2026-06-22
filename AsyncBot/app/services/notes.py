from sqlalchemy import select, or_

from app.db.connector import async_session_maker
from app.models import NoteModel


async def create_note(*, tg_id: int, title: str, content: str) -> NoteModel:
    note = NoteModel(user_id=tg_id, title=title, content=content)

    async with async_session_maker() as session:
        session.add(note)
        await session.commit()
        await session.refresh(note)

    return note


async def get_last_notes(limit: int = 10) -> list[NoteModel]:
    query = select(NoteModel).order_by(NoteModel.created_at.desc()).limit(limit)

    async with async_session_maker() as session:
        result = await session.execute(query)

    return list(result.scalars())


async def get_notes_by_id(id_: int) -> NoteModel | None:
    query = select(NoteModel).where(NoteModel.id == id_)

    async with async_session_maker() as session:
        result = await session.execute(query)

    return result.scalar_one_or_none()


async def find_notes(search: str = "", limit: int = 10) -> list[NoteModel]:
    query = select(NoteModel).order_by(NoteModel.created_at.desc()).limit(limit)

    if search:
        query = query.where(
            or_(
                NoteModel.title.icontains(search),
                NoteModel.title.icontains(search),
            )
        )

    async with async_session_maker() as session:
        result = await session.execute(query)

    return list(result.scalars())
