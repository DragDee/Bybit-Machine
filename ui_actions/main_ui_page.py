from PySide6.QtWidgets import QMessageBox

from utils.read_xlsx import read_excel
from .ui_actions import UiActions


import asyncio

class MainUiActions(UiActions):

    def register_btn(self):
        args = dict()
        self.function_name = 'register_manager'

        try:
            args['affilate_id'] = int(self.main_window_obj.ui.affilate_id_input.text())
            args['group_id'] = int(self.main_window_obj.ui.group_id_input.text())
            args['group_type'] = int(self.main_window_obj.ui.group_type_edit.text())
        except:
            print('рефф параметры должны быть в формате int')

        self.func_args = [args]

        self.result_btn()
        #self.function_name = 'get_cookies'


    def read_excel(self):
        print('read attempt')
        try:
            start = int(self.main_window_obj.ui.excel_start_edit.text())
            finish = int(self.main_window_obj.ui.excel_finish_edit.text()) + 1
            asyncio.run(read_excel(start, finish))
        except Exception as ex:
            print(f'произошло исключение {ex}')
            QMessageBox.critical(self.main_window_obj, "произошло исключение", f'произошло исключение {ex}')


