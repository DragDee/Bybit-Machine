import imaplib
import ssl
from imaplib import IMAP4, IMAP4_SSL_PORT, IMAP4_PORT
import email
from email import utils
from email.header import decode_header
import re

import time
from email.utils import parsedate_to_datetime

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from models.bybit_account import BybitAccount
from models.database import async_session
from models.email import Email
from models.proxy import Proxy

import socks
import socket

from socks import create_connection
from socks import PROXY_TYPE_SOCKS4
from socks import PROXY_TYPE_SOCKS5
from socks import PROXY_TYPE_HTTP

from imaplib import IMAP4


from imaplib import IMAP4, IMAP4_SSL, IMAP4_PORT, IMAP4_SSL_PORT
from socks import PROXY_TYPE_SOCKS4, PROXY_TYPE_SOCKS5, PROXY_TYPE_HTTP




class SocksIMAP4(IMAP4):
    def set_proxy(self, proxy: Proxy):
        self.proxy = proxy

    def open(self, host, port=IMAP4_PORT, *args):
        self.host = host
        self.port = port
        self.sock = socks.socksocket()
        self.sock.set_proxy(PROXY_TYPE_SOCKS5,
                            self.proxy.ip,
                            self.proxy.port,
                            self.proxy.proxy_login,
                            self.proxy.proxy_password)
        self.sock.connect((host,port))
        self.file = self.sock.makefile('rb')



class Mail:
    #imap_server = 'imap.rambler.ru'
    imap_server = 'imap.gmx.com'
    port = 993

    allowed_time_spread = 121

    def __init__(self, email: Email):

        '''proxy_socket = socks.socksocket()
        proxy_socket.set_proxy(socks.SOCKS5,
                               proxy.ip,
                               proxy.port,
                               proxy.proxy_login,
                               proxy.proxy_password,)
        proxy_socket.connect((self.imap_server, self.port))'''

        '''socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,
                              proxy.ip,
                              proxy.port,
                              proxy.proxy_login,
                              proxy.proxy_password)
        socket.socket = socks.socksocket'''


        self.mail = imaplib.IMAP4_SSL(self.imap_server, port=self.port)
        #self.mail = SocksIMAP4(self.imap_server, port=self.port)
        '''self.mail.set_proxy(proxy=proxy)'''
        '''self.mail.sock = proxy_socket'''
        self.mail.login(email.imap_login, email.imap_password)

    def get_mail_sender_from_msgdata(self, msg_data) -> str:
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                # Парсим сообщение в объект email
                msg = email.message_from_bytes(response_part[1])

                from_ = msg.get("From")
                print(f"От кого: {from_}")
                return from_

    def get_date_from_msg_data(self, msg_data):
        msg = self.get_msg_from_msgdata(msg_data)
        date_str = msg['Date']

        email_date = parsedate_to_datetime(date_str)

        if email_date is not None:
            timestamp = email_date.timestamp()
            return timestamp

    def get_msg_from_msgdata(self, msg_data):
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                return msg

    def code(self, folder: str):
        time0 = int(time.time()) - self.allowed_time_spread
        try:
            last_msg_data = self.get_lasts_mail_msgdata(folder)
            mail_body = self.get_mail_body_from_msgdata(last_msg_data)
            subject = self.get_subject_from_msgdata(last_msg_data)
        except:
            return None



        if not subject:
            print('Тему письма не удалось получить')
            return None

        if '[Bybit]' in subject:
            print("Найдено письмо с нужной темой")
            date = int(self.get_date_from_msg_data(last_msg_data))

            if date < time0:
                print('данное письмо не подходит по времени')
                return None

            code = self.find_code_in_text(str(last_msg_data))
            return code

    def get_last_mailcode(self, time_out: int = 60):
        i = 0
        folders = [
            'inbox',
            'Spam'
        ]

        time1 = time.time()
        time2 = time1
        code = self.code(folders[i])

        while not code and time2 - time1 <= time_out:
            print(f'письмо пока не нашли')
            time2 = time.time()
            i += 1
            ost = i % 2

            code = self.code(folders[ost])

            time.sleep(1)

        self.mail.logout()

        if not code:
            print("За установленное время не удалось найти код")
            return None

        print(code)
        return code

    def get_lasts_mail_msgdata(self, folder: str = 'inbox'):
        self.mail.select(folder)

        status, messages = self.mail.search(None, 'ALL')

        if not status:
            print('Произошла ошибка')
            return None

        # Получаем список номеров сообщений
        mail_ids = messages[0].split()

        if not len(mail_ids):
            print("По данному критерию писем не найденно ")
            return None

        last_id = mail_ids[-1]

        status, msg_data = self.mail.fetch(last_id, "(RFC822)")

        return msg_data

    def get_mail_body_from_msgdata(self, msg_data):
        body = ''

        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])

                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        if "plain" in content_type:
                            body = part.get_payload(decode=True).decode()
                            #print(f"Сообщение: {body}")
                else:
                    body = msg.get_payload(decode=True).decode()
                    #print(f"Сообщение: {body}")

        return body

    def get_subject_from_msgdata(self, msg_data):
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                # Парсим сообщение в объект email
                msg = email.message_from_bytes(response_part[1])

                # Декодируем тему письма
                try:
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else 'utf-8')

                except Exception as ex:
                    #print(ex)
                    return None

                return subject

    def print_mail_by_mailid(self, mail_id: str):
        body = ''

        self.mail.login(self.username, self.password)
        self.mail.select("inbox")

        status, msg_data = self.mail.fetch(mail_id, "(RFC822)")

        for response_part in msg_data:
            if isinstance(response_part, tuple):
                # Парсим сообщение в объект email
                msg = email.message_from_bytes(response_part[1])

                # Декодируем тему письма
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else 'utf-8')

                # Отправитель
                from_ = msg.get("From")

                print(f"Тема: {subject}")
                print(f"От кого: {from_}")

                # Если сообщение содержит текст, вытаскиваем его
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        if "plain" in content_type:
                            body = part.get_payload(decode=True).decode()
                            print(f"Сообщение: {body}")
                else:
                    body = msg.get_payload(decode=True).decode()
                    print(f"Сообщение: {body}")

        self.mail.logout()

        return body

    def find_code_in_text(self, text: str):
        pattern = r"\*(\d+)\*"
        pattern = r"\>(\d{6})\<"

        matches = re.findall(pattern, text)

        # Если совпадения найдены
        if matches:
            for match in matches:
                return match
        else:
            print("Число не найдено")
            return None



if __name__ == '__main__':

    #mail.mail.logout()
    '''t = mail.print_mail_by_mailid(mail_id='7')
    print(t)
    mail.find_code_in_text(t)'''

    #print(mail.get_mail_sender('3'))