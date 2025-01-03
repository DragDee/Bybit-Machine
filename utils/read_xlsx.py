import time

import openpyxl
from sqlalchemy.orm import joinedload

from models.email import Email
from models.bybit_account import BybitAccount
from models.proxy import Proxy
from models.database import async_session
import asyncio
from sqlalchemy import select
from data.config import ROOT_DIR
import os


#xlsx_name = ROOT_DIR + '/Kerkala.xlsx'
xlsx_name = os.path.join(ROOT_DIR, 'Accounts.xlsx')

def parse_proxy(proxy_str: str):
    try:
        parsed_proxy = proxy_str.split(':')
    except Exception as ex:
        print(ex)
        parsed_proxy = ['', '', '', '', '']

    return parsed_proxy


async def read_excel(start=2, finish=2):
    book = openpyxl.open(xlsx_name, read_only=True)
    sheet = book.worksheets[0]

    for row in range(start, finish):
        bybit_id = sheet[row][0].value
        mail_imap = sheet[row][1].value
        mail_imap_password = sheet[row][2].value
        bybit_password = sheet[row][3].value
        parsed_proxy = Proxy.parse_proxy(sheet[row][4].value)
        group_name = sheet[row][5].value
        google_auth = sheet[row][6].value
        withdraw_wallet_prvt_key = sheet[row][7].value
        is_registered = sheet[row][8].value

        bybit_password = mail_imap_password if not bybit_password else bybit_password
        group_name = 'Default group' if not group_name else group_name
        is_registered: bool = True if is_registered == 1 else False

        print(bybit_id, mail_imap, mail_imap_password, bybit_password)

        async with async_session() as session:
            email = Email(mail_imap, mail_imap_password)
            session.add(email)
            await session.commit()

            proxy = Proxy(
                 ip=parsed_proxy[1],
                 port=parsed_proxy[2],
                 proxy_login=parsed_proxy[3],
                 proxy_password=parsed_proxy[4],
                 proxy_type=parsed_proxy[0])

            session.add(proxy)
            await session.commit()



            bybit_acc = BybitAccount(
                email_id=email.id,
                proxy_id=proxy.id,
                bybit_id=bybit_id,
                password=bybit_password,
                totp_key=google_auth,
                withdraw_wallet_private_key=withdraw_wallet_prvt_key,
                user_agent=BybitAccount.get_random_user_agent(),
                group_name=group_name,
                is_registered=is_registered
            )
            session.add(bybit_acc)
            await session.commit()


if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(read_excel())