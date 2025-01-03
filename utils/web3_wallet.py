import secrets
from eth_account import Account
import mnemonic
from models.bybit_account import BybitAccount


class Web3Wallet:

    def __init__(self, bybit_account: BybitAccount):
        self.bybit_account = bybit_account

    def generate_mnemonic(self):
        mnemo = mnemonic.Mnemonic("english")
        return mnemo.generate(strength=128)

    def generate_wallet_from_mnemonic(self, mnemonic_phrase):
        Account.enable_unaudited_hdwallet_features()

        seed = mnemonic.Mnemonic.to_seed(mnemonic_phrase, passphrase="")
        account = Account.from_mnemonic(mnemonic_phrase)
        return account.address

    def get_private_key_from_mnemonic(self, mnemonic_phrase):
        Account.enable_unaudited_hdwallet_features()
        account = Account.from_mnemonic(mnemonic_phrase)
        private_key = account.key.hex()
        return private_key

    def get_pub_key_from_prvt(self, prvt_key: str):
        account = Account.from_key(prvt_key)
        return account.address

    async def generate_wallet_and_save_to_db(self):
        mnemonic_phrase = self.generate_mnemonic()
        prvt_key = self.get_private_key_from_mnemonic(mnemonic_phrase)
        await self.bybit_account.update(withdraw_wallet_private_key=prvt_key)

        return prvt_key

