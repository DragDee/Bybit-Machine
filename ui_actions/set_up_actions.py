from models.bybit_account import BybitAccount
from .ui_actions import UiActions

class SetUpActions(UiActions):
    def __init__(self, main_window_obj):
        super().__init__(main_window_obj)
        self.function_name = 'full_set_up'
        self.timer_name = 'set_up_timeEdit'


    def get_checkbox_list(self):
        checkbox_list = []

        from main import MainWindow
        self.main_window_obj: MainWindow

        if self.main_window_obj.ui.fa2_checkbox.isChecked():
            checkbox_list.append('add_2fa')
        if self.main_window_obj.ui.wl_on_checkbox.isChecked():
            checkbox_list.append('enable_whitelist_withdraw')
        if self.main_window_obj.ui.add_wallet_checkbox.isChecked():
            checkbox_list.append('generate_address_add_to_whitelist')
        if self.main_window_obj.ui.only_wl_checkbox.isChecked():
            checkbox_list.append('withdraw_via_whitelist_only')
        if self.main_window_obj.ui.block_checkbox.isChecked():
            checkbox_list.append('block_new_withdraw_address')
        if self.main_window_obj.ui.change_password_checkbox.isChecked():
            checkbox_list.append('change_password')

        return checkbox_list

    def result_btn(self):
        self.func_args = [self.get_checkbox_list()]
        print(self.func_args)
        super().result_btn()

