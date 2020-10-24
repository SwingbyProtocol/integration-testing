import requests
import json
import math
import os

from utils import Decimal
from web3 import Web3, HTTPProvider

default_pkey = ""
priv_key = os.environ.get("ETH_PKEY", default_pkey)
eth_rpc = os.environ.get("ETH_RPC", "51.15.143.55:8545")

web3 = Web3(Web3.HTTPProvider(eth_rpc))
eth_account = web3.eth.account.privateKeyToAccount(priv_key)
eth_address = eth_account.address

erc20_abi = '[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"}]'
contracts = {
  "BTCE": {
    "address": web3.toChecksumAddress("0xeb47a21c1fc00d1e863019906df1771b80dbe182"),
    "decimals": 8,
    "abi": erc20_abi,
  }
}

wei = 1000000000000000000

class EthClient:

  def _symbol_is_valid(self, symbol):
    if symbol == "ETH":
      return
    if not contracts[symbol]:
      raise Exception("Invalid symbol", symbol)

  def get_address_balance(self, symbol, address):
    address = web3.toChecksumAddress(address)
    # verify input
    self._symbol_is_valid(symbol)
    if symbol == "ETH":
      # get balance for ETH
      return Decimal(web3.eth.getBalance(eth_address)) / wei
    # otherwise use erc20 contract
    instance = web3.eth.contract(
      address=contracts[symbol]["address"],
      abi=json.loads(contracts[symbol]["abi"])
    )
    balance = instance.functions.balanceOf(eth_address).call()
    return Decimal(balance) / math.pow(10, contracts[symbol]["decimals"])

  def get_address(self):
    return eth_address

  def get_balance(self, symbol):
    return self.get_address_balance(symbol, self.get_address())

  def send_transaction(self, address_to, symbol, value):
    address_to = web3.toChecksumAddress(address)
    # verify input
    self._symbol_is_valid(symbol)
    if symbol == "ETH":
      # build ETH transaction
      amnt = int(value * wei)
      tx = {
        'to': address_to,
        'value': amnt,
        'gas': 2000000,
        'gasPrice': web3.toWei('3', 'gwei'),
        'nonce': web3.eth.getTransactionCount(self.get_address()),
      }
    else:
      # build erc20 transaction
      instance = web3.eth.contract(
        address=contracts[symbol]["address"],
        abi=json.loads(contracts[symbol]["abi"])
      )
      amnt = int(value * math.pow(10, contracts[symbol]["decimals"]))
      tx = instance.functions.transfer(address_to, amnt).buildTransaction({
        'gas': 200000,
        'gasPrice': web3.toWei('3', 'gwei'),
        'nonce': web3.eth.getTransactionCount(self.get_address()),
      })
    # sign and broadcast tx
    signed_txn = web3.eth.account.signTransaction(tx, private_key=priv_key)
    return web3.eth.sendRawTransaction(signed_txn.rawTransaction)
