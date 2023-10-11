from models import Users
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import select
from hashlib import sha256


class CRUD:
    async def get_all_users(self, async_session: async_sessionmaker[AsyncSession]):
        async with async_session() as session:
            statement = select(Users).order_by(Users.user_id)
            result = await session.execute(statement)
            return result.scalars().all()
    async def get_user_by_id(self, async_session: async_sessionmaker[AsyncSession], user_id: int):
        async with async_session() as session:
            sql_query = select(Users).order_by(Users.user_id == user_id)
            result = await session.execute(sql_query)
            return result.scalars().one()

    async def create_user(self, async_session: async_sessionmaker[AsyncSession], user_data: Users):
        async with async_session() as session:
            session.add(user_data)
            await session.commit()

    async def update_user(self, async_session: async_sessionmaker[AsyncSession], user_id: int, new_password: str):
        async with async_session() as session:
            user = await self.get_user_by_id(session, user_id)
            user.user_password = await sha256(bytes(new_password, encoding="utf-8")).hexdigest()
            await session.commit()

    async def delete_user(self, async_session: async_sessionmaker[AsyncSession], user_data: Users):
        async with async_session() as session:
            await session.delete(user_data)
            await session.commit()
