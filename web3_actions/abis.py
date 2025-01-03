import os
import sys
from pathlib import Path

if getattr(sys, 'frozen', False):
    ROOT_DIR = Path(sys.executable).parent.absolute()
else:
    ROOT_DIR = Path(__file__).parent.parent.absolute()

ABIS_DIR = os.path.join(ROOT_DIR, 'web3_actions/abis')

USDT_ABI = os.path.join(ABIS_DIR, 'usdt.json')
TOKEN_ABI = os.path.join(ABIS_DIR, 'token.json')