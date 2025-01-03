from sqlalchemy import Column, String, Integer, Boolean, Float, ForeignKey
from typing import Optional

from sqlalchemy.orm import relationship

from models.database import async_session
from sqlalchemy import select, update, or_

from models.base import Base
from models.db_operations import DbOperations


class Proxy(Base, DbOperations):
    __tablename__ = 'proxy'
    id = Column(Integer, primary_key=True)
    ip = Column(String)
    port = Column(String)
    proxy_login = Column(String)
    proxy_password = Column(String)
    proxy_type = Column(String)


    def __init__(self,
                 ip: str,
                 port: str,
                 proxy_login: str,
                 proxy_password: str,
                 proxy_type: str):

        self.ip = ip
        self.port = port
        self.proxy_login = proxy_login
        self.proxy_password = proxy_password
        self.proxy_type = proxy_type

    def __repr__(self):
        info: str = f'{self.proxy_type}://{self.ip}:{self.port}:{self.proxy_login}:{self.proxy_password}'
        return info

    @staticmethod
    def parse_proxy(proxy_str: str):
        try:
            p = proxy_str.split('://')
            proxy_type = p[0]
            parsed_proxy = p[1].split(':')
            parsed_proxy.insert(0, proxy_type)
        except Exception as ex:
            print(ex)
            parsed_proxy = [' ', ' ', ' ', ' ', ' ']

        return parsed_proxy
