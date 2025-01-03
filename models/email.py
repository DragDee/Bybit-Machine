from sqlalchemy import Column, String, Integer, Boolean, Float, ForeignKey
from typing import Optional

from sqlalchemy.orm import relationship

from models.database import async_session
from sqlalchemy import select, update, or_

from models.base import Base
from models.db_operations import DbOperations


class Email(Base, DbOperations):
    __tablename__ = 'email'
    id = Column(Integer, primary_key=True)
    imap_login = Column(String, unique=True)
    imap_password = Column(String)

    def __init__(self, imap_login: str, imap_password: str):
        self.imap_login = imap_login
        self.imap_password = imap_password

    def __repr__(self):
        info: str = f'Email = {self.imap_login}, password = {self.imap_password}'
        return info