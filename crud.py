from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Users, PasswordUpdates
from datetime import datetime


class CRUD:
    def get_users(self, session: Session):
        sql_query = select(Users).order_by(Users.id)
        result = session.execute(sql_query)

        return result.scalars().all()

    def get_user_by_username(self, session: Session, username: str):
        sql_query = select(Users).filter(Users.username.like(username))
        result = session.execute(sql_query)

        return result.scalars().one_or_none()

    def get_timestamp_by_username(self, session: Session, username: str):
        sql_query = select(PasswordUpdates.timestamp).filter(PasswordUpdates.username.like(username))
        result = session.execute(sql_query)

        return result.scalars().one()

    def create_user(self, session: Session, user_data: Users):
        passwordUpdate = PasswordUpdates(username=user_data.username)
        session.add_all([user_data, passwordUpdate])
        session.commit()

    def update_password(self, session: Session, user: Users, new_password: str):
        user.password = new_password
        session.commit()

    def update_timestamp(self, session: Session, username: str):
        sql_query = select(PasswordUpdates).filter(PasswordUpdates.username.like(username))
        result = session.execute(sql_query).scalars().one()

        result.timestamp = datetime.now().timestamp()
        session.commit()
