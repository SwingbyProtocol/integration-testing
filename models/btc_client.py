import requests
import json
import os

from bit import PrivateKeyTestnet, wif_to_key
from bit.network import NetworkAPI, satoshi_to_currency

default_pkey = ""
testnet_priv_key = os.environ.get("BTC_PKEY", default_pkey)
key = wif_to_key(testnet_priv_key)
btc_address = key.address

class BtcClient:

  def get_balance_satoshi(self):
    self.get_balance()
    return key.balance

  def get_balance_block_cypher(self, address):
    endpoint = "https://api.blockcypher.com/v1/btc/test3/addrs/{}/balance".format(address)
    resp = requests.get(endpoint, stream=True, timeout=15)
    data = json.loads(resp.content)
    return float(data['balance'] / 100000000)

  def get_address_balance(self, address):
    val = satoshi_to_currency(NetworkAPI.get_balance_testnet(address), 'btc')
    return float(val)

  def get_address(self):
    return btc_address

  def get_balance(self):
    try:
      return self.get_balance_block_cypher(btc_address)
    except Exception as e:
      print ("Error in get balance:", e)
      return float(key.get_balance('btc'))

  def send_transaction(self, address, value):
    # https://ofek.dev/bit/guide/transactions.html#creating-and-signing
    raw = key.create_transaction([(address, value, 'btc')])
    NetworkAPI.broadcast_tx_testnet(raw)
