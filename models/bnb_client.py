import os
from binance_chain.http import HttpApiClient
from binance_chain.messages import TransferMsg, Transfer
from binance_chain.wallet import Wallet
from binance_chain.environment import BinanceEnvironment


default_pkey = ""
testnet_env = BinanceEnvironment.get_testnet_env()
testnet_priv_key = os.environ.get("BNB_PKEY", default_pkey)
wallet = Wallet(testnet_priv_key, env=testnet_env)
bnb_address = wallet.address
client = HttpApiClient(env=testnet_env)

class BnbClient:

  def get_address(self):
    return bnb_address

  def get_address_account(self, address):
    return client.get_account(address)

  def get_account(self):
    return self.get_address_account(bnb_address)

  def get_address_balance(self, symbol, address):
    balances = self.get_address_account(address)['balances']
    print (symbol)
    print (balances)
    for b in balances:
      if b['symbol'] == symbol:
        return float(b['free'])

  def get_balance(self, symbol):
    return self.get_address_balance(symbol, bnb_address)

  def send_transaction(self, address, symbol, value, memo="Send from swingby integration-tester"):
    transfer_msg = TransferMsg(
      wallet=wallet,
      symbol=symbol,
      amount=value,
      to_address=address,
      memo=memo
    )
    client.broadcast_msg(transfer_msg, sync=True)
