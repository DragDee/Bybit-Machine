import time
import random

from models.bybit_account import BybitAccount
from tasks.bybit_set_up import BybitSetUp
from .editable_list_view import EditingListView
from .ui_actions import UiActions

class ExactCoinUi(UiActions, EditingListView):
    def __init__(self, main_window_obj):
        super().__init__(main_window_obj)
        #self.function_name = 'make_volume'
        self.function_name = 'get_exact_coin_balance'
        self.timer_name = 'volume_timer'

        UiActions.__init__(self, main_window_obj)

    def result_btn(self):
        from main import MainWindow
        self.main_window_obj: MainWindow

        coin = (self.main_window_obj.ui.exact_coin_lineEdit.text()).upper()
        self.func_args = [coin]

        super().result_btn()

    async def set_up_start(self, db_object: BybitAccount):
        try:
            async with BybitSetUp(db_object) as bb:
                func = getattr(bb, self.function_name)
                res = await func(*self.func_args)
                print(res)



                db_object.message = res
        except Exception as ex:
            print(f'При выполнении задачи произошло исключение {ex}')
            db_object.message = f'При выполнении задачи произошло исключение {ex}'

        #await self.sleep_after()

        return db_object