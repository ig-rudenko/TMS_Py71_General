from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.models import NoteModel


async def create_note(session: AsyncSession, *, tg_id: int, title: str, content: str) -> NoteModel:
    note = NoteModel(user_id=tg_id, title=title, content=content)

    session.add(note)
    await session.commit()
    await session.refresh(note)

    return note


async def get_last_notes(session: AsyncSession, limit: int = 10) -> list[NoteModel]:
    query = select(NoteModel).order_by(NoteModel.created_at.desc()).limit(limit)

    result = await session.execute(query)

    return list(result.scalars())


async def get_notes_by_id(session: AsyncSession, id_: int) -> NoteModel | None:
    query = select(NoteModel).where(NoteModel.id == id_)

    result = await session.execute(query)

    return result.scalar_one_or_none()


async def find_notes(session: AsyncSession, search: str = "", limit: int = 10) -> list[NoteModel]:
    query = select(NoteModel).order_by(NoteModel.created_at.desc()).limit(limit)

    if search:
        query = query.where(
            or_(
                NoteModel.title.icontains(search),
                NoteModel.title.icontains(search),
            )
        )

    result = await session.execute(query)

    return list(result.scalars())
