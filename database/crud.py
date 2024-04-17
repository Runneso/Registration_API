from schemas import CreateUser
from .models import Users

from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class CRUD:
    @classmethod
    async def get_users_orm(cls, session: AsyncSession):
        sql_query = select(Users).order_by(Users.id)

        result = await session.execute(sql_query)
        return result.scalars().all()

    @classmethod
    async def create_user_orm(cls, user_data: CreateUser, session: AsyncSession):
        try:
            new_user = Users(**user_data.model_dump())
            session.add(new_user)
            await session.commit()
        except Exception as error:
            print(error)
            await session.close()
            raise HTTPException(status_code=409, detail="Conflict user data!")
        await session.close()
