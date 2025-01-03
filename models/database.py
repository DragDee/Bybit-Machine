import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


from data.config import DATABASE_NAME

async def pragma(engine):
    async with engine.begin() as conn:
        await conn.execute(text("PRAGMA journal_mode=WAL"))
        await conn.commit()

        return engine



engine = create_async_engine(f'sqlite+aiosqlite:///{DATABASE_NAME}',
                             echo=False,
                             connect_args={
                                 "timeout": 5,
                                 "check_same_thread": False,
                             }

                             )
#engine = asyncio.run(pragma(engine))

async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
