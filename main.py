
import asyncio
import sys
import os
import platform
from symtable import Class
from typing import Optional

from models.database import async_session
from ui_actions.exact_coin_ui import ExactCoinUi
from ui_actions.ts_ui import TsUi
from ui_actions.volume_ui import VolumeUi
from utils.read_xlsx import read_excel

from sqlalchemy.orm import joinedload
from sqlalchemy import select
from models.bybit_account import BybitAccount
from db_operations import SqlAlchemyTableModel, Data
from ui_actions.ui_actions import UiActions
from ui_actions.chrome_browser_ui import ChomeActions
from ui_actions.withdraw_ui_actions import WithdrawActions
from ui_actions.data_ui_actions import DataUiActions

from another_windows.wait_dialog_window import WaitTaskDialog

from modules import *
from widgets import *
from main_window import Ui_MainWindow
from ui_actions.set_up_actions import SetUpActions
from ui_actions.main_ui_page import MainUiActions
from ui_actions.deposit_ui import DepositUi
os.environ["QT_FONT_DPI"] = "135" # FIX Problem for High DPI and Scale above 100%


widgets = None


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui

        Settings.ENABLE_CUSTOM_TITLE_BAR = True

        title = "BYBIT MACHINE"
        description = "Bybit automation soft"
        self.setWindowTitle(title)
        widgets.titleRightInfo.setText(description)


        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))


        UIFunctions.uiDefinitions(self)

        widgets.btn_home.clicked.connect(self.buttonClick)
        widgets.btn_widgets.clicked.connect(self.buttonClick)
        widgets.btn_new.clicked.connect(self.buttonClick)
        widgets.btn_save.clicked.connect(self.buttonClick)
        self.ui.btn_exit.clicked.connect(self.buttonClick)
        self.ui.deposit_btn.clicked.connect(self.buttonClick)
        self.ui.register_in_ts_btn.clicked.connect(self.buttonClick)
        self.ui.volume_btn.clicked.connect(self.buttonClick)
        self.ui.exact_coin_menu.clicked.connect(self.buttonClick)


        def openCloseLeftBox():
            UIFunctions.toggleLeftBox(self, True)
        widgets.toggleLeftBox.clicked.connect(openCloseLeftBox)
        widgets.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)


        def openCloseRightBox():
            UIFunctions.toggleRightBox(self, True)
        widgets.settingsTopBtn.clicked.connect(openCloseRightBox)

        self.show()

        useCustomTheme = False
        themeFile = "themes\py_dracula_light.qss"

        if useCustomTheme:
            UIFunctions.theme(self, themeFile, True)

            AppFunctions.setThemeHack(self)

        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))

        self.clicked_buttons = set()


    def activate_table_view(self, table_view_name: str, ui_action_class, btn_dict: Optional[dict] = None, headers=None):
        #print(ui_action.clicked_value_dict)

        table_view_object = getattr(self.ui, table_view_name)

        self.model = SqlAlchemyTableModel(Data.get_data(),
                                          headers=['id', 'bybit_id', 'group_name', 'email', 'password',
                                                   'is_registered', 'kyc_level', 'is_password_changed', 'last_ts_registered'])
        table_view_object.setModel(self.model)

        if table_view_name not in self.clicked_buttons:
            ui_action = ui_action_class(self)
            setattr(self, f'{table_view_name}_ui_action', ui_action)

            self.clicked_buttons.add(table_view_name)

            table_view_object.clicked.connect(lambda x: ui_action.table_click(x, table_view_name))


            if btn_dict:
                for btn_con, func in btn_dict.items():
                    btn = getattr(self.ui, btn_con)
                    if isinstance(func, str):
                        func = getattr(ui_action, func)
                    btn.clicked.connect(func)


        ui_action = getattr(self, f'{table_view_name}_ui_action')
        ui_action.clear_attributes()

    def buttonClick(self):
        btn = self.sender()
        btnName = btn.objectName()

        if btnName == "btn_home":
            widgets.stackedWidget.setCurrentWidget(widgets.home)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

            btn_dict = {
                'result_btn': 'result_btn',
                #'add_accs_button': lambda: Data.read_excel_attempt(self),
                'add_accs_button': 'read_excel',
                'register_btn': 'register_btn'
            }
            self.activate_table_view(table_view_name='tableView', ui_action_class=MainUiActions, btn_dict=btn_dict)

        if btnName == "btn_widgets":
            widgets.stackedWidget.setCurrentWidget(widgets.widgets)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

            self.activate_table_view(
                btn_dict={
                    'set_up_button': 'result_btn'
                },
                ui_action_class=SetUpActions,
                table_view_name='tableView_set_up'
            )


        if btnName == "btn_new":
            widgets.stackedWidget.setCurrentWidget(widgets.new_page) # SET PAGE
            UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU

            self.activate_table_view(
                btn_dict={
                    'launch_profile_btn': 'result_btn'
                },
                ui_action_class=ChomeActions,
                table_view_name='launch_profile_table_view'
            )

        if btnName == "btn_save":
            print("Save BTN clicked!")
            widgets.stackedWidget.setCurrentWidget(widgets.withdraw)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

            self.activate_table_view(
                btn_dict={
                    'launch_withdraw_btn': 'result_btn'
                },
                ui_action_class=WithdrawActions,
                table_view_name='withdraw_tableView'
            )

        if btnName == 'btn_exit':
            print("exit BTN clicked!")
            widgets.stackedWidget.setCurrentWidget(widgets.data)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

            self.activate_table_view(
                btn_dict={
                    'listView': 'on_ListView_item_clicked',
                    'data_btn': 'result_btn'
                },
                ui_action_class=DataUiActions,
                table_view_name='data_tableView'
            )

            print(f'Button "{btnName}" pressed!')

        if btnName == 'deposit_btn':
            print("exit BTN clicked!")
            widgets.stackedWidget.setCurrentWidget(widgets.deposit)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

            self.activate_table_view(
                btn_dict={
                    'deposit_btn_launch': 'result_btn'
                },
                ui_action_class=DepositUi,
                table_view_name='deposit_tableView'
            )


            print(f'Button "{btnName}" pressed!')

        if btnName == 'register_in_ts_btn':
            print("register in Ts")
            self.ui.stackedWidget.setCurrentWidget(self.ui.tokensplash)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

            self.activate_table_view(
                btn_dict={
                    'register_in_st_btn': 'result_btn'
                },
                ui_action_class=TsUi,
                table_view_name='ts_tableView'
            )

            print(f'Button "{btnName}" pressed!')

        if btnName == 'volume_btn':
            print("Volume")
            self.ui.stackedWidget.setCurrentWidget(self.ui.volume)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

            self.activate_table_view(
                btn_dict={
                    'launch_volume_btn': 'result_btn'
                },
                ui_action_class=VolumeUi,
                table_view_name='volumeTableView'
            )

            print(f'Button "{btnName}" pressed!')

        if btnName == 'exact_coin_menu':
            self.ui.stackedWidget.setCurrentWidget(self.ui.exact_coin_balance)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

            self.activate_table_view(
                btn_dict={
                    'exact_coin_pushButton': 'result_btn'
                },
                ui_action_class=ExactCoinUi,
                table_view_name='coin_balance_tableView'
            )

            print(f'Button "{btnName}" pressed!')


    def resizeEvent(self, event):
        UIFunctions.resize_grips(self)

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')

if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    sys.exit(app.exec())

