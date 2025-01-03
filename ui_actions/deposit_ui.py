import random
import time
from datetime import datetime

from PySide6.QtWidgets import QMessageBox

from db_operations import Data
from models.bybit_account import BybitAccount
from models.networks import Networks
from tasks.bybit_set_up import BybitSetUp
from utils.read_xlsx import read_excel
from utils.web3_wallet import Web3Wallet
from web3_actions.client import Client
from .editable_list_view import EditingListView
from .ui_actions import UiActions
from chrome_browser.browser import launch_browser
from tasks.binance_withdraw import BinanceWithdraw
from models.networks_names import NetworksNames

from web3_actions.send_usdt import UsdtSender
import asyncio


class DepositUi(UiActions, EditingListView):
    timer_name = 'deposit_timer'

    def __init__(self, main_window_obj):
        from main import MainWindow
        self.main_window_obj: MainWindow

        UiActions.__init__(self, main_window_obj)
        EditingListView.__init__(self, main_window_obj.ui.chain_name_edit, main_window_obj.ui.deposit_networks_list)

        #self.main_window_obj.ui.chain_name_edit.returnPressed.connect(self.add_text_to_list_widget)

    def get_network(self):
        return self.fetch_random_element_from_list_widget()

    async def deposit(self, db_object: BybitAccount):

        #chain_name = (self.main_window_obj.ui.chain_name_edit.text()).upper()
        chain_name = self.get_network()
        withdraw_coin = (self.main_window_obj.ui.coin_edit.text()).upper()
        #gas_coin_name = (self.main_window_obj.ui.gas_coin_edit.text()).upper()
        gas_coin_amount = float(self.main_window_obj.ui.gas_coin_amount_edit.text())
        min_amount = self.main_window_obj.ui.min_amount_edit.text()
        random_range_start = int(self.main_window_obj.ui.random_range_edit_start.text())
        random_range_finish = int(self.main_window_obj.ui.random_range_edit_finish.text())

        amount_to_withdraw = float(min_amount) * (1 + random.uniform(random_range_start, random_range_finish) / 100)

        if not db_object.is_withdraw_address_set:
            print('Нет кошелька в вл, сначала добавьте его в вл')
            return False

        buffer_public_address = Web3Wallet(db_object).get_pub_key_from_prvt(db_object.withdraw_wallet_private_key)
        print(f'buffer wallet = {buffer_public_address}')

        chains = NetworksNames()
        bybit_chain_name = (await chains.get(binance_name=chain_name))[0]
        network: Networks = (await Networks().get(name=bybit_chain_name.name))[0]
        gas_coin_name = network.coin_symbol
        print(network)

        async with BybitSetUp(db_object) as bb:
            bybit_dep_address = await bb.get_deposit_address(coin=withdraw_coin, chain=bybit_chain_name.bybit_name)

        if not bybit_dep_address:
            print('Не удалось получить адрес депозита байбит')
            return False

        if gas_coin_amount:
            res = BinanceWithdraw().binance_withdraw(buffer_public_address, gas_coin_amount, gas_coin_name, chain_name)
            if not res:
                print('При выводе монет для газа произошла ошибка')
                return False
        else:
            print('Вывод газ коина не требуется')

        res = BinanceWithdraw().binance_withdraw(buffer_public_address, amount_to_withdraw, withdraw_coin, chain_name)
        if not res:
            print('При выводе монет произошла ошибка')
            return False

        network = (await Networks().get(name=bybit_chain_name.name))[0]
        print(network)
        client  = Client(private_key=db_object.withdraw_wallet_private_key, network=network)

        #usdt_sender = UsdtSender(client)
        async with UsdtSender(client) as usdt_sender:
            await usdt_sender.wait_fot_balance(amount_to_withdraw, gas_coin_amount)
            usdt_balance = usdt_sender.get_usdt_balance()
            res = await usdt_sender.send_usdt(bybit_dep_address, usdt_sender.get_usdt_balance())
            if res:
                await db_object.update(first_deposit_date=datetime.now())
                await db_object.update(deposit_amount=usdt_balance)
            return res




    async def set_up_start(self, db_object: BybitAccount):
        try:
            await self.sleep_after()

            res = await self.deposit(db_object)

            db_object.message = res if not res else 'Операция прошла успешно'
        except Exception as ex:
            print(f'При выполнении задачи произошло исключение {ex}')
            db_object.message = f'При выполнении задачи произошло исключение {ex}'

        return db_object



