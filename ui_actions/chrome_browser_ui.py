from db_operations import Data
from models.bybit_account import BybitAccount
from .ui_actions import UiActions
from chrome_browser.browser import launch_browser

import asyncio

class ChomeActions(UiActions):

    async def launch_tasks(self):
        id_list = self.get_clicked_items_id()
        db_objects = await Data.get_db_objects_from_id_list(id_list)

        tasks = []
        for db_object in db_objects:
            tasks.append(launch_browser(db_object))

        self.db_objects_list = await asyncio.gather(*tasks)

