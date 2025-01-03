from models.bybit_account import BybitAccount
from .ui_actions import UiActions

class TsUi(UiActions):
    def __init__(self, main_window_obj):
        super().__init__(main_window_obj)
        self.function_name = 'register_in_TS'
        self.timer_name = 'ts_timer'


    def result_btn(self):
        from main import MainWindow
        self.main_window_obj: MainWindow
        ts_id = self.main_window_obj.ui.ts_edit.text()

        self.func_args = [ts_id]
        super().result_btn()

