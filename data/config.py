import sys
import os
from pathlib import Path

from utils.read_config_file import read_keys_from_file

DATABASE_NAME = 'application_main.sqlite'

def get_application_path():
    if hasattr(sys, '_MEIPASS'):
        # Для PyInstaller, но мы используем Nuitka
        application_path = sys._MEIPASS
    elif sys.executable:
        # Для Nuitka
        application_path = os.path.dirname(os.path.abspath(sys.executable))
    else:
        # Для запуска из исходного кода
        application_path = os.path.dirname(os.path.abspath(__file__))
    return application_path

if getattr(sys, 'frozen', False):
    #ROOT_DIR = Path(sys.executable).parent.absolute()
    ROOT_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
else:
    ROOT_DIR = Path(__file__).parent.parent.absolute()
    #ROOT_DIR = os.path.dirname(os.path.abspath(__file__))



DATABASE_NAME = os.path.join(ROOT_DIR, DATABASE_NAME)
DATABASE_CONNECTION = f'sqlite+aiosqlite:///{DATABASE_NAME}'
SYNC_DATABASE_CONNECTION = f'sqlite:///{DATABASE_NAME}'

config_dict = read_keys_from_file(os.path.join(ROOT_DIR, 'data', 'conf.txt'))

TWO_CAPTCHA_KEY   = config_dict.get("TWO_CAPTCHA_KEY")
binance_api_key   = config_dict.get("binance_api_key")
binance_prvt_key  = config_dict.get("binance_prvt_key")
MAIN_EVM_WALLET   = config_dict.get("MAIN_EVM_WALLET")

