
import time

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from chrome_browser.set_up_driver import DriverSetUp
from models.bybit_account import BybitAccount
import asyncio

from models.database import async_session


class GetDriver:

    def __init__(self, bybit_acc : BybitAccount):
        self.bybit_acc = bybit_acc

    def return_driver(self):
        driver_set_up = DriverSetUp()
        useragent = self.bybit_acc.user_agent
        print("Запускаем браузер")
        driver = driver_set_up.get_chromedriver(
                                        proxy=self.bybit_acc.proxy,
                                        user_agent=useragent,
                                        headless=True)

        return driver


async def launch_browser(db_object: BybitAccount):
        driver = GetDriver(db_object).return_driver()

        try:
            driver.get('https://www.bybit.com/login')
            driver.maximize_window()


            cookies = db_object.cookies
            driver.delete_all_cookies()
            for cookie in cookies:

                if not cookie['domain']:
                    cookie['domain'] = 'bybit.com'
                if not cookie['path']:
                    cookie['path'] = '/'
                if not cookie['expirationDate']:
                    cookie['expirationDate'] = time.time() + 10 ** 7

                cookie['domain'] = 'bybit.com'

                try:
                    driver.add_cookie(cookie)
                except Exception as ex:
                    print(cookie)
                    print(f'Exeption {ex}')

            driver.refresh()
            driver.get('https://www.bybit.com')
            driver.refresh()

            await asyncio.sleep(1200)

        except Exception as exs:

            print("исключение")
            print(exs)

            driver.quit()

