import asyncio
from time import sleep
from typing import Optional, TYPE_CHECKING

from PySide6 import QtWidgets
from PySide6.QtCore import QModelIndex, Qt, QThread, Signal
from PySide6.QtGui import QColor

from db_operations import SqlAlchemyTableModel
from tasks.bybit_set_up import BybitSetUp
from db_operations import Data
from models.bybit_account import BybitAccount

from another_windows.wait_dialog_window import WaitTaskDialog
from another_windows.results_window import Ui_ResultsWindow
import time


class WorkerThread(QThread):
    progress = Signal(int)  # Сигнал для передачи прогресса
    #finished = Signal()     # Сигнал о завершении работы

    def __init__(self, ui_actions_object):
        super().__init__()
        self.ui_actions_object = ui_actions_object

    def run(self):
        asyncio.run(self.ui_actions_object.launch_tasks())



class UiActions:

    result_headers = []
    function_name = 'get_cookies'
    timer_name = 'main_timeEdit'
    func_args = []

    def __init__(self, main_window_obj):
        self.main_window_obj = main_window_obj
        self.clicked_value_dict = {}
        self.db_objects_list = []
        self.seconds = 0

    def clear_attributes(self):
        self.clicked_value_dict = {}
        self.db_objects_list = []
        self.seconds = 0

    def table_click(self, index: QModelIndex, table_view_name: str):
        row = index.row()

        id_value = self.main_window_obj.model.data(self.main_window_obj.model.index(row, 0), Qt.DisplayRole)
        if not self.clicked_value_dict.get(id_value):
            self.clicked_value_dict[id_value] = 1

        else:
            self.clicked_value_dict[id_value] += 1

        self.main_window_obj.model.toggle_cell(row, 0, table_view_name)
        print(self.clicked_value_dict)

    def get_clicked_items_id(self) -> list:
        if not len(self.clicked_value_dict):
            print('Нет выбраных ячеек')
            return []

        id_list = []
        for item in self.clicked_value_dict:
            if self.clicked_value_dict[item] % 2 == 1:
                id_list.append(item)

        return id_list

    def get_timer_info(self):
        try:
            timer_object = getattr(self.main_window_obj.ui, self.timer_name)

            minutes = timer_object.time().minute()
            seconds = timer_object.time().second()

            self.seconds = minutes * 60 + seconds

        except Exception as ex:
            print(f'не удалось получить заначение задержки , произошло исключение  = {ex}')


    def task_interrupted(self):
        self.main_window_obj.new_window.close()  # Закрываем информационное окно
        self.main_window_obj.ui.result_btn.setEnabled(True)
        print("Операция прервана пользователем")
        self.cancel_task()

    def cancel_task(self):
        # Останавливаем поток
        if self.thread.isRunning():
            self.thread.terminate()
            self.thread.wait()

    def result_btn(self):
        self.get_timer_info()

        self.main_window_obj.ui.result_btn.setEnabled(False)
        self.main_window_obj.new_window = QtWidgets.QDialog()
        self.progress_dialog = WaitTaskDialog()
        self.progress_dialog.setupUi(self.main_window_obj.new_window)
        #self.main_window_obj.new_window.rejected.connect(self.task_interrupted)
        self.main_window_obj.new_window.show()

        self.thread = WorkerThread(self)
        #self.thread.progress.connect(self.update_progress)
        self.thread.progress.connect(lambda value: self.progress_dialog.progressBar.setValue(value))
        self.thread.finished.connect(self.task_finished)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()


        #asyncio.run(self.buffer())

    def update_progress(self, value):
        self.progress_dialog.progressBar.setValue(value)

    def task_finished(self):
        self.main_window_obj.new_window.close()   # Закрываем информационное окно
        self.main_window_obj.ui.result_btn.setEnabled(True)   # Включаем кнопку обратно
        print("Операция завершена")

        self.show_result_window()

    def show_result_window(self, headers: Optional[list]=None):
        self.main_window_obj.new_window = QtWidgets.QDialog()
        self.result_dialog = Ui_ResultsWindow()
        self.result_dialog.setupUi(self.main_window_obj.new_window)
        self.main_window_obj.new_window.show()

        headers = self.result_headers if self.result_headers else \
            ['id', 'bybit_id', 'group_name', 'email', 'email_pass', 'message']

        self.model = SqlAlchemyTableModel(self.db_objects_list,
                                          headers=headers)
        self.result_dialog.tableView.setModel(self.model)


    async def set_up_start(self, db_object: BybitAccount):
        try:
            async with BybitSetUp(db_object) as bb:
                func = getattr(bb, self.function_name)
                res = await func(*self.func_args)
                print(res)



                db_object.message = res if not res else 'Операция прошла успешно'
        except Exception as ex:
            print(f'При выполнении задачи произошло исключение {ex}')
            db_object.message = f'При выполнении задачи произошло исключение {ex}'

        #await self.sleep_after()

        return db_object

    def sleep_after(self, time_to_sleep=None):
        time_to_sleep = self.seconds if not time_to_sleep else time_to_sleep
        time.sleep(time_to_sleep)

    async def filter_db_objects_list(self):
        buffer_list = []

        for i in self.db_objects_list:
            if isinstance(i, BybitAccount):
                buffer_list.append(i)

        print(buffer_list)

    async def launch_tasks(self):
        if self.seconds:
            print(f'Задержка между акками = {self.seconds}')
            await self.sync_launch_tasks()
            return None

        print('Начинаю ассинхронное выполнение')

        id_list = self.get_clicked_items_id()
        db_objects = await Data.get_db_objects_from_id_list(id_list)

        tasks = []
        for db_object in db_objects:
            tasks.append(self.set_up_start(db_object))

        self.db_objects_list = await asyncio.gather(*tasks)

    async def sync_launch_tasks(self):
        print('Задержка включена, начинаем синхронное выполнение')

        id_list = self.get_clicked_items_id()
        db_objects = await Data.get_db_objects_from_id_list(id_list)

        db_objects_list = []
        for db_object in db_objects:
            db_objects_list.append(await self.set_up_start(db_object))
            self.sleep_after()

        self.db_objects_list = db_objects_list

