from sqlalchemy import Column, Integer, String, Boolean

from models.base import Base
from models.db_operations import DbOperations


class Networks(Base, DbOperations):
    __tablename__ = 'networks'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    rpc = Column(String)
    chain_id = Column(Integer)
    eip1559_tx = Column(Boolean)
    coin_symbol = Column(String)
    decimals = Column(Integer)
    explorer = Column(String)

    '''def __init__(self,
                 name: str,
                 rpc: str,
                 chain_id: int,
                 eip1559_tx: bool,
                 coin_symbol: str,
                 explorer: str,
                 decimals: int,
                 ):
        self.name = name
        self.rpc = rpc
        self.chain_id = chain_id
        self.eip1559_tx = eip1559_tx
        self.coin_symbol = coin_symbol
        self.decimals = decimals
        self.explorer = explorer'''

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if value:
                setattr(self, key, value)

    def __repr__(self):
        info: str = f'Имя сети = {self.name} rpc = {self.rpc} coin symbol = {self.coin_symbol}'
        return info

