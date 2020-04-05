"""
Module used to describe a BtcIndexerClient object
"""
import json
from .websocket import GenericWebsocket

class BtcIndexerClient(GenericWebsocket):

  responses = []

  def __init__(self, host, *args, **kwargs):
    self.host = host
    super(BtcIndexerClient, self).__init__(host, *args, **kwargs)

  async def on_message(self, socketId, message):
    self.responses += [message]

  async def send_action(self, action, data):
    payload = { "action": action, "params": data }
    raw = json.dumps(payload)
    print ("SEND", raw)
    await self.get_socket(0).ws.send(raw)

  async def get_transactions(self, address, mempool=False):
    await self.send_action("getTxs", { "address": address, "mempool": mempool })

  async def get_transaction(self, tx_hash, mempool=False):
    await self.send_action("getTx", { "txid": tx_hash, "mempool": mempool })

  async def send_ping(self):
    await self.send_action("ping", {})

  def close(self):
    pass
