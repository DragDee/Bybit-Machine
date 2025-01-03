import time

from db_operations import Data
from models.bybit_account import BybitAccount
from .ui_actions import UiActions
from chrome_browser.browser import launch_browser

import asyncio

class WithdrawActions(UiActions):
    function_name = 'full_automatic_withdraw'
    timer_name = 'withdraw_timeEdit'

    def get_withdraw_mode(self):
        self.func_args = []

        if self.main_window_obj.ui.radioButton.isChecked():
            self.func_args.append(1)
        elif self.main_window_obj.ui.radioButton_2.isChecked():
            self.func_args.append(2)
        elif self.main_window_obj.ui.radioButton_3.isChecked():
            self.func_args.append(3)

    def result_btn(self):
        self.get_withdraw_mode()
        super().result_btn()


