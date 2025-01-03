from PySide6.QtCore import QStringListModel, QModelIndex
from PySide6.QtGui import QColor, QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QListView

from db_operations import Data
from models.bybit_account import BybitAccount
from tasks.bybit_set_up import BybitSetUp
from .ui_actions import UiActions

class DataUiActions(UiActions):
    def __init__(self, main_window_obj):
        super().__init__(main_window_obj)
        self.function_name = 'full_set_up'
        self.timer_name = 'data_time'

        self.result_headers = ['id', 'bybit_id', 'group_name', 'email', 'email_pass', 'message']

        self.selected_items = []



        self.items_dict = {
            "Уровень кус": ['get_kyc_level', 'kyc_level'],#Название функции, имя функции, имя столбца в таблице
            "Баланс": ['get_total_balance', 'balance'],
            "Метка на тс": ['', ''],
        }
        self.items = []

        self.set_up_listView()

    def set_up_listView(self):
        # Создаем модель данных
        self.ListViewModel = QStandardItemModel()
        self.items = [item for item, value in self.items_dict.items()]
        for item_name in self.items:
            item = QStandardItem(item_name)
            self.ListViewModel.appendRow(item)

        # Создаем QListView и устанавливаем модель
        self.main_window_obj.ui.listView.setModel(self.ListViewModel)
        self.main_window_obj.ui.listView.setSelectionMode(QListView.NoSelection)

    '''def result_btn(self):
        print(self.selected_items)'''

    def on_ListView_item_clicked(self, index: QModelIndex):
        item = self.ListViewModel.itemFromIndex(index)
        item_text = item.text()
        if item_text in self.selected_items:
            # Если элемент уже выбран, снять выбор
            self.selected_items.remove(item_text)
            # Установить исходный цвет
            item.setBackground(QColor(40, 44, 52))
            item.setForeground(QColor("white"))
        else:
            # Добавить элемент в список выбранных
            self.selected_items.append(item_text)
            # Установить фиолетовый цвет
            item.setBackground(QColor("purple"))
            item.setForeground(QColor("white"))



    async def set_up_start(self, db_object: BybitAccount):
        try:
            async with BybitSetUp(db_object) as bb:
                if not hasattr(db_object, 'message'):
                    db_object.message = ''

                for bb_func_name in self.selected_items:
                    func = getattr(bb, self.items_dict.get(bb_func_name)[0])
                    res = await func(*self.func_args)
                    print(res)

                    db_object.message += str(res) if res != True else f'Операция {bb_func_name} прошла успешно '

                    if self.items_dict.get(bb_func_name)[1] not in self.result_headers:
                        self.result_headers.append(self.items_dict.get(bb_func_name)[1])


                #await self.sleep_after()

                #db_object.message = res if not res else 'Операция прошла успешно'
        except Exception as ex:
            print(f'При выполнении задачи произошло исключение {ex}')
            db_object.message = f'При выполнении задачи произошло исключение {ex}'

        return db_object

