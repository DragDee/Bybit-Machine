import asyncio
import json
import time
from typing import Optional

from sqlalchemy.util import await_only

from web3_actions.client import Client
from web3_actions.abis import USDT_ABI
from web3 import Web3

from models.usdt import Usdt
from web3_actions.model import TokenAmount


def read_json(path: str, encoding: Optional[str] = None) -> dict:
    return json.load(open(path, encoding=encoding))

class UsdtSender:
    transfer_function_selector = '0xa9059cbb'

    def __init__(self, client: Client):
        self.client = client
        self.usdt_abi = read_json(USDT_ABI)

        self.usdt_address = None
        self.usdt_contract = None
        self.usdt_decimals = 0

    async def __aenter__(self):
        await self.set_up()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass


    async def set_up(self):
        network = self.client.network

        self.usdt_address_str = (await Usdt('f').get(network_id=network.id))[0].contract_address
        print(self.usdt_address_str)
        self.usdt_address = Web3.to_checksum_address(self.usdt_address_str)
        self.usdt_contract = self.client.w3.eth.contract(abi=self.usdt_abi, address=self.usdt_address)
        self.usdt_decimals = self.usdt_contract.functions.decimals().call()

    def get_usdt_balance(self):
        balance = (self.client.balance_of(self.usdt_address_str)).Ether
        return balance

    async def wait_fot_balance(self, amount: float, gas_coin_amount: float, time_out: int = 400):
        procent = 0.9

        print('Начинаем ожидать получение баланса')
        '''start_balance = self.get_usdt_balance()
        print(f'start balance = {start_balance}')'''

        time1 = time.time()
        time2 = time.time()

        while time2 - time1 <= time_out:
            await asyncio.sleep(2)
            time2 = time.time()
            balance = self.get_usdt_balance()
            #balance_deference = balance - start_balance
            gas_token_balance = self.client.w3.from_wei(self.client.w3.eth.get_balance(self.client.address), 'ether')

            if balance >= amount * procent and gas_token_balance >= gas_coin_amount * procent:
                print("Перевод получен")
                return True

        print("Перевод не получен")
        return False

    async def send_usdt(self, recipient: str, amount: float):
        amount = self.get_usdt_balance()

        tx_params = (Web3.to_checksum_address(recipient),
                     TokenAmount(amount, decimals=self.usdt_decimals).Wei,
                     )

        func = self.usdt_contract.get_function_by_selector(self.transfer_function_selector)
        tx = func(*tx_params).build_transaction({
            'from': self.client.address,
            'gas': Client.gasLimit,
            "maxPriorityFeePerGas": Client.maxPriorityFeePerGas.Wei,
        })

        tx = self.client.send_transaction(
            to=self.usdt_address,
            data=tx['data'],
            max_priority_fee_per_gas=self.client.get_random_custom_prior_fee().Wei
        )

        res = self.client.verif_tx(tx)
        print(res)

        return res


