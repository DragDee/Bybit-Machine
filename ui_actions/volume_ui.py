import time
import random

from models.bybit_account import BybitAccount
from .editable_list_view import EditingListView
from .ui_actions import UiActions

class VolumeUi(UiActions, EditingListView):
    def __init__(self, main_window_obj):
        super().__init__(main_window_obj)
        #self.function_name = 'make_volume'
        self.function_name = 'warm_up'
        self.timer_name = 'volume_timer'

        UiActions.__init__(self, main_window_obj)
        EditingListView.__init__(self, main_window_obj.ui.symbol_edit, main_window_obj.ui.VolumelistWidget)


    def result_btn(self):
        from main import MainWindow
        self.main_window_obj: MainWindow

        #symbol = self.main_window_obj.ui.symbol_edit.text()
        symbols = self.get_list_widget_contents()
        print(symbols)
        volume = float(self.main_window_obj.ui.volume_edit.text())
        range_start = int(self.main_window_obj.ui.volume_range_start.text())
        range_finish = int(self.main_window_obj.ui.volume_range_finish.text())

        self.func_args = [symbols, volume, (range_start, range_finish)]

        action = []
        if self.main_window_obj.ui.volume_checkBox.isChecked():
            action.append('volume')
        if self.main_window_obj.ui.loan_checkBox.isChecked():
            action.append('loan')
        if self.main_window_obj.ui.close_loan_chechbox.isChecked():
            action.append('close_loans')

        self.func_args.insert(0, action)

        super().result_btn()

