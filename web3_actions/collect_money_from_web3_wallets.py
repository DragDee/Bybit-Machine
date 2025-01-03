import asyncio
import json

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import joinedload


from models.bybit_account import BybitAccount
from models.database import async_session
from models.networks import Networks
from web3_actions.client import Client
from models.proxy import Proxy



def read_json(path: str, encoding: Optional[str] = None) -> dict:
    return json.load(open(path, encoding=encoding))

class WalletCollector:

    def __init__(self, client: Client):
        self.client = client


    def collect(self, destination_address: str, amount: Optional[float]=None, part: Optional[float]=None):

        last_block = self.client.w3.eth.get_block('latest')
        native_balance = self.client.w3.eth.get_balance(self.client.address)
        if not amount:
            amount = self.client.w3.eth.get_balance(self.client.address)

        if part:
            amount = int(amount * part)

        max_fee_per_gas = self.client.get_max_fee_per_gas()
        tx_cost = int(self.client.gasLimit * max_fee_per_gas * Client.gasBoost)

        '''print(f'custom gas = {int(tx["gas"] * Client.gasBoost)}')
        print(f'custom maxfeepergas = {max_fee_per_gas}')
        print(f'custom tx fee = {tx_cost}')'''

        amount = amount - tx_cost

        tx = self.client.send_transaction(
            to=destination_address,
            value=amount
        )

        res = self.client.verif_tx(tx_hash=tx)

        print(res)


async def custom_main(id):
    async with async_session() as session:
        query = (
            select(BybitAccount).options(joinedload(BybitAccount.email))
        )

        res = await session.execute(query)
        result = res.unique().scalars().all()
        db_object = result[id]
        print(db_object)

    network = (await Networks().get(name='arbitrum'))[0]
    print(network)
    client = Client(private_key=db_object.withdraw_wallet_private_key, network=network)

    wc = WalletCollector(client=client)
    wc.collect(destination_address='0x864ba8f0e31E9b8511d4Cd7ff12F84Bb859e2Fef')

if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(custom_main(id=145))


