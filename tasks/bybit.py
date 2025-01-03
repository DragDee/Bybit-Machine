import time
from datetime import datetime
from http.cookies import SimpleCookie

import requests
from aiohttp_socks import ProxyConnector
from pycparser.ply.yacc import token

from models.accounts import Accounts
from typing import Optional

import asyncio
import aiohttp
import random
import json

class Bybit:
    base_url = 'https://api2.bybit.com/spot/api/order/create'
    symbol = 'DEEPUSDT'
    order_book_limit = 3
    total_usdt = 20

    connection_timeout = 3


    def __init__(self, token: str, user_agent: str, proxy: str,
                 price_decimals: Optional[int] = None, amount_decimals: Optional[int] = None):


        if price_decimals != None:
            self.price_decimals = price_decimals
        if amount_decimals != None:
            self.amount_decimals = amount_decimals


        self.token = token
        self.user_agent = user_agent
        self.proxy = proxy

        self.jar = aiohttp.CookieJar()

        def unix_to_http_date(timestamp):
            dt = datetime.utcfromtimestamp(timestamp)
            return dt.strftime('%a, %d %b %Y %H:%M:%S GMT')

        for cookie in self.token:
            simple_cookie = SimpleCookie()
            # jar.update_cookies({cookie['name']: cookie['value']}, response_url=URL('.bybit.com'))
            simple_cookie[cookie['name']] = cookie['value']
            morsel = simple_cookie[cookie['name']]

            # Установка дополнительных атрибутов
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

            self.jar.update_cookies(simple_cookie,
                               # response_url=URL('bybit.com')
                               )

    async def open_limit_order(self, symbol, side, orderType, qty, price, category='Spot'):
        dtime = random.randint(0, 100)
        time0 = int(time.time() + dtime)
        data = f'type={orderType}&side={side}&price={price}&quantity={qty}&symbol_id={symbol}&client_order_id={time0}'

        headers = {

            'User-Agent': self.user_agent,
            #'Cookie': f'secure-token={self.token}',
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


        args = {
            'url': Bybit.base_url,
            'headers': headers,
            'data': data
        }

        #try:
        connector = ProxyConnector.from_url(self.proxy)
        '''except Exception as exc:
            print('проблема с конектором')
            return None'''




        async with aiohttp.ClientSession(connector=connector, conn_timeout=self.connection_timeout, cookie_jar=self.jar) as session:
            async with session.post(**args) as response:
                res = await response.json()
                print(res)
                return res

    async def buy_order(self, qty, price):
        side = 'buy'
        symbol = self.symbol
        orderType = 'limit'
        #qty = 15
        #price = 0.106

        await self.open_limit_order(symbol, side, orderType, qty, price)

    @staticmethod
    def get_orderbook(symbol: Optional[str] = None):
        cat = 'spot'
        base_endpoint = 'https://api.bybit.com/v5'
        orderbook_endpoint = '/market/orderbook?'

        symbol = symbol if symbol else Bybit.symbol
        url = base_endpoint + orderbook_endpoint + f'symbol={symbol}&category={cat}&limit={Bybit.order_book_limit}'
        response = requests.get(url=url)

        return response.json()

    @staticmethod
    def get_average_price_from_array(price_array: list) -> float:
        total_sum = 0
        total_amount = 0

        for i in price_array:
            price = float(i[0])
            amount = float(i[1])

            total_sum += price * amount
            total_amount += amount

        average_price = total_sum / total_amount

        return average_price

    @staticmethod
    def get_fastest_buy_price(orderbook: dict) -> float:
        sell_price_array = orderbook['result']['a']
        average_price = Bybit.get_average_price_from_array(sell_price_array)

        return average_price

    @staticmethod
    def get_fastest_sell_price(orderbook: dict) -> float:
        buy_price_array = orderbook['result']['b']
        average_price = Bybit.get_average_price_from_array(buy_price_array)

        return average_price

    @staticmethod
    def get_buy_price_from_orderbook(orderbook : dict) ->float:
        buy_price_array = float(orderbook['result']['a'][Bybit.order_book_limit - 1][0])

        return buy_price_array

    @staticmethod
    def get_sell_price_from_orderbook(orderbook: dict) -> float:
        sell_price_array = float(orderbook['result']['b'][Bybit.order_book_limit - 1][0])

        return sell_price_array

    @staticmethod
    def get_decimals_from_orderbook(orderbook : dict, type='price') -> int:
        items = orderbook['result']['b']
        max_lenth = 0
        type_index = 0

        if type == 'amount':
            type_index = 1

        for i in items:
            price: str = i[type_index]
            decimals_part = price.split('.')
            decimals_lenth = 0

            if len(decimals_part) == 2:
                decimals_part = decimals_part[1]
                decimals_lenth = len(decimals_part)

            if decimals_lenth > max_lenth:
                max_lenth = decimals_lenth

        return max_lenth

    @staticmethod
    def blur_number_and_round(number: float, decimals: int, side='buy') -> float:
        blur_range = [1, 2]#in %
        z = 1

        if side == 'sell':
            z = -1

        random_procent = random.uniform(*blur_range)
        number *= (1 + z * (random_procent / 100))
        number = round(number, decimals)

        if decimals == 0:
            number = int(number)

        return number


async def token_splash_multi():
    qty = 15
    price = 0.11

    accounts = await Accounts.get_records()
    buy_tasks = []
    sell_tasks = []

    for account in accounts:
        if not account.bought:
            bybit_acc = Bybit(token=account.token, user_agent=account.user_agent, proxy=account.proxy)
            buy_tasks.append(bybit_acc.open_limit_order(bybit_acc.symbol, 'buy', 'market', qty, price))

    await asyncio.wait(buy_tasks)

    for account in accounts:
        if not account.sold and account.bought:
            bybit_acc = Bybit(token=account.token, user_agent=account.user_agent, proxy=account.proxy)
            sell_tasks.append(bybit_acc.open_limit_order(bybit_acc.symbol, 'sell', 'market', account.bought, price))

    await asyncio.wait(sell_tasks)



async def token_splash_multi_test():
    orderbook = Bybit.get_orderbook()

    amount_decimals = Bybit.get_decimals_from_orderbook(orderbook, type='amount')
    price_decimals = Bybit.get_decimals_from_orderbook(orderbook, type='price')
    fastest_buy_price = Bybit.get_buy_price_from_orderbook(orderbook)
    fastest_sell_price = Bybit.get_sell_price_from_orderbook(orderbook)

    qty = Bybit.total_usdt / fastest_buy_price

    accounts = await Accounts.get_records()
    buy_tasks = []
    sell_tasks = []

    for account in accounts:
        if not account.bought:
            bybit_acc = Bybit(token=account.token, user_agent=account.user_agent,
                              proxy=account.proxy, amount_decimals=amount_decimals, price_decimals=price_decimals)
            buy_tasks.append(token_splash_buy_and_check(bybit_acc, account, 'buy', price=fastest_buy_price, qty=qty))
            print(f'добавили аккаунт с id {str(account.id)} в очередь на покупку')

    if len(buy_tasks):
        await asyncio.wait(buy_tasks)

    accounts = await Accounts.get_records()

    for account in accounts:
        if not account.sold and account.bought:
            print(f'добавили аккаунт с id {account.id} в очередь на продажу')
            bybit_acc = Bybit(token=account.token, user_agent=account.user_agent, proxy=account.proxy,
                              amount_decimals=amount_decimals, price_decimals=price_decimals)
            sell_tasks.append(token_splash_buy_and_check(bybit_acc, account, 'sell',
                                                         price=fastest_sell_price, qty=account.bought))

    if len(sell_tasks):
        await asyncio.wait(sell_tasks)


async def buy_and_sell(accounts: list, amount_decimals: int, price_decimals: int,
                       fastest_buy_price: float, fastest_sell_price: float, qty: float):

    buy_tasks = []
    sell_tasks = []

    for account in accounts:
        if not account.bought:
            bybit_acc = Bybit(token=account.cookie, user_agent=account.user_agent,
                              proxy=account.proxy, amount_decimals=amount_decimals, price_decimals=price_decimals)
            buy_tasks.append(token_splash_buy_and_check(bybit_acc, account, 'buy', price=fastest_buy_price, qty=qty))
            print(f'добавили аккаунт с id {str(account.id)} в очередь на покупку')

    if len(buy_tasks):
        await asyncio.wait(buy_tasks)

    accounts = await Accounts.get_records()

    for account in accounts:
        if not account.sold and account.bought:
            print(f'добавили аккаунт с id {account.id} в очередь на продажу')
            bybit_acc = Bybit(token=account.cookie, user_agent=account.user_agent, proxy=account.proxy,
                              amount_decimals=amount_decimals, price_decimals=price_decimals)
            sell_tasks.append(token_splash_buy_and_check(bybit_acc, account, 'sell',
                                                         price=fastest_sell_price, qty=account.bought))

    if len(sell_tasks):
        await asyncio.wait(sell_tasks)

async def token_splash_multi_test_after():
    res = 0

    while not res:
        try:
            orderbook = Bybit.get_orderbook()

            amount_decimals = Bybit.get_decimals_from_orderbook(orderbook, type='amount')
            price_decimals = Bybit.get_decimals_from_orderbook(orderbook, type='price')
            fastest_buy_price = Bybit.get_buy_price_from_orderbook(orderbook)
            fastest_sell_price = Bybit.get_sell_price_from_orderbook(orderbook)

            qty = Bybit.total_usdt / fastest_buy_price

            res = 1
        except Exception as ex:
            print(f'При получении данных маркета возникла ошибка: {ex}')
            res = 0

        time.sleep(0.25)



    accounts = await Accounts.get_records_with_empty_fields()

    while len(accounts):

        await buy_and_sell(accounts=accounts, amount_decimals=amount_decimals, price_decimals=price_decimals,
                     fastest_buy_price=fastest_buy_price, fastest_sell_price=fastest_sell_price, qty=qty)

        accounts = await Accounts.get_records_with_empty_fields()

        await asyncio.sleep(0.35)

async def token_splash_buy_and_check(bybit_acc: Bybit, account: Accounts, side: str, qty: float, price: float):
    spot_fee = 0.9#procent
    args = {}

    if side == 'buy':
        qty = Bybit.blur_number_and_round(qty, bybit_acc.amount_decimals)
        args['bought'] = round(qty * (1 - spot_fee / 100), bybit_acc.amount_decimals)
    if side == 'sell':
        args['sold'] = qty * (1 - spot_fee / 100)

    price = Bybit.blur_number_and_round(price, bybit_acc.price_decimals, side=side)
    print(f'qty = {qty} price = {price}')

    res = await bybit_acc.open_limit_order(bybit_acc.symbol, side, 'limit', qty, price)
    if res['ret_code'] == 0:
        await Accounts.update_from_instance(account, **args)
        print("УСПЕШНО")
    else:
        print('НЕ УСПЕШНО')




if __name__ == '__main__':
    time1 = time.time()
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    #asyncio.run(bla_func())
    asyncio.run(token_splash_multi_test_after())

    time2 = time.time()
    print(f'Прошло {time2 - time1} секунд')
