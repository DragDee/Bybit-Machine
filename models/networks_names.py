from sqlalchemy import Column, String, Integer, Boolean, Float, ForeignKey
from typing import Optional

from sqlalchemy.orm import relationship

from models.database import async_session
from sqlalchemy import select, update, or_

from models.base import Base
from models.db_operations import DbOperations


class NetworksNames(Base, DbOperations):
    __tablename__ = 'network_name'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    binance_name = Column(String, default='')
    bybit_name = Column(String, default='')
    mexc_name = Column(String, default='')

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if value:
                setattr(self, key, value)

    def __repr__(self):
        info: str = (f'Network Name = {self.name}, Binance = {self.binance_name}, Bybit = {self.bybit_name},'
                     f' Mexc = {self.mexc_name}')
        return info