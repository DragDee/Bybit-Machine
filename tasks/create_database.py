from models.database import engine, async_session
from models.base import Base
from models.accounts import Accounts
import asyncio
from models.email import Email
from models.bybit_account import BybitAccount
from models.proxy import Proxy
from models.accounts import Accounts

async def create_db():
    #Base.metadata.create_all(engine)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

async def async_db_operations():
    async with async_session() as session:
        async with session.begin():
            new_user = Accounts(token="k5k", bought=1.0, sold=1.0)
            session.add(new_user)
        await session.commit()

if __name__ == '__main__':
    asyncio.run(create_db())