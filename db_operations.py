import asyncio

from PySide6.QtCore import QAbstractTableModel, Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QMessageBox
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from models.bybit_account import BybitAccount
from models.database import async_session
from utils.read_xlsx import read_excel


class SqlAlchemyTableModel(QAbstractTableModel):
    def __init__(self, data, headers=None):
        super().__init__()
        self._data = data
        self._headers = headers if headers else []
        self.toggled_cells = set()

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        if self._data:
            return len(self._headers)
        return 0

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        row = index.row()
        column = index.column()

        if role == Qt.DisplayRole:
            row_data = self._data[row]
            column_name = self._headers[column]
            value = getattr(row_data, column_name, "")
            return str(value)

        elif role == Qt.BackgroundRole:
            if (row, column) in self.toggled_cells:
                # Возвращаем более тёмный цвет, например, светло-серый
                return QColor("#c44dff")
            else:
                # Возвращаем стандартный цвет (можно изменить по необходимости)
                # return QColor("#FFFFFF")
                pass

        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            if section < len(self._headers):
                return self._headers[section].capitalize()
            return f"Column {section+1}"
        else:
            return str(section + 1)

    def toggle_cell(self, row, column, table_view_name):
        """
        Переключает состояние ячейки: если была темной, делает стандартной и наоборот.
        """

        cell = (row, column)

        if cell in self.toggled_cells:
            self.toggled_cells.remove(cell)
        else:
            self.toggled_cells.add(cell)

        #print(self.toggled_cells)

        # Уведомляем представление, что данные изменились
        index = self.index(row, column)
        self.dataChanged.emit(index, index, [Qt.BackgroundRole])

class Data:

    @staticmethod
    def read_excel_attempt(main_window_obj):
        print('read attempt')
        try:
            asyncio.run(read_excel())
        except Exception as ex:
            print(f'произошло исключение {ex}')
            QMessageBox.critical(main_window_obj, "произошло исключение", f'произошло исключение {ex}')

    @staticmethod
    async def get_data_from_db():
        async with async_session() as session:
            query = (
                select(BybitAccount).options(joinedload(BybitAccount.proxy)).options(joinedload(BybitAccount.email))
            )

            res = await session.execute(query)
            result = res.unique().scalars().all()


        return result

    @staticmethod
    def get_data():
        res = asyncio.run(Data.get_data_from_db())
        return res

    @staticmethod
    async def get_db_objects_from_id_list(id_list: list):
        async with async_session() as session:
            query = (
                select(BybitAccount)
                .options(joinedload(BybitAccount.proxy))
                .options(joinedload(BybitAccount.email))
                .filter(BybitAccount.id.in_(id_list))
            )

            res = await session.execute(query)
            result = res.unique().scalars().all()

        return result

if __name__ == '__main__':
    res = asyncio.run(Data().get_db_objects_from_id_list([5]))
    print(res)