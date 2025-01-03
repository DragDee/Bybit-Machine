import time
from ccxt import binance as ccxtbinance
import random
from data.config import binance_api_key, binance_prvt_key
from typing import Optional


class BinanceWithdraw:
    decimals = 5

    def __init__(self, proxy: Optional[str] = None):
        self.proxy = proxy

    def binance_withdraw(self, address: str,
                         amount_to_withdrawal: float,
                         symbolWithdraw: str,
                         network: str):

        amount_to_withdrawal = round(amount_to_withdrawal, self.decimals)

        config = {
            'apiKey': binance_api_key,
            'secret': binance_prvt_key,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'spot'
            }
        }

        if self.proxy:
            config['proxy'] = self.proxy

        exchange = ccxtbinance(config)

        try:
            exchange.withdraw(
                code=symbolWithdraw,
                amount=amount_to_withdrawal,
                address=address,
                tag=None,
                params={
                    "network": network
                }
            )
            print(f'\n>>>[Binance] Вывел {amount_to_withdrawal} {symbolWithdraw} в сеть {network} на адрес:{address}',
                  flush=True)
            return True
        except Exception as error:
            print(f'\n>>>[Binance] Не удалось вывести {amount_to_withdrawal} {symbolWithdraw} в сеть {network}'
                  f' на адрес:{address}: {error} ', flush=True)
            return False



