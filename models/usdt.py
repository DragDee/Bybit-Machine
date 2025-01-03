from sqlalchemy import Column, String, Integer, Boolean, Float, ForeignKey
from typing import Optional

from sqlalchemy.orm import relationship

from models.database import async_session
from sqlalchemy import select, update, or_

from models.base import Base
from models.db_operations import DbOperations
from models.networks import Networks


class Usdt(Base, DbOperations):
    __tablename__ = 'usdt'
    id = Column(Integer, primary_key=True)
    contract_address = Column(String)
    network_id = Column(String, ForeignKey('networks.id'))

    network = relationship("Networks", backref="usdt")

    def __init__(self, contract_address: str):
        self.contract_address = contract_address

    def __repr__(self):
        info: str = f'USDT, Contract address = {self.contract_address}'
        return info