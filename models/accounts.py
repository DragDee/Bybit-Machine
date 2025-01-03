from sqlalchemy import Column, String, Integer, Boolean, Float, JSON, ForeignKey
from typing import Optional

from sqlalchemy.orm import relationship, joinedload

from models.database import async_session
from sqlalchemy import select, update, or_

from models.base import Base
from models.bybit_account import BybitAccount



class Accounts(Base):
    __tablename__ = 'ts_accounts'
    id = Column(Integer, primary_key=True)
    token = Column(String)
    cookie = Column(JSON)
    user_agent = Column(String)
    proxy = Column(String)
    bought = Column(Float, default=0)
    sold = Column(Float, default=0)



    def __init__(self, token: str, user_agent: str, proxy: str, bought: float = 0, sold: float = 0):
        self.token = token
        self.user_agent = user_agent
        self.proxy = proxy
        self.bought = bought
        self.sold = sold

    def __repr__(self):
        info: str = f'Token = {self.token[-20:]}, bought = {self.bought}, sold = {self.sold}'
        return info

    @staticmethod
    async def get_records(**kwargs):
        async with async_session() as session:
            res = await session.execute(select(Accounts).filter_by(**kwargs))
            #res = await session.execute(select(Accounts).where(Accounts.key == value))
            return res.scalars()

    @staticmethod
    async def get_records_with_empty_fields():
        stmt_get = (
            select(Accounts)
                .where(
                or_(Accounts.bought == None,
                    Accounts.sold == None)
                )
        )

        async with async_session() as session:
            res = await session.execute(stmt_get)

            return res.scalars().all()

    @staticmethod
    async def get_record(**kwargs):
        objects = await Accounts.get_records(**kwargs)
        obj = objects.first()

        return obj

    @staticmethod
    async def get_or_create(**kwargs):
        instance = await Accounts.get_record(**kwargs)
        if not instance:
            instance = Accounts(**kwargs)
            async with async_session() as session:
                session.add(instance)
                await session.commit()

        return instance


    @staticmethod
    async def add_record(**kwargs):
        async with async_session() as session:
            acc = Accounts(**kwargs)
            session.add(acc)
            await session.commit()

    @staticmethod
    async def update_from_instance(instance, **values):
        async with async_session() as session:
            stmt_update = (
                update(Accounts)
                    .where(Accounts.id == instance.id)
                    .values(**values)
                    .execution_options(synchronize_session="fetch")
            )

            await session.execute(stmt_update)
            await session.commit()