from sqlalchemy import Column, String, Integer, Boolean, Float, JSON, ForeignKey
from typing import Optional

from sqlalchemy.orm import relationship, joinedload

from models.database import async_session
from sqlalchemy import select, update, or_

from models.base import Base
from models.bybit_account import BybitAccount



class TsAccounts(Base):
    __tablename__ = 'tokensplash_accs'
    id = Column(Integer, primary_key=True)
    bought = Column(Float, default=0)
    sold = Column(Float, default=0)
    bybit_account_id = Column(Integer, ForeignKey('bybit_account.id'))

    bybit_account = relationship("BybitAccount", backref="tokensplash_accs")


    def __init__(self, token: str, user_agent: str, proxy: str, bought: float = 0, sold: float = 0):
        self.token = token
        self.user_agent = user_agent
        self.proxy = proxy
        self.bought = bought
        self.sold = sold

    def __repr__(self):
        info: str = f'ID = {self.id}, {self.bybit_account}, bought = {self.bought}, sold = {self.sold}'
        return info

    @staticmethod
    async def get_records(**kwargs):
        async with async_session() as session:
            res = await session.execute(select(TsAccounts).filter_by(**kwargs))
            #res = await session.execute(select(Accounts).where(Accounts.key == value))
            return res.scalars()

    @staticmethod
    async def get_records_with_empty_fields():
        stmt_get = (
            select(TsAccounts, BybitAccount)
                .where(
                or_(TsAccounts.bought == None,
                    TsAccounts.sold == None)
                ).options(joinedload(TsAccounts.bybit_account)).options(joinedload(BybitAccount.email)).options(joinedload(BybitAccount.proxy))
        )

        async with async_session() as session:
            res = await session.execute(stmt_get)

            return res.scalars().all()

    @staticmethod
    async def get_record(**kwargs):
        objects = await TsAccounts.get_records(**kwargs)
        obj = objects.first()

        return obj

    @staticmethod
    async def get_or_create(**kwargs):
        instance = await TsAccounts.get_record(**kwargs)
        if not instance:
            instance = TsAccounts(**kwargs)
            async with async_session() as session:
                session.add(instance)
                await session.commit()

        return instance


    @staticmethod
    async def add_record(**kwargs):
        async with async_session() as session:
            acc = TsAccounts(**kwargs)
            session.add(acc)
            await session.commit()

    @staticmethod
    async def update_from_instance(instance, **values):
        async with async_session() as session:
            stmt_update = (
                update(TsAccounts)
                    .where(TsAccounts.id == instance.id)
                    .values(**values)
                    .execution_options(synchronize_session="fetch")
            )

            await session.execute(stmt_update)
            await session.commit()