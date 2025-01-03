import asyncio
import email.utils

import logging
import random
import string
from datetime import datetime, timedelta
from http.cookies import SimpleCookie
from operator import length_hint

import aiohttp
from Demos.FileSecurityTest import ace_no
from aiohttp import ClientTimeout
from aiohttp_socks import ProxyConnector
from ccxt.static_dependencies.marshmallow.fields import Decimal
from sqlalchemy.util import await_only
from twocaptcha import TwoCaptcha
import requests
import time
import json

from sqlalchemy.orm import joinedload
from sqlalchemy import select
from yarl import URL

from models.database import async_session
from models.networks import Networks
from models.networks_names import NetworksNames

from tasks.bybit import Bybit
from tasks.change_password_hashing import encrypt_string
from utils.mail import Mail
from utils.totp import get_onetime_code_from_secret_totp
from requests.utils import dict_from_cookiejar, cookiejar_from_dict
from urllib import parse
import urllib
from tasks.tg_bought_soft import generate_signature
from models.email import Email
from models.proxy import Proxy
from models.bybit_account import BybitAccount
from utils.web3_wallet import Web3Wallet

from data.config import TWO_CAPTCHA_KEY, MAIN_EVM_WALLET
from typing import Optional

from utils.login_name import generate_login_name
from tasks.get_encrypted_password import get_encrypted_pass_and_timestamp
import math
from utils.mail import Mail
from utils.get_current_date import get_current_date_formatted

from utils.new_signature import encrypt_signature
from web3_actions.client import Client
from web3_actions.collect_money_from_web3_wallets import WalletCollector
from decimal import Decimal


class BybitSetUp:
    #main_url = 'https://api2.bybit.com'
    main_url = 'https://api2.bybitglobal.com'
    common_url = 'https://api2.bybit.com'
    bybit_global_url = 'https://api2.bybitglobal.com'
    nl_bybit_url = 'https://api2.bybit.nl'

    def __init__(self, bybit_account: BybitAccount):
        self.bybit_account = bybit_account

        captcha_config = {
            'apiKey': TWO_CAPTCHA_KEY,
            'defaultTimeout': 120,
            'recaptchaTimeout': 600,
            'pollingInterval': 10,
        }

        self.solver = TwoCaptcha(**captcha_config)

    async def __aenter__(self):
        proxy: Proxy = self.bybit_account.proxy
        proxies = f'{proxy.proxy_type}://{proxy.proxy_login}:{proxy.proxy_password}@{proxy.ip}:{proxy.port}'

        jar = aiohttp.CookieJar()

        def unix_to_http_date(timestamp):
            dt = datetime.utcfromtimestamp(timestamp)
            return dt.strftime('%a, %d %b %Y %H:%M:%S GMT')

        for cookie in self.bybit_account.cookies:
            # print(cookie)
            simple_cookie = SimpleCookie()
            # jar.update_cookies({cookie['name']: cookie['value']}, response_url=URL('.bybit.com'))
            simple_cookie[cookie['name']] = cookie['value']
            morsel = simple_cookie[cookie['name']]

            '''if 'domain' in cookie and cookie['domain']:
                morsel['domain'] = cookie['domain']'''
            if 'path' in cookie and cookie['path']:
                morsel['path'] = cookie['path']
            if 'expirationDate' in cookie and cookie['expirationDate']:
                morsel['expires'] = unix_to_http_date(cookie['expirationDate'])
            if 'secure' in cookie and cookie['secure']:
                morsel['secure'] = True
            if 'httponly' in cookie and cookie['httponly']:
                morsel['httponly'] = True

            jar.update_cookies(simple_cookie,
                               # response_url=URL('bybit.com')
                               )

        connector = ProxyConnector.from_url(proxies)
        self.session = aiohttp.ClientSession(connector=connector, cookie_jar=jar)

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def update_cookies_file_old(self, new_cookies: dict):
        sign = 0
        to_delete = []

        # cookies = json.load(self.bybit_account.cookies)
        cookies = self.bybit_account.cookies

        for i in range(len(cookies)):
            for new_cookie_name, new_cookie_value in new_cookies.items():
                if cookies[i]['name'] == new_cookie_name:
                    cookies[i]['value'] = new_cookie_value
                    to_delete.append(new_cookie_name)

        for i in to_delete:
            del (new_cookies[i])

        for new_cookie_name, new_cookie_value in new_cookies.items():
            dic = {
                'name': new_cookie_name,
                'value': new_cookie_value
            }
            cookies.append(dic)

        # self.bybit_account.update(cookies=json.dumps(cookies))
        await self.bybit_account.update(cookies=cookies)

    async def update_cookies_file(self, new_cookies: list):
        sign = 0
        to_delete = []

        # cookies = json.load(self.bybit_account.cookies)
        cookies = self.bybit_account.cookies

        for i in range(len(cookies)):
            for new_cookie in new_cookies:
                if cookies[i]['name'] == new_cookie.get('name') and cookies[i]['domain'] == new_cookie.get('domain') and new_cookie.get('value'):
                    cookies[i]['value'] = new_cookie.get('value')
                    cookies[i]['domain'] = new_cookie.get('domain')
                    cookies[i]['expirationDate'] = new_cookie.get('expirationDate')
                    cookies[i]['path'] = new_cookie.get('path')
                    to_delete.append(new_cookie)

        for i in to_delete:
            if i in new_cookies:
                new_cookies.remove(i)

        for new_cookie in new_cookies:
            dic = {
                'name': new_cookie.get('name'),
                'value': new_cookie.get('value'),
                'domain': new_cookie.get('domain'),
                'expirationDate': new_cookie.get('expirationDate'),
                'path': new_cookie.get('path')
            }
            cookies.append(dic)

        # self.bybit_account.update(cookies=json.dumps(cookies))
        await self.bybit_account.update(cookies=cookies)
        #await self.dublicate_cookies()

    async def dublicate_cookies(self):
        cookies = self.bybit_account.cookies
        cookies_to_dubl = []

        for cookie in cookies:
            if cookie.get('domain') == "bybitglobal.com":
                dublicate_cookie = cookie.copy()
                dublicate_cookie['domain'] = "bybit.com"
                cookies_to_dubl.append(dublicate_cookie)

        for cookie in cookies_to_dubl:
            cookies.append(cookie)

        await self.bybit_account.update(cookies=cookies)

    def get_headers_v2(self, guid: Optional[str] = None):
        if not guid:
            guid = generate_login_name(str(time.time()))

        headers = {
            "accept": "application/json",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            # "content-length": "595",
            "content-type": "application/json;charset=UTF-8",
            "cookie": self.get_cookies_str(),
            "guid": guid,
            "lang": "ru-RU",
            "origin": "https://www.bybit.com",
            "platform": "pc",
            "priority": "u=1, i",
            "referer": "https://www.bybit.com/",
            "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "traceparent": "00-ca930c2a676508a0cc2b8827d719a5f4-9a57e7eba8ecb37c-00",
            "tx-id": "dmVyMQ|ZmE2OTMyYTgxNW0wenFyMzkweGFvcDJmMTVmZDQwNTll||==",
            "user-agent": self.bybit_account.user_agent,
            "usertoken": ""
        }

        return headers

    def get_headers(self):
        headers = {
            'User-Agent': self.bybit_account.user_agent,
            'Referer': 'https://www.bybit.com/',
            'Content-Type': 'application/json;charset=UTF-8',
            'authority': 'api2-2.bybit.com',
            'accept': 'application/json',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'ru-RU',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.bybit.com',
            'referer': 'https://www.bybit.com/',
            'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'cookie': self.get_cookies_str()
        }

        return headers

    def get_cookies_str(self) -> str:
        # cookies = json.load(self.bybit_account.cookies)
        cookies = self.bybit_account.cookies

        cookie_str = ''
        for cookie in cookies:
            if cookie:
                cookie_str += f"{cookie['name']}={cookie['value']}; "

        return cookie_str[:-1]

    async def enable_whitelist_withdraw(self):
        if self.bybit_account.is_withdraw_whitelist_enabled:
            print('Вл уже включён')
            return None

        print('Включаем вл')
        print(f'TOTP code is {self.bybit_account.totp_key}')
        site_key = '6LeNsZIUAAAAANOHTT1IaGp-RlIFHP2-YyaponYD'
        server = self.main_url + '/user/assets/money-address'
        email_server = '/send/email'
        whitelist_switcher_url = '/v3/private/cht/asset-withdraw/address/change-address-verification'

        if self.bybit_account.is_withdraw_whitelist_enabled:
            print('Вайтслист уже включен')
            return None

        proxy = self.bybit_account.proxy
        proxies = f'{proxy.proxy_login}:{proxy.proxy_password}@{proxy.ip}:{proxy.port}'

        print('Ждём верифа каптчи')
        captcha_res = await asyncio.to_thread(self.solver.recaptcha, site_key, url=server, proxy={
            'type': 'http',
            'uri': f'{proxies}'
        })

        print(captcha_res)

        res = await self.make_request(
            data={
                'email': self.bybit_account.email.imap_login,
                'type': 'recaptcha',
                'cnt': 0,
                'from': 20,
                'key_version': 'v2',
                'g_recaptcha_response': captcha_res['code']
            },
            url=self.bybit_global_url + email_server
        )
        print(res)

        mail_code = await asyncio.to_thread(Mail(self.bybit_account.email).get_last_mailcode)
        res = await self.make_request(
            data={
                "open": "true",
                "email_code": str(mail_code),
                "verification_code": str(get_onetime_code_from_secret_totp(self.bybit_account.totp_key))
            },
            url=self.bybit_global_url + whitelist_switcher_url
        )
        print(res)

        if res:
            await self.bybit_account.update(is_withdraw_whitelist_enabled=True)
            print('Белый список включен')

            await self.wait_for_2fa()

    async def parse_cookies(self):
        cookie_dict = {}
        for cookie in self.bybit_account.cookies:
            cookie_dict[cookie['name']] = cookie['value']

        return cookie_dict

    async def make_request(self,
                           url: str,
                           data: Optional = None,
                           method: str = 'post',
                           headers: Optional[dict] = None,
                           time_out=30,
                           update_cookies=True,
                           return_json=True,
                           usegovnosession=True,
                           cookies=None,
                           check_res=True
                           ):

        if not headers:
            headers = self.get_headers()

        try:
            # pass
            del headers['cookie']
        except:
            pass
        # headers = httpx.Headers(headers)

        # del headers['content-length']
        # new_cookie = await self.parse_cookies()
        # print(new_cookie)

        # self.client.cookies.update(self.bybit_account.cookies)

        func = getattr(self.session, method)

        args = {
            # 'proxies': proxies,
            'headers': headers,
            'url': url
        }
        if cookies:
            args['cookies'] = cookies

        if method == 'post':
            args['data'] = data
        else:
            args['params'] = data

        if time_out:
            args['timeout'] = time_out

        # print(self.client.cookies)

        # res = await func(**args)

        async with func(**args) as res:

            if update_cookies:
                cookie_list = []
                cookie_dict = {key: morsel.value for key, morsel in res.cookies.items()}

                for key, morsel in res.cookies.items():
                    # print(morsel.keys())
                    dict = {}
                    dict['name'] = key
                    dict['value'] = morsel.value
                    #dict['domain'] = morsel['domain']
                    dict['domain'] = 'bybit.com'
                    dt = email.utils.parsedate_to_datetime(morsel['expires'])

                    # Преобразование в Unix-временную метку
                    dict['expirationDate'] = dt.timestamp()
                    dict['path'] = "/"
                    dublicate_dict = dict.copy()
                    dublicate_dict['domain'] = 'bybitglobal.com'
                    cookie_list.append(dict)
                    cookie_list.append(dublicate_dict)

                # cookie_dict = {name: value for name, value in res.cookies.items()}

                await self.update_cookies_file(cookie_list)

            if check_res:
                if not await self.check_res(res):
                    return None

            if return_json:
                res = await res.json()

            return res

    async def check_res(self, res):
        if res.status // 100 != 2:
            print(await res.text())
            print("Произошла ошибка")
            return None

        try:
            res = await res.json()
            '''if res.get('ret_code') == 10007:
                print('необходимо залогиниться снова')
                await self.get_cookies(retries=1)
                return None'''

            if res.get('ret_code') != 0 and res.get('retCode') != 0:
                print(res)
                print('При запросе произошла ошибка')
                return None

        except Exception as ex:
            print(f"Произошло исключение = {ex}")
            print(await res.text())
            return None

        return True

    async def get_random_chain(self):
        chains_list = [
            'ARBI',

        ]

        return random.choice(chains_list)

    async def generate_address_add_to_whitelist(self):
        if self.bybit_account.is_withdraw_address_set:
            print("Кошелек для вывода уже установлен в вл")
            return None

        print('Генерируем веб3 кошель и устанавливаем его в вл')
        prvt_key = None
        web3_wallet = Web3Wallet(self.bybit_account)
        if not self.bybit_account.withdraw_wallet_private_key:
            prvt_key = await web3_wallet.generate_wallet_and_save_to_db()
            await self.renew_bybit_account()

        wallet_public_key = web3_wallet.get_pub_key_from_prvt(
            self.bybit_account.withdraw_wallet_private_key)
        wallet_public_key = str(wallet_public_key)
        print(wallet_public_key)
        chain = await self.get_random_chain()

        await self.add_address_to_whitelist(address=wallet_public_key, chain=chain)

        await self.wait_for_2fa()

    async def check_mark(self, ts_id: int):
        res = await self.make_request(
            data=json.dumps(
                {
                    'projectCode': str(ts_id)
                }),
            url=self.common_url + '/spot/api/deposit-activity/v1/project/pledge',
            check_res=False,
            headers=self.get_headers_v2()
        )

        print(res)

        if res['ret_code'] == 20007:
            print('На аккаунте метка')
            await self.bybit_account.update(has_ts_mark=True)
            return True

        return False

    async def add_address_to_whitelist(self, address: str, chain: str):
        url = '/user/public/risk/default-intercept'
        verify_url = '/user/public/risk/verify'
        components_url = '/user/public/risk/components'
        send_code_url = '/user/public/risk/send/code'
        address_create_url = '/v3/private/cht/asset-withdraw/address/address-create'
        sence = 30062

        string = '{"addresses":[{' + f'"coin":"baseCoin","address":"{address}","chain_type":"{chain}","is_verified":true,"address_type":0' + '}]}'
        encoded_str = urllib.parse.quote(string)  # преобразуем в url вид

        res = await self.make_request(
            data=
            {
                'sence': sence,
                'ext_info_str': encoded_str
            },
            url=self.main_url + url,
            method='post'
        )

        risk_token = res['result']['risk_token']

        res = await self.make_request(
            data={
                'risk_token': risk_token
            },
            url=self.main_url + components_url,
        )

        print(res)


        send_code_res = await self.make_request(
            data={
                'component_id': 'email_verify',
                'risk_token': risk_token
            },
            url=self.main_url + send_code_url
        )

        print('send code result')
        print(send_code_res)


        request_data = {
            'risk_token': str(risk_token),
            'component_list': {
                'email_verify': str(Mail(self.bybit_account.email).get_last_mailcode()),
                'google2fa': get_onetime_code_from_secret_totp(self.bybit_account.totp_key)
            },
        }
        request_data = json.dumps(request_data)

        headers = {
            "accept": "application/json",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "no-cache",
            "content-type": "application/json;charset=UTF-8",
            "gdfp": "dmVyMQ|MTNhZjg2Zjc1ZG0wem45aDJwd2pveTk2MTU5OTA4NDhl||v2:gRoG/yXpWm2/MGeG63YEkdYLXEQ4EtNeZfW8rLR0FZ5u6BqQCXuwtbyRy0n5ir4lL65xxddgNKP1YSdTpJtv2HJ+065T06PvrypRh7p+B9BmlfpR7aRY1dtIJcXyzoEaEcdXZUszmfRiNvXO3dLt+77canvB/Bb3sY/m0kHtNo9VKIUs5Hp/r3XJT8spo1qXof7l543jGbauupcOF/85lynby6Axj3wDMhK+YOCrbnjQ8lXmK8bb",
            "guid": "9fc624d9-32ae-2e30-65d7-557ed76d813e",
            "lang": "en",
            "origin": "https://www.bybit.com",
            "platform": "pc",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://www.bybit.com/",
            "sec-ch-ua": '"Not)A;Brand";v="99", "Opera GX";v="113", "Chromium";v="127"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "traceparent": "00-d170fedadc574f43f8c9d906e8287706-013d78b8fe41b5ae-01",
            "tx-id": "dmVyMQ|MTNhZjg2Zjc1ZG0wem45aDJwd2pveTk2MTU5OTA4NDhl||v2:gRoG/yXpWm2/MGeG63YEkdYLXEQ4EtNeZfW8rLR0FZ5u6BqQCXuwtbyRy0n5ir4lL65xxddgNKP1YSdTpJtv2HJ+065T06PvrypRh7p+B9BmlfpR7aRY1dtIJcXyzoEaEcdXZUszmfRiNvXO3dLt+77canvB/Bb3sY/m0kHtNo9VKIUs5Hp/r3XJT8spo1qXof7l543jGbauupcOF/85lynby6Axj3wDMhK+YOCrbnjQ8lXmK8bb",
            "user-agent": self.bybit_account.user_agent,
            "x-signature": generate_signature('', request_data),
        }

        res = await self.make_request(
            data=request_data,
            url=self.main_url + verify_url,
            headers=headers
        )
        print(request_data)
        print("Result of risk token verif")
        print(res)


        res = await self.make_request(
            data={
                'address': address,
                'address_type': 0,
                'chain_type': chain,
                'coin': "baseCoin",
                'is_verified': 'true',
                'risk_verified_result_token': risk_token
            },
            url=self.main_url + address_create_url
        )
        print(res)

        if res:
            await self.bybit_account.update(is_withdraw_address_set=True)

    async def wait_for_2fa(self):
        time_to_wait = 31
        print(f'Задержка {time_to_wait} секунд, чтоб google 2fa обновился')
        await asyncio.sleep(time_to_wait)

    def generate_random_password(self):
        length = random.randrange(10, 16)

        characters = string.ascii_letters + string.digits  # Включаем буквы и цифры
        random_string = ''.join(random.choice(characters) for _ in range(length))
        return random_string

    async def change_password(self):

        new_password = self.generate_random_password()
        res = await self.make_request(
            data={
                'old_password': encrypt_string(self.bybit_account.password),
                'password': encrypt_string(new_password),
                'samepassword': encrypt_string(new_password),
                'type': 'google2fa'
            },
            url= self.main_url + '/user/change/password'
        )

        print(res)
        if not res:
            print('При изменении пароля произошла ошибка')
            return False

        await self.bybit_account.update(password=new_password)
        print('Пароль изменён и сохранён в бд')
        await self.bybit_account.update(cookies=[])
        await self.bybit_account.update(is_password_changed=True)
        await self.renew_bybit_account()
        return True

    async def full_set_up(self, functions_list: list):
        print(functions_list)

        if 'change_password' in functions_list:
            await self.change_password()
            await self.get_cookies()
        if 'add_2fa' in functions_list:
            await self.add_2fa()
        if 'enable_whitelist_withdraw' in functions_list and self.bybit_account.totp_key:
            await self.enable_whitelist_withdraw()
        if 'generate_address_add_to_whitelist' in functions_list and self.bybit_account.totp_key:
            await self.generate_address_add_to_whitelist()
        if 'withdraw_via_whitelist_only' in functions_list and self.bybit_account.totp_key:
            await self.withdraw_via_whitelist_only()
        if 'block_new_withdraw_address' in functions_list and self.bybit_account.totp_key:
            await self.block_new_withdraw_address()

        return True

    async def withdraw_address_level(self, address_level: int):
        withdraw_address_level_url = '/user/private/change/withdraw-addr-level'
        res = await self.make_request(
            data={
                'email_code': '',
                'from': 0,
                'google2fa': str(get_onetime_code_from_secret_totp(self.bybit_account.totp_key)),
                'withdraw_addr_level': address_level
            },
            url=self.main_url + withdraw_address_level_url
        )
        print(res)
        return res

    async def withdraw_via_whitelist_only(self):
        if self.bybit_account.is_withdraw_only_to_whitelist:
            print('Вывод ТОЛЬКО на вл уже установлен')
            return None

        print('Настраиваем вывод ТОЛЬКО на вл адреса')
        address_level = 1
        res = await self.withdraw_address_level(address_level=address_level)
        if res:
            await self.bybit_account.update(is_withdraw_only_to_whitelist=True)

        await self.wait_for_2fa()

    async def block_new_withdraw_address(self):
        if self.bybit_account.is_blocked_new_whitelist_address:
            print('Блокирование вл уже установлено')
            return None

        address_level = 2
        res = await self.withdraw_address_level(address_level=address_level)
        if res:
            await self.bybit_account.update(is_blocked_new_whitelist_address=True)

        await self.wait_for_2fa()

    async def verify_risk_token_with_sign(self, risk_token: str, guid: Optional[str] = None):
        verify_url = 'https://api2.bybit.com/user/public/risk/verify'

        request_data = {
            'risk_token': str(risk_token),
            'component_list': {
                'google2fa': get_onetime_code_from_secret_totp(self.bybit_account.totp_key)
            },

        }
        request_data = json.dumps(request_data)

        headers = {
            "accept": "application/json",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "no-cache",
            "content-type": "application/json;charset=UTF-8",
            "gdfp": "dmVyMQ|==||==",
            "guid": "9fc624d9-32ae-2e30-65d7-557ed76d813e",
            "lang": "en",
            "origin": "https://www.bybit.com",
            "platform": "pc",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://www.bybit.com/",
            "sec-ch-ua": '"Not)A;Brand";v="99", "Opera GX";v="113", "Chromium";v="127"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "traceparent": "00-d170fedadc574f43f8c9d906e8287706-013d78b8fe41b5ae-01",
            "tx-id": "dmVyMQ|MTNhZjg2Zjc1ZG0wem45aDJwd2pveTk2MTU5OTA4NDhl||v2:gRoG/yXpWm2/MGeG63YEkdYLXEQ4EtNeZfW8rLR0FZ5u6BqQCXuwtbyRy0n5ir4lL65xxddgNKP1YSdTpJtv2HJ+065T06PvrypRh7p+B9BmlfpR7aRY1dtIJcXyzoEaEcdXZUszmfRiNvXO3dLt+77canvB/Bb3sY/m0kHtNo9VKIUs5Hp/r3XJT8spo1qXof7l543jGbauupcOF/85lynby6Axj3wDMhK+YOCrbnjQ8lXmK8bb",
            "user-agent": self.bybit_account.user_agent,
            "x-signature": generate_signature('', request_data),
        }
        if guid:
            headers['guid'] = guid

        res = await self.make_request(
            data=request_data,
            url=verify_url,
            headers=headers
        )

        return res

    async def get_deposit_address(self, coin: str = None, chain: str = None):
        deposit_address_url = 'https://api2.bybit.com/v3/private/cht/asset-deposit/deposit/address-chain'

        request_data_str = f"coin={coin}&chain={chain}"

        request_data = {
            'coin': coin,
            'chain': chain
        }

        headers = self.get_headers()
        headers["x-signature"] = generate_signature(request_data_str, '')

        res = await self.make_request(
            data=request_data,
            url=deposit_address_url,
            headers=headers,
            method='get'
        )

        print(res)

        try:
            chain_name = res['result']['chainName']
            address = res['result']['address']

            print(chain_name)
            print(address)

            return address
        except Exception as ex:
            print('При получении адресса депозита произошла ошибка, проверьте аргументы депозита, а так же уровень кус')
            return None


    async def get_kyc_level(self):
        profile_url = 'https://api2.bybit.com/v2/private/user/profile'

        res = await self.make_request(
            url=profile_url,
            method='get'
        )

        if not res:
            print('Произошла ошибка при получении уровня кус')
            return False

        #return res['result']['kyc_person_level'] if res else None

        await self.bybit_account.update(kyc_level=res.get('result').get('kyc_person_level'))
        return True

    async def register_in_TS(self, ts_id: int):
        pledge_url = 'https://api2.bybit.com/spot/api/deposit-activity/v1/project/pledge'

        '''headers = {
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "max-age=0, no-cache, no-store",
            "content-type": "application/json;charset=UTF-8",
            "lang": "en",
            "origin": "https://www.bybit.com",
            "platform": "pc",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://www.bybit.com/",
            "sec-ch-ua": '"Not)A;Brand";v="99", "Opera GX";v="113", "Chromium";v="127"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "accept": 'application/json, text/plain, */*',
            "accept-encoding": 'gzip, deflate, br, zstd',
            "content-length": '32',
            "traceparent": '00-633dc11a7a8c12d3346ae8f03e134234-de4a6b6d44ec30ba-00',
            "user-agent": self.bybit_account.user_agent,
        }'''

        print(ts_id)

        res = await self.make_request(
            data=json.dumps(
                {
                    'projectCode': str(ts_id)
                }),
            url=pledge_url,
            headers=self.get_headers_v2()
        )

        print(res)

        if not res:
            return False

        await self.bybit_account.update(last_ts_registered=ts_id)
        return True

    async def wait_until_captcha_res(self,
                                     prox,
                                     captcha_id='21d26fa4b7436365b69dc79ca52ff627',
                                     url='https://www.bybit.com/ru-RU/login'):

        captcha_res = await self.captcha_result(captcha_id, url, prox)
        retries = 5

        while not captcha_res and retries > 0:
            captcha_res = await self.captcha_result(captcha_id, url, prox)
            retries -= 1

        return captcha_res

    async def captcha_result(self, captcha_id, url, prox):
        try:
            captcha_res = await asyncio.to_thread(self.solver.geetest_v4, captcha_id=captcha_id, url=url, proxy=prox)
            return captcha_res
        except Exception as ex:
            print(f'При получении каптчи произошло исключение {ex}')
            return None

    async def check_login_cookies(self):
        res = await self.make_request(
            url=self.main_url + '/user/private/profile-v2',
            method='get',
            check_res=True
        )
        if not res:
            return False

        return True

    async def get_cookies(self, retries=3):

        if await self.check_login_cookies():
            print('Куки все еще валидны, логин не нужен')
            return True

        print('Начинаю получение куки')
        login_res = await self.login()

        while not login_res and retries > 0:
            retries -= 1
            login_res = await self.login()

        if login_res:
            print('Логин прошел успешно')
            return True

        return False

    async def captcha_order(self, login_name: str, scene: str):
        order_url = '/user/magpice/v1/captcha/order'
        # order_url = 'https://api2.bybit.nl/user/magpice/v1/captcha/order'

        res = await self.make_request(
            data={
                'country_code': "",
                'login_name': login_name,
                'scene': scene,
                'txid': "",
            },
            url=self.main_url + order_url
        )

        print(res)
        return res

    def get_proxy_for_2captcha(self) -> dict:
        proxy = self.bybit_account.proxy
        prox = {'type': f'{proxy.proxy_type.upper()}',
                'uri': f'{proxy.proxy_login}:{proxy.proxy_password}@{proxy.ip}:{proxy.port}'}

        return prox

    async def verify_captcha(self, captcha_code, login_name: str, serial_no: str, scene: str):
        captcha_verify_url = '/user/magpice/v1/captcha/verify'
        # capthca_verify_url = 'https://api2.bybit.nl/user/magpice/v1/captcha/verify'

        headers = self.get_headers()
        headers['guid'] = login_name

        res = await self.make_request(
            data={
                'captcha_output': captcha_code['captcha_output'],
                'captcha_type': 'gee4captcha',
                'gee4test_gen_time': captcha_code['gen_time'],
                'login_name': login_name,
                'lot_number': captcha_code['lot_number'],
                'pass_token': captcha_code['pass_token'],
                'scene': scene,
                'serial_no': serial_no
            },
            url=self.main_url + captcha_verify_url,
            headers=headers,
            usegovnosession=True
        )

        return res

    async def login_request(self, login_name, serial_no, risk_token: Optional[str] = None):
        login_url = '/login'
        # login_url = 'https://api2.bybit.nl/login'
        encrypted_password, timestamp = get_encrypted_pass_and_timestamp(password=self.bybit_account.password)

        headers = {
            "accept": "application/json",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            # "content-length": '608',
            # 'Transfer-Encoding': 'chunked',
            "content-type": "application/json;charset=UTF-8",
            "cookie": self.get_cookies_str(),
            "guid": login_name,
            "lang": "ru-RU",
            "origin": "https://www.bybit.com",
            "platform": "pc",
            "priority": "u=1, i",
            "referer": "https://www.bybit.com/",
            "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "traceparent": "00-a2526579be34635c8f7c6dcdd72714d9-a63900bca76450df-00",
            "tx-id": "dmVyMQ|MWM5YzE0M2EyY20wejNkMDZ5anhiOGM2Yjg1MTUwY2Y4||==",
            "user-agent": self.bybit_account.user_agent,
            "usertoken": ""
        }

        data = {
            'encrypt_password': encrypted_password,
            'encrypt_timestamp': str(timestamp),
            'magpie_verify_info': {
                'scene': '31000',
                'token': serial_no,
            },
            'proto_ver': '2.1',
            'username': self.bybit_account.email.imap_login
        }

        if risk_token:
            data['google2fa'] = str(get_onetime_code_from_secret_totp(self.bybit_account.totp_key))
            data['risk_token'] = risk_token,

        data = json.dumps(data)

        try:
            res = await self.make_request(
                url=self.main_url + login_url,
                data=data,
                headers=headers,
            )

            print(res)
            # risk_token = res['result']['risk_token']
            return res['result']['risk_token'] if not risk_token else res

        except Exception as exep:
            print(f"Произошло исключение = {exep}")
            return None

    async def register_manager(self, ref_info: Optional[dict] = None):
        print(ref_info)
        retries = 3

        if self.bybit_account.is_registered:
            print('Аккаунт уже зарегистрирован')
            return True

        print('Начинаю регистрацию')
        register_res = await self.register(ref_info)

        while not register_res and retries > 0:
            retries -= 1
            register_res = await self.register(ref_info)

        if register_res:
            return True

        return False

    async def register(self, refferal_info: Optional[dict] = None):

        await self.get_abck_cookie_register()
        scene = '31004'

        login_name = generate_login_name(email=self.bybit_account.email.imap_login)
        res = await self.captcha_order(login_name=login_name, scene=scene)
        if not res:
            return False
        serial_no = res['result']['serial_no']

        print("Ждём получения решения по каптче")
        captcha_res = await self.wait_until_captcha_res(self.get_proxy_for_2captcha(), url='https://www.bybit.com/en/register')
        captcha_code = json.loads(captcha_res['code'])
        print(captcha_res)

        await self.update_cookies_file(
            [
                {
                    'name': '_by_l_g_d',
                    'value': login_name
                },
                {
                    'name': 'deviceId',
                    'value': generate_login_name(str(time.time()))
                }
            ]
        )

        from yarl import URL
        self.session.cookie_jar.update_cookies({'_by_l_g_d': login_name}, response_url=URL('bybit.com/'))

        self.session.cookie_jar.update_cookies({'deviceId': generate_login_name(email=str(time.time()))},
                                               response_url=URL('bybit.com/'))

        print('Верификация капчи')
        res = await self.verify_captcha(captcha_code=captcha_code, login_name=login_name, serial_no=serial_no,
                                        scene=scene)
        print(f'Верификация капчи {res}')

        default_intercept_url = '/user/public/risk/default-intercept'


        default_intercept = await self.make_request(
            data=json.dumps({
                'ext_info': {
                    'userName': self.bybit_account.email.imap_login
                },
                'sence': '30002'
            }),
            url=self.main_url + default_intercept_url,
            headers=self.get_headers_v2(guid=login_name)
            # headers=headers
        )
        print('default_intercept')
        print(default_intercept)
        risk_token = default_intercept.get('result').get('risk_token')

        email_url = '/verify/register/email'
        email_res = await self.make_request(
            data=json.dumps({
                'email': self.bybit_account.email.imap_login,
                'from': 1,
                'is_fake': 'false',

                'location_link': "https://www.bybit.com/en/login" if not refferal_info
                    else f"https://www.bybit.com/sign-up?affiliate_id={refferal_info['affilate_id']}"
                         f"&group_id={refferal_info['group_id']}&group_type={refferal_info['group_type']}"
                         f"&ref_code={refferal_info['affilate_id']}",

                'magpie_verify_info': {
                    'scene': scene,
                    'token': serial_no
                },
                'ref': '' if not refferal_info else str(refferal_info['affilate_id']),
                'type': 'geecaptcha'
            }),
            url=self.main_url + email_url,
            headers=self.get_headers_v2(guid=login_name)
        )

        print(email_res)
        if not email_res:
            return False

        encrypted_password, timestamp = get_encrypted_pass_and_timestamp(password=self.bybit_account.password)
        last_refresh_time = get_current_date_formatted()
        ext_json = '{\"original_referrer\":\"www.bybit.com/en/login\",\"original_source\":\"bybit.com\",\"original_medium\":\"other\",\"original_last_url\":\"https://www.bybit.com/en/register\",\"original_last_refresh_time\":\"' + f'{last_refresh_time}' + r'\"}'

        email_url = '/register/email'

        data = {
            'email': self.bybit_account.email.imap_login,
            'emailverify': Mail(self.bybit_account.email).get_last_mailcode(),
            'encrypt_password': encrypted_password,
            'encrypt_timestamp': str(timestamp),
            'ext_json': ext_json,
            'from': 1,
            # 'g': generate_login_name(str(time.time())),
            'g': '6870d933-3a2c-b6a9-f228-8f163699c228',
            'lang': 'en',
            'last_refresh_time': last_refresh_time,
            'location_link': "https://www.bybit.com/en/login",
            'medium': "direct",
            'risk_token': risk_token,
            'url': "https://www.bybit.com/en/register",
            'user_code': ''
        }

        if refferal_info:
            data = {
                'affiliate_id': str(refferal_info['affilate_id']),
                'email': self.bybit_account.email.imap_login,
                'emailverify': Mail(self.bybit_account.email).get_last_mailcode(),
                'encrypt_password': encrypted_password,
                'encrypt_timestamp': str(timestamp),
                'from': 1,
                # 'g': generate_login_name(str(time.time())),
                'g': '6870d933-3a2c-b6a9-f228-8f163699c228',

                'group_id': str(refferal_info['group_id']),
                #'group_type': str(refferal_info['group_type']),

                'lang': 'en',
                'last_refresh_time': last_refresh_time,

                'location_link': f"https://www.bybit.com/sign-up?affiliate_id={refferal_info['affilate_id']}"
                         f"&group_id={refferal_info['group_id']}&group_type={refferal_info['group_type']}"
                         f"&ref_code={refferal_info['affilate_id']}",

                'medium': "affiliate",
                'risk_token': risk_token,
                'url': f"https://www.bybit.com/sign-up?affiliate_id={refferal_info['affilate_id']}"
                         f"&group_id={refferal_info['group_id']}&group_type={refferal_info['group_type']}"
                         f"&ref_code={refferal_info['affilate_id']}",
                'user_code': str(refferal_info['affilate_id'])
            }
            if refferal_info['group_type']:
                data['group_type'] = str(refferal_info['group_type'])


        register_res = await self.make_request(
            data=data,
            url=self.main_url + email_url,
        )
        print(register_res)

        if register_res:
            await self.bybit_account.update(is_registered=True)
            return True

        return False

    async def renew_bybit_account(self):
        #self.bybit_account = (await self.bybit_account.get(id=self.bybit_account.id))[0]
        print('Обновляем обект self.bybit_account')

        async with async_session() as session:
            query = (
                select(BybitAccount).options(joinedload(BybitAccount.proxy)).options(joinedload(BybitAccount.email)).
                where(BybitAccount.id == self.bybit_account.id)
            )

            res = await session.execute(query)
            result = res.unique().scalars().all()

            self.bybit_account = result[0]

    async def add_2fa(self):
        if self.bybit_account.totp_key:
            print('Google 2fa уже установлен')
            return None

        print('Начинаем установку 2фа')
        info_res = await self.make_request(
            url='https://api2.bybitglobal.com/google2fa/info',
            method='get'
        )
        print(info_res)

        if not info_res:
            print('Произошла ошибка при получении totp secret key')
            return False

        totp_key = info_res.get('result').get('secret')

        default_intercept = await self.make_request(
            data={
                'sence': '60004'
            },
            url='https://api2.bybitglobal.com/user/public/risk/default-intercept'
        )
        print(default_intercept)
        risk_token = default_intercept.get('result').get('risk_token')

        components = await self.make_request(
            data={
                'risk_token': risk_token
            },
            url='https://api2.bybitglobal.com/user/public/risk/components'
        )
        print(components)

        code = await self.make_request(
            data=json.dumps({
                'component_id': 'email_verify',
                'risk_token': risk_token
            }),
            url='https://api2.bybitglobal.com/user/public/risk/send/code',
            headers=self.get_headers_v2()
        )
        print(code)
        email_code = await asyncio.to_thread(Mail(self.bybit_account.email).get_last_mailcode)
        email_code = str(email_code)

        data = json.dumps({
            'component_list': {
                'email_verify': email_code
            },
            'risk_token': risk_token
        })

        headers = self.get_headers_v2()
        headers['x-signature'] = generate_signature('', data)
        verify = await self.make_request(
            data=data,
            url='https://api2.bybitglobal.com/user/public/risk/verify',
            headers=headers
        )
        print(verify)

        bind = await self.make_request(
            data={
                'code': str(get_onetime_code_from_secret_totp(totp_key)),
                'risk_token': risk_token,
                'secret': totp_key
            },
            url='https://api2.bybitglobal.com/google2fa/bind'
        )

        print(bind)

        if bind:
            await self.bybit_account.update(totp_key=totp_key)
            print('2fa сохранён')

            await self.wait_for_2fa()
            await self.renew_bybit_account()


    async def login(self):
        scene = '31000'

        login_name = generate_login_name(email=self.bybit_account.email.imap_login)

        await self.get_abck_cookie_register()

        res = await self.captcha_order(login_name=login_name, scene=scene)
        serial_no = res['result']['serial_no']

        print("Ждём получения решения по каптче")
        captcha_res = await self.wait_until_captcha_res(self.get_proxy_for_2captcha())
        captcha_code = json.loads(captcha_res['code'])
        print(captcha_code)
        # captcha_code = {'captcha_id': '21d26fa4b7436365b69dc79ca52ff627', 'lot_number': '4c32929577174d3e8489afead3f7e46a', 'pass_token': '89253c61f8fa4527a0f03e962c14a7ad0292fb2dc6d050bb7aa31a8aa55aa40b', 'gen_time': '1729788147', 'captcha_output': 'gbHPeiNhRJ70zq4U1oqu80y9Aw2brutnFtZ8szWIUJmTBqR3HwHobAITTY3v7t7QFUQkgQrl6ksazZ48jmieGcQARzncZ24T4myy_if8XdhwjQCemwyUea2kgX-e_QcsX3g4Y3sGfZ1KimVPG8GCzTdNIO_x63g-I48nTFGnWsLT26MrmMOdnxrH1-pP2VIoHHJpRc3XdkX38pzRGz_lWkDWnhjukNEqmhHFLSTAzHUmln3V62BzHVd5QAMLAphsLM7hyAWWuvV-u-2p_K_mWIAPhiowbopgig91OuyD4PDR65f2TJju7pcy_9YrbvQEV6u84kWiB64zqU52DwQXoDnPUHCrXpxsg2eIKnZnRRsJaJUa-CvGnBrljDbZEuNZlooJpzgV2BV_ccV4jMpsk1sMvfuiwHf8CW7hWqCPRWzU7y8TAHoo77AutHFl7AfV'}

        await self.update_cookies_file(
            [
                {
                    'name': '_by_l_g_d',
                    'value': login_name
                },
                {
                    'name': 'deviceId',
                    'value': generate_login_name(str(time.time()))
                }
            ]
        )

        print('Верификация капчи')
        res = await self.verify_captcha(captcha_code=captcha_code, login_name=login_name, serial_no=serial_no,
                                        scene=scene)
        print(res)

        risk_token = await self.login_request(login_name=login_name, serial_no=serial_no)
        if not self.bybit_account.totp_key:
            #return risk_token
            return True

        if not risk_token:
            return None

        components_url = '/user/public/risk/components'
        # components_url = 'https://api2.bybit.nl/user/public/risk/components'

        res = await self.make_request(
            data={
                'risk_token': risk_token
            },
            url=self.main_url + components_url
        )

        print(res)

        res = await self.verify_risk_token_with_sign(risk_token, login_name)
        print('Результат верифа риск токена')
        print(res)

        res = await self.login_request(login_name=login_name, serial_no=serial_no, risk_token=risk_token)

        return True if res else None

    async def get_abck_cookie(self):
        print("получаем abc куки")
        res = await self.make_request(
            url='https://www.bybit.com/ZgcU8M/4_YMf/r-C1U/RA/k3huVLt8aSJXEi/PxVSYg/NWYXX0/B6U2AB',
            data=json.dumps({
                "sensor_data": "2;0;3159348;3421253;13,0,0,1,2,0;:d&,ld1g:83.ji4v/_RHw9$gvk*z&}*nN|GLFb6v[@(vH7v_:#IFv>U-]$D<]Q#ja1_`d6LFkD9I%0i{Nv)|W&~r };;`eg^d:hmpLye=W>U;0z}Kp!YFigoCQi!F7C%(gAfxTefC~dkMYZ Xim(Y=GBUc7Bcy5/>oWt~g>5||)<;J69oSb~cSK?_tKk&HhokW/RpP .|>8MJe][8 BhM0:C7O>}EUiqv.q/.r)%q1Adry~+~Zp?,z-0Zy]~[o~O_`:e+|f`o+6Uw3$;}t?[YKk GcJvRpGSrxc,SN:M]}.R^6;=4#Q&&l3X*A/^HiDiz3&J~zr$|YeHM&7RH9j8/-UtTwcF3Y>^yxue5:2=T+Gy.[x75@q9XI~8sSA{i=+Hqz&j;/7esBhIy8b|2&`d%>Z0sDdH;tM{x=J#j{ U?%vd,l1[U3}uGZ5L&&z^LLhBuwvvMHrG)u>2K=Tp&XE4C`taI)( #XK-h~1%t&3h@}I:nbyJd ``r9u4:#q;1 %wTs$a{05Hs#a=,f5/$:TLfN<b`8xDiU_O&1Wa 63<gmtC,pKBphh#dJ.5]+L1Wx7CCoKeJ$)8/ pQ4:LabrYjbJycp7A@|&@g&vtLX9MUx@{Xm6EU(8)n/teX:fKkVvwI9Hmm|@fA=Ye#&#tdKh,=JlNaMMTHK%=;fikVx<wAs]8gDlez3CpghtHhZ3@jMt!A.5#T`Rd%D4<rh8vhB.?jU=lA_bv5Ti1GU7fPCzh h!+Ek/$xff+j$6U K-w x>B-$br|ZYhRW;&8b?feI%?_mU?N*AvLji{[1TT$f,WeFEswd4!{vJ-sQ?p>Vy9OJ=RPo77=hA|;C>lyQ/,=BP(~*wXb,&{mGbLocp_dY0.V/ETXh3=U;+8(M+f,S@-*kcO7>0nC[1lNA/):5gr?9a]!$Uaca[%RKCS2#LXq_`K%8Y2f.j|B<B!fki@eJ#&_tfTxYq+nFO[x9rA~K(Gp$(dBTdBdX60qkB;mFQjL%i(E(+B3aUj4?SH&1W bW$-%(`G,b&2zf{-]{lI<bFsV[y]Hl#g=0& wxriC{7XB9Ij?nX8&_S&R]-vq/U8xvRdcqQR5{Ieh^w/oQ1ofQAePv?%~HnUHJ6?-!TN)!Mnjg<S?r_FO5#T8t+?.X*s^hf}(.!?wm>lt#<fH)+{tao=@Syz&_%(w0)5=_bqJ&c;_uAPBuQ07~7wz<YkvV,&p$/Ob$}x{gPMZU3gk;I=LKO@*bJS^?m~x37esHMgZhE}<G(`b@IShSaV^$|!F(Ugj 8jxYgsw%tEj{pD7:BVbXnhoB(HaF6(*E/_mBf$*=pBcM5m}u&3ZTto{WIm,o`v!McBj:X5,P@xGig=RSvi?!ACScMn8+%B?v@#>zMw,G4,Xzxk)y5Nu3OThIJo==;QvBxWo5!ez/4-b%+| E_%QW00G;FnNCEj$^!lH9[w5h]``*+c$7qeRY-P Qk<6{{[L)<iB(`I:>25r^IK|(l,ZVU~8:C+p/vb0dDLSM.+~setY_8Lj= kn:,r?o+,I`fHy^Fh$uqLEAS6,q:)|s*N5h9^o{rK9pGFoA+Y49imx5[@Jx(8W~m<vX:cEBaHD[oW-3ujeiQK|b C97HP)ZPtp<5_5Oa^[!+(Z]IA=C8F)Y+?G@^nD0qeS~k?/@oUT(F0h#k.|}z/oNqEAA_!fD9s~eZ+x=hZY.DJ0J77CX`cRBpEA:d/taU;<&(gQsGQLu4F2E8Ta$!++uU$#&U0(YhFkPI.yWq}&sFB5@Jr~.<POEsSbu=wn]ZG`N_W5lR`aB)-{4>gs?M]a[K!:D$NUEVHdavS[8z$5q]jWz9fs8JotyaIh%J2<215RTiXjG{7UA$64dtUhEVov&oYz2}Xl`k|AKiM=(mQdQ>Zc7X(D|;p{}ng)MBq+0IGs%C=#p.Phg]r LkJm[q@Wxmd LM)ANvuL^2211$Quci}Gn*|I4I G[[K,MF@SO}GowH_s^l.vdXy>y?&eVvSzD,@`;;8Ne?S$Gi}A;;qKKM{4+X4m_5!>bwlH%a_y4u|e1`qA83qO`b<XWAA y;0W:2F+fio8W|X.bBNz}-iMZy7lZ2.%tT@hOWxN,69v7m@~M0P|.9%u48rKE{t`fAAiB_w[Fgt>nM1q6!P#1O.%F^-nkXS?J:BnCf)z_y+t)wXStiFs G3%@cN84m}t&tyR=^.$d0P E;({aQnbxI0,Q*l>DCSDR"})
        )

        print(res)

        await self.check_login_cookies()

    async def get_abck_cookie_register(self):
        print("получаем abc куки")
        #'https://www.bybit.com/nJc9VnQQUuWDiSlkZY9z/t7ifNLcpf7JLit/FAxyGwE/FVJ1Enp-/QjcB'
        res = await self.make_request(
            url='https://www.bybitglobal.com/nJc9VnQQUuWDiSlkZY9z/t7ifNLcpf7JLit/FAxyGwE/FVJ1Enp-/QjcB',
            data=json.dumps({
                "sensor_data": "2;0;4473158;4473138;8,1,0,2,2,23;+$2sRrvd@F-4@]VeKa5t9P<u!0Ra/K$4]MoTDaoT+72VMbm&)2cRu*9_r11e<eBJ(%23!2Y@=G7VR~{FZE56IzVNe&<e.fGTaPohaBfA [^xTPbs[{aM8g[WS[x)` yKQ)_y^-<hQ&a1#)iXt|w1?],(33DU*SoAd^s3IX30 VQu605K2r.hS;qDBTEPvx&[PvZ3s}p|eW&|&VPGKv/$MPf`a0osk/=B=SzF:}d}2<V7V&XrW lwm?+HAL0}h-&&:y*?-vNnG39UWH${pPcO[D7Ha<9kY:G[[4RPk c|H^b7 v;)e*0Jma6=,We*K]uY(tu]Gcnfa<`*{d%*614VsOHgaZU=Q54Y.5VOBxU(:SfD%k&Z e9)S%A^pXcn%}yuN~Ij#uWLRqg>bS^X*5y3WM9na50lmvCkGq^$nhk| %cr;b@,,c1d&]2}OEN.k.e_0E[%[kP.1TQ<41xkY{}heg?11)~e2@4*{nm3G03;?Be>:lSrwiu(4d_[Gk-v//0bR=w}EVP-IPB38[EVN<yNixV3Q<bj9It!@GN%o08~ZLLZP{m hoZ-Bk@73<]{QX1@qq|(KxzgW&7^d!)3H7qga1+m~|N`Nk@_z.;-w<Y:(46VMq|D<N-!pg]I_wC_,iDW{:M=Ai)%Svz=Io~=PXCaO+}r9E*D%z%L,9eJOtE50=K #Tj;>,&Bi;m$+GRvQ*h=!BcTS+U]Fa <XDRw3,4Vg<O.e/fW&fU[^~WW]+ikg +n)c-W` 29lH?U~A(eG3{[Mg20@#Y`i1NzN5N&@epyW*AHzL@teLK!l2n(1aX_l?M*[:iAe8>M(r.pJo5ssc/J[mA)?~=x[X 9kON;%Yh~>L9Qce8K&^a]!ygl> r,9A5R+Oym;t#o/zDPM}vuQ_bIT(}YHD;YwJ~wSAwaCtAW><e-kPV;WO_xJ1t:qdf!>+YS*{iT5u/[TFxR7(}~,I;7Him0@MP<QD{x`hNK%f(UXT)SHDQGU^$v7xzKht!FjT@D$BwwVY(]Q[%^gRhgw9XNfTK*eivK}nYXKTK_<4UK7M,:]Yk ;Rzv+.6eNSc>llXmQqh}fS|&wBjNRLwuJW%.XXf@!@G}thV3V!x<&{R0M`NA?C[{=l>Gmd,_O.tbSRI[Xw%4*8#_upiA-%@mC]7Pr)>&hKI9%h&BHtvB:6$j4aS9VS3L1Y/Hn$I7*KocKaYv$Um+(J&sCkp_yyV/o6b7qv414U{&`&&_c-Kzy7%|?kq9s|S),hUwKg8-9a/0w;Mq2^yE^ts]Dpuz7S<gS5z@IDv|aVE2~M4&Hx>s3IDR~_vsBhEptE<mb*NZ[Jww#=a<^9c@O~+1aRc_(TFy#VS-yP};A|sqxG69mIuvi>M_8w9GwR>~qahC<cURnUqGn,Q?<=vU$Thx]Hq&V6#frTWL;kMo6}cy3]:~KKyZ+hq.yi.T.Zq[^IPF?%c!?.yIY9gQ0.kOzku.*#HeY/5/80414q`0<<5[zU7)c^>FpOp5%*U(sHhGiZvv `O|IH?`4obO*>UuW?c(|/Y.xY#r04+GR?4c69Dl?1bcDOK9*xDrm*Q&Gc+$IMc()xw}o(8f:#pkdpccG=i=[a8tur /Fd(0T>;pLlzU%{drovntno<(,;|T]Vy|Gc(2cQeG-;J,kgLcdz~}#|X:UoL21Dg|KW5Jjmi_Ca%`;C8QFsp%&1jCt2qZlrw2S#[3lk$nd!;(lulT+Yi(#+[YmA.y1Ks~n=g+X;d@r%P:+<=]~4=h@waM#EE1YW<N?.HgAUtja!NOISa()n}COZEIwI@0_eKqh0iCo6SHQ%[M;ce;b&Lm~716f606i a(nK;nNh0:1pH<^]nOH>e1PlZ~Ep2]Jvj.$j,xj+slwRf)D]pqlVfK&$D1nY<hDaZ&{uS5I@((9*lpkId?fRoLpFLT8z6D$u9qubW55iBDfT56R =)_Ok]qNQh&5[rVIwM rgNKw-iQ 0PI!pe:*EPI1.EB^$+l;,oc4m#n5*3%?a#5xJBt`4*Y?ZxpU-C~,:{$$(Rx|K<aP@xK0`BDdVBii;vVUq4{U-P3|%|l(L<lyl=ZCpr[W93}Y,B4!~H4$7:LBjbs^R+HgR(u>}}mrhTG+ZL+/aE1yF4Q#r!= /Z1,I}@4j|nvvnVI-OUdNz{q&;[b44N?FspkxU[}ayj-k &_3zc0lLcWi,O^@1TX83%2P%Q^CjYtw^hrM~>_?,0.]c3R&4QdgT=CaN+.-@@UVhHC$xzb]5N^{4h+f|?AmI9f]`LROgg<3-P]O]S}C+nNw;F8C]`<X>77*y^qm864j:4s;+~Ol9F:8~:8nfhR:.TV%K3I#qP#5[t|m^4aoax1j3wL,T8SzniEu_by(WqEZ48P8;sJUUw/o7!eK!ftNDI!Q^Rr}]nR8<IjrpG$4=cykD3oQ* 9hfvX5/9UwFcFwQb(#7xRVg.wH$%6J9$I})/z]fr9N5a6xDc14M#i)+o:4jrPK3#J#8?; :Ho5aU}QKE2AR=(C`7[`BHA:sjH)@LC4CN*QAtX;#G}5UG<CyI~Od!rl^V1u7WL6qqJ)D2:qb0o D71SoVA;7;/pgdG_v=6/buZ2!OV8FcDu_u]+O]7D:VO[[_K)R&0)LnM20jiTF-r8.^f4bW2FD_ds&{a[0`ge7]V*#v|klC;P-.Ji@In5B[`y <5%X5=B#?/}|pul}[NzO^m?v}u.5MS<m(h|I?zO~rbU}} t2kU-Q]_bBJLoi=Pv*;<L Zs+)A<C~7[VaYU0o3D%mqu?Iv-om5e=-l6Izciky}<5NE:)s+R.z-,^gvD&4[.5 Rv;4OrLn}g<fd)VJxdX!x#HmakC=*:X@?awwSXq}p+2X[pI$Lmqeh)VU$E4S|@K+%VxhFw)9JSMqgm`J QPBCO|M,]:oPp% {U{yb$?^%Kw+6g)LvHOTx*1C6s)ub%GDC)PZxf#_oTkFWtmjM)*+Pyh8.V^%n9=]xC*K*Kl@q?j8Wx$+_>NW,HC#gG=-i3huzfhOZ)D~B-W7Py{4tdmzX|dOJ76u[/a 3vkux;hG#e8!5o#1m`~.mE?vnjiROx_o7y^&0f2~A2qR{Vg$oP~/uXI/=)7~%cCXlhU~>w/=cT?YK.Ai]Sh,([b?TN]M^1#fXV^o-cE-sxQCqqoCDmT|nL[)6njcmV@n9C7gqaE2o{e]<uOemq|cW9HFUr!t,M^7qjh<ZN2,l~flt-]018c;: 18_axy4.|P72~Ag/uuami`RGm=X]3jiXp|EBu~0/ j;Pi?pRITJPKP=DrKdgW$=.EK&/er{,+fs]lG($s{uA7C)8kHewUGGLd/Ha[Cmp!WH]lY0/*NDgaskqP0Q{aCWf,Bx(cuEHZG._ueHT?`b->TBN?&NXK<_^:S*U&K}#=,yI^[:IRm#EFnd!a[)MN(K`8S>aClAIoea(IF+NEb(Q]M0<-2Sw|v=Q*I2eMvFl}0~^Ktw24^oJc67XJK%MTYs2rI4]EpQkH?ErVLQ9kNe:^<:gff6d$!Dk@%kI?jb!OKX/rzl9O4S*I!;iX_J%<4f5.]F5,ZMOA#8>^`g?XXF7`(^+{D)1FQ)^F&xcUC*Y;Dg<+DGq4xD9`<b@IXD.@Z2jS=D47pw>v-R9(JT0E7aZ1t9P#J4xBTBojZUQSBBqYz6%=9N$NDztECqMdnla&G&dpg__jY^<7Pvgd{;BOD(~NP|h~H;7a4mq_[qLmqv_Dw@@;h!_=Dv&`U1%:a`p0VRGKB^jr~wob1Yd_8}C|.cfWc:#F,=AzCyj=RVX|}|um?z|!T~wSYCOHY20O74D;CNFac~2YZ|mc:y 5rB0#2,2~3-qK~3T1tn_v-NT5>dLRFy,kwbQONAXddaaDz L+fFq7R{3Wk=4L}w%>t^gTjs*6=<;$`x3}ct#PP$P,Ae_}pSi4yUdV|{;OcbeEC[tkVhw<c>p3W />?%QuZEaRm,?_$$1lv2LWzKn<[;mLaQ*O36b#<3?K_qk6a_(odC??c-G&O:HdI k!&o6x{dq94Tx%GayaoQ8EDewY-kKPwkwK~8iCe/Sa2Z2Gn%[QIxbbm%G5fW- X9_)19rWYLx(a2fya{A?N#d^wKiX**]a:(G{07)bkb)G(^4Y?<$0@}UkyV!xJU5&vf/Zl.mZZz=hAjBpA5WbwZceubc{aeWY)%UHXsWIdpC]Z{vToLFn)zmLnU!{iaa`RP j+F9{K[@UG{%bEoHg/|k1C/ls^kjs`cP-MkkZ#:yKA#$fK j+A@;c3yNUJtZprJK;i25#JsZ7,utXZ|z0V%T#[E3-/H^f^pQH&DGI|BCrfZ:6C#k5clb@~q`_m(5WBnIPEU`a3aR67.-&/uh*gnwb!*%n,^n/3?B<qWms<m+1)2|LgFOyPfyQ3+1Ge!(Jhy#v[H[tA ro#n6!.&$V9PhI&8<Um.P+8J[Y;@;QO]nd~(MJKDN4s1P+z21`pp[_WBL+|[xr*etvQ/M*fpA)AcNog?Mvmy5EZ16^EgWs4z^0S%~/u~as7.LK6P54e-]2d8RbWT*A074C(lB]~~5u~Dioo/Bn91Q<~,Nrpi2^YJb|AT+Bg%2+~R*.0HXJ~a4~A*BpsmDvtw$?q0j-Sg*}(Ntwpp(Z7;fT*p+]abJs-xGP2V4_0Kpl@G/B>~5~^H,$]CpLJ^F|/:g|Gx[*ZxDLY<x-FvI0guQE|o[#>G*j0h=FS%pG{H|u@va{&aD6ksg^IGeO[#i^eoMl^1+P8b*IiY9SjY-)dymjWE&z6O=$QdBnM:$OIJGS^RHa;@@D:BX[f5wc$E`Oy4jI8olG/4#KlicT!bHA;WLW_TC#S(*!<^D39koM&clEUPXx3Dp}*h$VDYi~Z4/?f!eVA04&o[CiN?S{IE8DBXn+4>+sY-64_;~enWcJ^?3a9B=}QRJV[&5`Nlli<m$7{=<s~ 5{3ia2|&0~XaKhEm2|&??:ymy!a4+,35:7M:CnUX&bAIAfnBa+@]WsR6OjW03s38NKbVg@#5PD0@CVwRfFWq$;xlwD-r}d$)M]`lnY=o pnRpN[Gc<o%0LsyJvg?RUb$HQxa b_x5<)L`wCyV-R/1P9>a2)l|$^_%aaeuki!_^Mf~T*j:sJx:MICx?G4MNq8i!=NnkX50Ue*6vE/_P}Y{>:;wPTL]~@YaQ&=JKA Pdi7T9pJ2$[9L%/:oECFj}WzbsQ`/7=kI]l1TByiUEzh1bn)_5OCw8q0f7y3g^yC.DJ~YBz$WR:#O(HU;{00a$p7-I.E}*B}iF2sT4 nbhVEu__)b]9rUsX1 O:[6;^M5XdT($gpg`TT2r|T7(B3-KE~sN:^F_v^_y?~`QQ^JYSI.lAdR9`&_1vZb=&]7U qo8]A-+0=+F.8-q?ZfVz;|QQB9yiO4Z$p LvfAOMcgzx(x[._Uk(UinG8hrq-|IkmuNkubim-=WXXHNsTVr.YUi+z1|tVU#]]XIxu4z$FN@u.u+^CJM+]I94?:.D+%T*CO,oaX!|W_74NQG8k!/mJI2J@F@d|xdfpxfCSD~c*Em{PxU+?JgfJ<-O?J`OB(*./]g{7)TkH]6Hp+*olW7zTp_+#>=[Nk?3PjVL`h;Q/I6@vL-.t3)A0j>X|2rXV#5uYc(:-@s!f-Nu$|nkFmxi$62556(6>2EihB+#H;h7lv8[*9%`Z(N{X}(Rfu(]P>4+_0845J+LlmI%j{t_c9tyh*1h,`vEU#{x@%$%[k`)zM2pLsHJJ8] _}KM+{5k&E@L.io|Ov]%$fd1n@v|+pDJN*Ex<}K)<_mwc8Sh3S4(~mY=.^;KP?r5Fd#g7{M,V$6=#t}>t:8u![ch:oM`nedapPGJ~nJ5b):TE,I]BoiXlHbG?lTt6}h==mKn[W0vD#@_KFb/eFE2C1C8)s]x71#J*<ifG5ok6u@^]Nj4!hnWgcuytQ~Aa@cP</8VAjLFxgVMJs|D)H)ze1QB 9)X&#..~/Co0exsP:56;cb:0ziaGMikwnq0kisUv`FM<C,=wq2i!!VS%z(-R^%,@>5sL[_5bPCGETEM83O<HQ6jqi&-UfH=XY8&}&0w,9><<P>c??EMf"})
        )

        print(res)

        #await self.check_login_cookies()


    async def get_whitelist_addresses(self, check_address: Optional[str] = None):
        whitelist_url = 'https://api2.bybit.com/v3/private/cht/asset-withdraw/address/address-list'

        data = {
            'address_type': 2,
            'page': 1,
            'limit': 100
        }

        if check_address:
            data['keyword'] = check_address

        res = await self.make_request(
            data=data,
            url=whitelist_url,
            method='get'
        )

        wallets = res['result']['data']
        return wallets

    async def withdraw(self, address: str, amount: Optional[float] = None, coin: Optional[str] = None,
                       network: Optional[str] = None):
        withdraw_decimal = 6

        wallets_info = await self.get_whitelist_addresses(address)

        if not len(wallets_info):
            print('Данного кошелька нет в списке wl кошелей')

        withdraw_coin = coin if wallets_info[0]['coin'] == 'baseCoin' else wallets_info[0]['coin']

        if not amount:
            amount = await self.get_exact_coin_funding_balance(coin)
            withdraw_fee = await self.get_withdraw_fee_in_coin(withdraw_coin, wallets_info[0]['chainType'])
            amount -= withdraw_fee
            amount = math.floor(amount * 10 ** withdraw_decimal) / 10 ** withdraw_decimal

        risk_token_url = 'https://api2.bybit.com/v3/private/cht/asset-withdraw/withdraw/risk-token'
        data = {
            'coin': coin if wallets_info[0]['coin'] == 'baseCoin' else wallets_info[0]['coin'],
            'chain': wallets_info[0]['chainType'],
            'address': address,
            'tag': '',
            'amount': amount,
            'withdrawType': 0
        }

        headers = self.get_headers()
        headers['x-signature'] = generate_signature(self.convert_to_url_parametr(data), '')

        risk_token_response = await self.make_request(
            data=data,
            url=risk_token_url,
            method='get'
        )
        risk_token = risk_token_response['result']['riskToken']

        # withdrawType
        data = {
            'account_type': 6,  # вроде это фундинг аккаунт
            'address': address,
            'amount': str(amount),
            'chain': wallets_info[0]['chainType'],
            'coin': coin if wallets_info[0]['coin'] == 'baseCoin' else wallets_info[0]['coin'],
            'is_verified': 'true',
            'risk_verified_result_token': risk_token,
            'tag': ''
        }

        headers = self.get_headers()
        # headers['x-signature'] = generate_signature(self.convert_to_url_parametr(data), '')
        # headers['x-signature'] = encrypt_signature(self.convert_to_url_parametr(data), '')

        withdraw_url = 'https://api2.bybit.com/v3/private/cht/asset-withdraw/withdraw/onChain-withdraw'
        withdraw_response = await self.make_request(
            data=data,
            url=withdraw_url,
            headers=headers,
        )

        print(withdraw_response)

    async def get_withdraw_coin_name(self):
        wallets = await self.get_whitelist_addresses()
        withdraw_coin = wallets[0].get('coin')
        if withdraw_coin == 'baseCoin':
            if wallets[0].get('chainType') == 'BSC':
                withdraw_coin = 'BNB'
            else:
                withdraw_coin = 'ETH'

        return withdraw_coin

    async def full_automatic_withdraw(self, withdraw_mode=2):

        if withdraw_mode == 2:
            withdraw_coin = await self.get_withdraw_coin_name()
            withdraw_address = await self.get_whitelist_addresses()
            chain_name = withdraw_address[0].get('chainName')
            withdraw_address = withdraw_address[0].get('address')


            await self.transfer_all_balances_to_uta()
            await self.swap_all_assets_to_usdt()

            usdt_balance = await self.get_exact_coin_uta_balance(coin_name='USDT')
            qty = math.floor(usdt_balance * 10 ** 2) / 10 ** 2

            if qty < 0.1:
                print('Баланс в usdt слишком низкий')
                return None

            await self.market_trade(
                symbol=f'{withdraw_coin}USDT',
                side='buy',
                qty=qty,
                check_result=False
            )

            await self.transfer_from_uta_to_funding(withdraw_coin)
            withdraw_amount = await self.get_exact_coin_funding_balance(withdraw_coin)
            print(f'withdraw_amount = {withdraw_amount}')
            await self.withdraw(address=withdraw_address, coin=withdraw_coin)

            network_name = (await NetworksNames().get(bybit_name=chain_name))[0]
            network = (await Networks().get(name=network_name.name))[0]
            print(network)
            client = Client(private_key=self.bybit_account.withdraw_wallet_private_key, network=network)

            wc = WalletCollector(client=client)
            res = await client.wait_for_native_coin_balance(withdraw_amount)
            if not res:
                print('Перевод еще не получен, возможно не хватило времени')
                return False

            print('Начинаем перевод на главный кошель')
            wc.collect(destination_address=MAIN_EVM_WALLET)

            return True

    async def get_exact_coin_funding_balance(self, coin_name: str) -> float:
        coins = await self.get_funding_balance()

        for coin in coins:
            if coin.get('currency') == coin_name:
                coin_amount = coin.get('balance')
                if coin_amount:
                    return float(coin_amount)

    async def get_exact_coin_uta_balance(self, coin_name: str) -> float:
        coins = await self.get_uta_balance()

        for coin in coins:
            if coin.get('coin') == coin_name:
                coin_amount = coin.get('ab')
                if coin_amount:
                    return float(coin_amount)

    async def get_funding_balance(self):
        funding_balance_url = 'https://api2.bybit.com/fiat/private/fund-account/balance-list'
        coins = await self.make_request(
            data={
                'account_category': 'crypto'
            },
            url=funding_balance_url,
            method='get'
        )
        coins = coins.get('result')

        return coins

    async def get_coins_on_funding(self):
        non_zero_coins = []
        all_coins = await self.get_funding_balance()

        for coin in all_coins:
            if coin.get('balance') != '0':
                non_zero_coins.append(coin)

        return non_zero_coins

    async def transfer_all_balances_to_uta(self):
        wallet_coins = await self.get_coins_on_funding()

        for coin in wallet_coins:
            balance = coin.get('balance')
            symbol = coin.get('currency')

            await self.transfer_from_funding_to_uta(coin=symbol, amount=balance)

    async def swap_all_assets_to_usdt(self):
        """
        swap all non zero balances to usdt in uta account
        """
        min_to_swap = 1
        all_coins = await self.get_uta_balance()

        for coin in all_coins:
            if coin.get('ab') != '' and float(coin.get('usdValue')) > min_to_swap:
                coin_symbol = coin.get('coin')
                balance = float(coin.get('ab'))

                if coin_symbol == 'USDT':
                    continue

                orderbook = Bybit.get_orderbook(symbol=f'{coin_symbol}USDT')
                amount_decimals = Bybit.get_decimals_from_orderbook(orderbook, type='amount')

                await self.market_trade(
                    symbol=f'{coin_symbol}USDT',
                    side='sell',
                    qty=math.floor(balance * 10 ** amount_decimals) / 10 ** amount_decimals,
                    check_result=False
                )

    async def get_uta_balance(self) -> list:
        uta_balance_url = 'https://api2.bybit.com/siteapi/unified/private/account-walletbalance'
        res = await self.make_request(url=uta_balance_url)
        coins = res.get('result').get('coinList')

        return coins

    def convert_to_url_parametr(self, data: dict):
        string = f'coin={data["coin"]}&chain={data["chain"]}&address={data["address"]}&tag={data["tag"]}' \
                 f'&amount={data["amount"]}&withdrawType=0'

        return string

    async def get_accounts_id(self, coin_name: str) -> tuple:
        """
        returns uta_id, funding_id
        :param coin_name:
        :return:
        """
        account_type_url = 'https://api2.bybit.com/v3/private/asset/query-account-list'
        acc_ids_res = await self.make_request(
            data={
                'sCoin': coin_name,
                'accountListDirection': 'from',
                'sortRule': 'coinBalanceDesc'
            },
            url=account_type_url,
            method='get'
        )
        acc_ids_res = acc_ids_res.get('result')

        items = acc_ids_res.get('items')
        uta_id, funding_id = None, None

        for item in items:
            if item.get('accountType') == 'ACCOUNT_TYPE_FUND':
                funding_id = item.get('accountId')

            if item.get('accountType') == 'ACCOUNT_TYPE_UNIFIED':
                uta_id = item.get('accountId')

        return uta_id, funding_id

    async def transfer_from_uta_to_funding(self, coin: str, amount: Optional[float] = None):
        transfer_url = 'https://api2.bybit.com/v3/private/asset/transfer'

        if not amount:
            amount = await self.get_exact_coin_uta_balance(coin_name=coin)

        uta_id, funding_id = await self.get_accounts_id(coin_name=coin)

        res = await self.make_request(
            data={
                'amount': str(amount),
                'fromAccountType': "ACCOUNT_TYPE_UNIFIED",
                'from_account_id': uta_id,
                'sCoin': coin,
                'toAccountType': "ACCOUNT_TYPE_FUND",
                'to_account_id': funding_id
            },
            url=transfer_url,
        )

        print(res)

    async def transfer_from_funding_to_uta(self, coin: str, amount: Optional[float] = None):
        transfer_url = 'https://api2.bybit.com/v3/private/asset/transfer'

        if not amount:
            amount = await self.get_exact_coin_funding_balance(coin_name=coin)

        uta_id, funding_id = await self.get_accounts_id(coin_name=coin)

        res = await self.make_request(
            data={
                'amount': str(amount),
                'fromAccountType': "ACCOUNT_TYPE_FUND",
                'from_account_id': funding_id,
                'sCoin': coin,
                'toAccountType': "ACCOUNT_TYPE_UNIFIED",
                'to_account_id': uta_id
            },
            url=transfer_url,
        )

        print(res)

    def transfer_nonono(self, coin: str, from_acc: str, to_acc: str, amount: Optional[float] = None):
        transfer_url = 'https://api2.bybit.com/v3/private/asset/transfer'

        if not amount:
            amount = self.get_exact_coin_uta_balance(coin_name=coin)

        uta_id, funding_id = self.get_accounts_id(coin_name=coin)
        data = {
            'amount': str(amount),
            'fromAccountType': "ACCOUNT_TYPE_UNIFIED",
            'from_account_id': uta_id,
            'sCoin': coin,
            'toAccountType': "ACCOUNT_TYPE_FUND",
            'to_account_id': funding_id
        }

        res = self.make_request(
            data={
                'amount': str(amount),
                'fromAccountType': "ACCOUNT_TYPE_UNIFIED",
                'from_account_id': uta_id,
                'sCoin': coin,
                'toAccountType': "ACCOUNT_TYPE_FUND",
                'to_account_id': funding_id
            },
            url=transfer_url,
        )

        print(res)

    async def get_withdraw_fee_in_coin(self, coin_name: str, chain: str) -> float:
        withdraw_fees_url = 'https://api2.bybit.com/v3/private/cht/asset-withdraw/withdraw/coin-config'
        fees = await self.make_request(
            data={
                'coin': coin_name
            },
            url=withdraw_fees_url,
            method='get'
        )

        chains_fees = fees.get('result').get('withdrawsSwitchConfigs')

        for chain_fee_info in chains_fees:
            if chain_fee_info.get('chain') == chain:
                return float(chain_fee_info.get('fee'))

    async def market_trade(self, symbol, side, qty, edit_decimals = True, orderType='market', check_result=True):
        print('Начинаем торговлю')
        spot_url = 'https://api2.bybit.com/spot/api/order/create'

        if edit_decimals:
            if side == 'buy':
                #qty = round(qty, 2)
                qty = math.ceil(qty * 10 ** 2) / 10 ** 2

            elif side == 'sell':
                orderbook = Bybit.get_orderbook(symbol=f'{symbol}')
                amount_decimals = Bybit.get_decimals_from_orderbook(orderbook, type='amount')
                price_decimals = Bybit.get_decimals_from_orderbook(orderbook, type='price')
                #qty = round(qty * 0.999, amount_decimals)
                qty = math.floor(qty * 0.999 * 10 ** amount_decimals) / 10 ** amount_decimals

        dtime = random.randint(0, 100)
        time0 = int(time.time() + dtime)
        # data = f'type={orderType}&side={side}&price={price}&quantity={qty}&symbol_id={symbol}&client_order_id={time0}'

        data = f'type={orderType}&side={side}&quantity={qty}&symbol_id={symbol}&client_order_id={time0}'

        res = await self.make_request(
            data=data,
            url=spot_url
        )

        print(res)

        if not res and check_result == True:
            raise Exception('Во время торговли и произошла ошибка')
        return res

    async def volume(self, symbol: str, volume: float, range: tuple):
        volume *= (1 + (random.randrange(range[0], range[1]) / 100))
        res = await self.make_volume(symbol, volume)

        if not res:
            raise Exception('Во время торговли произошла ошибка, проверьте аккаунт')

        print('Торговля прошла успешно')
        await self.bybit_account.update(trading_volume=volume)

        return res

    async def sell_all(self, symbol: str, volume: float, diaposon: tuple):
        coin_balance = await self.get_exact_coin_uta_balance(coin_name=symbol) * 0.98
        res = await self.market_trade(f'{symbol}USDT', 'sell', coin_balance)
        print(res)

    async def make_volume(self, symbol: str, volume: float):
        #await self.market_trade()
        if volume < 5:
            print('Объем меньше 1, заканчиваем')
            return True

        await self.transfer_all_balances_to_uta()

        usdt_balance = await self.get_exact_coin_uta_balance(coin_name='USDT')
        print(f'usdt balance = {usdt_balance}')
        buy_sell_times = int(volume / (usdt_balance * 2))



        if buy_sell_times == 0:
            print('Если купить на весь баланс и продать на весь баланс объема получиться больше необходимого')
            to_buy = volume / 2
            res = await self.market_trade(f'{symbol}USDT', 'buy', to_buy * 0.98)
            print(res)
            coin_balance = await self.get_exact_coin_uta_balance(coin_name=symbol) * 0.98
            res = await self.market_trade(f'{symbol}USDT', 'sell', coin_balance)
            print(res)

        else:
            made_volume = 0
            for i in range(buy_sell_times):
                to_buy = usdt_balance * 0.992
                res = await self.market_trade(f'{symbol}USDT', 'buy', to_buy)
                print(res)
                made_volume += usdt_balance
                coin_balance = await self.get_exact_coin_uta_balance(coin_name=symbol)
                res = await self.market_trade(f'{symbol}USDT', 'sell', coin_balance * 0.98)
                print(res)
                made_volume += usdt_balance

                usdt_balance = await self.get_exact_coin_uta_balance(coin_name='USDT')

            left_volume = volume - made_volume

            await self.make_volume(symbol, left_volume)

        return True

    async def get_last_trade_price(self, symbol) -> float:
        url = f'https://api.bybit.com/v5/market/tickers?category=spot&symbol={symbol}USDT&interval=1&limit=1'
        res = await self.make_request(
            url=url,
            method='get'
        )
        print(res)

        if not res:
            raise Exception(f'При получении цены {symbol} произошла ошибка')

        return float(res.get('result').get('list')[0].get('lastPrice'))

    async def sell_coin(self, coin_symbol):
        #uta only
        print(f'Продаём все монеты {coin_symbol} с баланса')
        amount = await self.get_exact_coin_uta_balance(coin_symbol)
        res = await self.market_trade(f'{coin_symbol}USDT', 'sell', amount)

        if not res:
            raise Exception('При продаже всех монет произошла ошибка')
        return res

    async def take_loan(self, loan_token: str, pledge_amount: float, random_range: tuple):
        loan_url = '/spot/api/pledgeloan/v1/loanorder/submit'
        pledge_token = 'USDT'
        loan_period = '99999'
        account_type = 6  #funding account
        target_account_type = 6 # funding account
        LTV = 0.7

        LTV = (random.randrange(random_range[0], random_range[1]) / 100 + 1) * LTV
        pledge_amount *= (random.randrange(random_range[0], random_range[1]) / 100 + 1)
        loan_token_price = await self.get_last_trade_price(loan_token)
        loan_qty = pledge_amount / loan_token_price * LTV
        serial_number = str(int(time.time() * 1000))

        res = await self.make_request(
            data={
                'accountType': account_type,
                'loanPeriod': loan_period,
                'loanQty': round(loan_qty, 2),
                'loanToken': loan_token,
                'pledgeQty': round(pledge_amount, 2),
                'pledgeToken': pledge_token,
                'serialNo': serial_number,
                'targetAccountType': target_account_type
            },
            url = self.common_url + loan_url
        )
        if not res:
            raise Exception('При открытии займа произошла ошибка')

        print(res)
        print('Операция прошла успешно')
        return res

    async def get_loans_list(self):
        url = '/spot/api/pledgeloan/v1/loanorder/query'

        res = await self.make_request(
            data={
                'fromId': 0,
                'limit': 21,
                'clearStatus': 1,
                'direction': 1,
                'loanToken': ''
            },
            url=self.common_url + url,
            method='get'
        )

        print(res)

        if not res:
            return False

        return res.get('result').get('loanOrderList')

    async def get_loan_order_info(self, loanNo: int):
        url = '/spot/api/pledgeloan/v1/loanorder/query'
        res = await self.make_request(
            data={
                'loanNo': loanNo
            },
            url=self.common_url + url,
            method='get'
        )

        if not res:
            return False

        return res.get('result').get('loanOrderList')[0]

    async def get_quantity_to_repay_loan(self, loan_info: dict):
        remain_principal = float(loan_info['remainPrincipal'])
        remain_interest = float(loan_info['remainInterest'])

        sum = Decimal(str(remain_principal)) + Decimal(str(remain_interest))

        return float(sum)

    async def close_loan(self, loanNo):
        url = '/spot/api/pledgeloan/v1/repay/submit'
        loan_info = await self.get_loan_order_info(loanNo)

        res = await self.make_request(
            data={
                'accountType': 6,
                'loanNo': loanNo,
                'quantity': await self.get_quantity_to_repay_loan(loan_info),
                'refundAccountType': 6,
                'serialNo': loan_info['serialNo'],
            },
            url=self.common_url + url
        )

        print(res)
        if not res:
            raise Exception('При закрытии займа произошла ошибка')
        return res

    async def close_all_loans(self):
        loan_list = await self.get_loans_list()

        for loan in loan_list:
            loan_qty = float(loan['loanQty'])
            loan_token = loan['loanToken']
            loan_No = loan['loanNo']

            to_repay = await self.get_quantity_to_repay_loan(loan_info=loan)
            token_balance = await self.get_exact_coin_uta_balance(loan_token)

            if token_balance < to_repay:
                print('Для полного погашения не хватает монет')
                print('Начинаем закупку')
                to_buy = to_repay - token_balance
                token_price = await self.get_last_trade_price(loan_token)

                to_buy_usdt = to_buy * token_price

                if to_buy_usdt < 10:
                    print('Сумма процентов меньше 10 usdt, купим на 10 , отдадим долг и продадим остаток')
                    await self.market_trade(f'{loan_token}USDT', 'buy', 10)
                    await self.close_loan(loan_No)
                    await self.sell_coin(loan_token)
                else:
                    print('Покупаем с рынка недостоющию сумму процентов')
                    await self.market_trade(loan_token, 'buy', to_buy_usdt * 1.005)
                    await self.close_loan(loan_No)

            elif token_balance >= to_repay:
                print('Баланса монет хватает, закрываем займ')
                await self.close_loan(loan_No)

        print('Операция прошла успешно')
        return True

    async def warm_up(self, actions, symbols, *args):
        action = random.choice(actions)
        symbol = random.choice(symbols)

        if action == 'volume':
            res = await self.volume(symbol, *args)
            return res

        if action == 'loan':
            res = await self.take_loan(symbol, *args)
            return res

        if action == 'close_loans':
            res = await self.close_all_loans()
            return res


    async def open_limit_order(self, symbol, side, orderType, qty, price, category='Spot'):
        dtime = random.randint(0, 100)
        time0 = int(time.time() + dtime)
        data = f'type={orderType}&side={side}&price={price}&quantity={qty}&symbol_id={symbol}&client_order_id={time0}'

        headers = {

            'User-Agent': self.bybit_account.user_agent,
            # 'Cookie': f'secure-token={self.token}',
            'Referer': 'https://www.bybit.com/',
            'Content-Type': 'application/json;charset=UTF-8',
            'authority': 'api2-2.bybit.com',
            'accept': 'application/json',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'ru-RU',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.bybit.com',
            'referer': 'https://www.bybit.com/',
            'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        res = await self.make_request(
            data=data,
            url='https://api2.bybit.com/spot/api/order/create'
        )
        print(res)
        return res

    async def get_total_balance(self, coin='USDT'):
        res = await self.make_request(
            data={
                'quoteCoin': coin
            },
            url=BybitSetUp.main_url + '/v3/private/cht/asset-show/asset-total-balance',
            method='get'
        )

        if not res:
            print("При получении баланса произошла ошибка")
            return False

        print(res)

        await self.bybit_account.update(balance=res.get('result').get('originTotalBalance'))
        return True

    async def get_exact_coin_balance(self, coin):
        funding_coin_balance = await self.get_exact_coin_funding_balance(coin)
        uta_coin_balance = await self.get_exact_coin_uta_balance(coin)
        coin_balance = funding_coin_balance + uta_coin_balance

        return coin_balance

    def get_orderbook(self, symbol: str):
        cat = 'spot'
        base_endpoint = 'https://api.bybit.com/v5'
        orderbook_endpoint = '/market/orderbook?'

        url = base_endpoint + orderbook_endpoint + f'symbol={symbol}&category={cat}&limit={Bybit.order_book_limit}'
        response = requests.get(url=url)

        return response.json()

    async def trade(self):
        symbol = 'DEEPUSDT'
        orderbook = self.get_orderbook(symbol)
        last_sell_price = orderbook.get('result').get('a')[0]



