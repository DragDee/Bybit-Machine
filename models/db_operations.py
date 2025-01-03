
from models.database import async_session
from sqlalchemy import update, and_, select, func

class DbOperations:

    async def add_record(self, **kwargs):
        async with async_session() as session:
            acc = self.__class__(**kwargs)
            session.add(acc)
            await session.commit()

    async def edit_record(self, **kwargs):
        async with async_session() as session:
            acc = self.__class__(**kwargs)
            session.add(acc)
            await session.commit()

    async def update(self, **values):
        async with async_session() as session:
            class_name = self.__class__
            stmt_update = (
                update(class_name)
                    .where(class_name.id == self.id)
                    .values(**values)
                    .execution_options(synchronize_session="fetch")
            )

            await session.execute(stmt_update)
            await session.commit()

    async def get(self, **kwargs) -> list:
        async with async_session() as session:
            class_name = self.__class__
            stmt = select(class_name)
            if kwargs:
                conditions = []

                conditions = [func.lower(getattr(class_name, key)) == func.lower(value) for key, value in kwargs.items()]
                stmt = stmt.where(and_(*conditions))

            result = await session.execute(stmt)
            await session.commit()

            return result.scalars().all()
