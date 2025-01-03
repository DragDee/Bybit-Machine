import random

from sqlalchemy import Column, String, Integer, Boolean, Float, ForeignKey, JSON, Date


from sqlalchemy.orm import relationship



from models.base import Base
from models.db_operations import DbOperations
from models.email import Email


class BybitAccount(Base, DbOperations):
    __tablename__ = 'bybit_account'
    id = Column(Integer, primary_key=True)
    user_agent = Column(String)
    bybit_id = Column(Integer, unique=True)
    group_name = Column(String)
    email_id = Column(Integer, ForeignKey('email.id'))
    password = Column(String)
    totp_key = Column(String)
    proxy_id = Column(Integer, ForeignKey('proxy.id'))
    cookies = Column(JSON, default=[])
    is_registered = Column(Boolean)
    is_withdraw_address_set = Column(Boolean)
    is_withdraw_whitelist_enabled = Column(Boolean)
    is_withdraw_only_to_whitelist = Column(Boolean)
    is_blocked_new_whitelist_address = Column(Boolean)
    is_2fa_enabled = Column(Boolean)
    is_password_changed = Column(Boolean, default=False)
    balance = Column(Float)
    uta_balance = Column(Float)
    funding_balance = Column(Float)
    kyc_level = Column(Integer)
    withdraw_wallet_private_key = Column(String)
    last_ts_registered = Column(String)
    is_ts_completed = Column(Boolean)
    has_ts_mark = Column(Boolean)
    first_deposit_date = Column(Date)
    deposit_amount = Column(Float, default=0)
    trading_volume = Column(Float, default=0)

    email = relationship("Email", backref="bybit_accounts")
    proxy = relationship("Proxy", backref="bybit_accounts")

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if value:
                setattr(self, key, value)

    def __repr__(self):
        info: str = f'BYBIT_acc id = {self.bybit_id}, email = {self.email}'
        return info

    '''@staticmethod
    def get_random_user_agent():
        software_names = [SoftwareName.CHROME.value]
        operating_systems = [OperatingSystem.WINDOWS.value]

        user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)

        # Get list of user agents.
        #user_agents = user_agent_rotator.get_user_agents()

        # Get Random User Agent String.
        user_agent = user_agent_rotator.get_random_user_agent()

        return user_agent'''

    @staticmethod
    def get_random_user_agent():
        r1 = random.randint(120, 130)
        r2 = random.randint(0, 130)
        r3 = random.randint(0, 130)
        r4 = random.randint(0, 130)
        chrome_version = f'{r1}.0.{r3}.{r4}'
        user_agent = f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version} Safari/537.36'

        return user_agent