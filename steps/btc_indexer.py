import time
import json
import utils
import re
import asyncio
from behave import given, when, then, step
from models import BtcIndexerClient, block_cypher_client, SwingbyNode
from behave.api.async_step import async_run_until_complete
import asyncio
from behave import use_step_matcher

running_clients = {}
count_clients_started = 0

api_clients = {
  "BlockCypher": block_cypher_client
}

INDEX_URL = "wss://testnet-indexer.swingby.network/ws"

def start_btc_indexer_client(context):
  global running_clients
  global count_clients_started
  client = BtcIndexerClient(INDEX_URL)
  count_clients_started += 1
  running_clients[count_clients_started] = client
  return client

@then('all indexer clients are disposed')
@async_run_until_complete
@asyncio.coroutine
async def step_impl(context):
  global running_clients
  try:
    for v in running_clients.values():
      await v.on_close()
  except Exception:
    pass

@when('I start a new BTC indexer instance')
def step_impl(context):
  context_client = start_btc_indexer_client(context)
  context_client._start_new_socket()
  context_client._wait_for_socket(0)
  context.client = context_client

@then('all BTC indexer clients are stopped')
def step_impl(context):
  global running_clients
  for rn in running_clients:
    rn["client"].close()

@when('a "{action:S}" action is sent to the BTC indexer for address "{address:S}"')
@async_run_until_complete
@asyncio.coroutine
async def step_send_action(context, action, address):
  client = get_client_with_context(context)
  await client.send_action(action, { "address": address })

@when('a ping action is sent to the BTC indexer')
@async_run_until_complete
@asyncio.coroutine
async def step_impl(context):
  client = context.client
  await client.send_ping()

@then('the indexer height should be within {amount:d} block of it')
@async_run_until_complete
@asyncio.coroutine
async def step_impl(context, amount):
  indexer = context.client
  api_height = context.last_height
  # get height from indexer
  await indexer.get_transactions("n37eRzDmZhDcLxRixwEvmemeWBHUUoRSRM")
  # wait for txid response
  def check_responses():
    if len(indexer.responses) > 0:
      res = json.loads(indexer.responses[-1:][0])
      print ("Indexer height = {}".format(res["height"]))
      if res['height'] > api_height - amount and res['height'] < api_height + amount:
        # in sync
        return True
  if not utils.wait_until(check_responses, timeout=10, label="Waiting for latest tx from indexer"):
    raise Exception("Did not receive correct indexer height for 10 seconds")

@when('I get the current BTC height from "{api}"')
def step_impl(context, api):
  client = api_clients[api]
  if not client:
    raise Exception("Unknown client {}".format(api))
  height = client.get_height()
  if not height or height < 1:
    raise Exception("Invalid height {}".format(height))
  print ("{} block height = {}", api, height)
  context.last_height = height

@step('I get the latest BTC transaction from "{api}"')
def step_impl(context, api):
  client = api_clients[api]
  if not client:
    raise Exception("Unknown client {}".format(api))
  tx = client.get_latest_tx()
  if not tx:
    raise Exception("get_latest_tx returned None")
  context.latest_btc_tx = tx

@then('the indexer should recognise the latest BTC transaction')
@async_run_until_complete
@asyncio.coroutine
async def step_impl(context):
  indexer  = context.client
  tx = context.latest_btc_tx
  tx_hash = tx["hash"]
  await indexer.get_transaction(tx_hash, mempool=True)
  # wait for txid response
  async def check_responses():
    if len(indexer.responses) > 0:
      res = json.loads(indexer.responses[-1:][0])
      indexer_tx = res
      print (indexer_tx)
      if indexer_tx['txid'] == tx_hash["hash"]:
        # found match
        return True
    await indexer.get_transaction(tx_hash, mempool=True)
  if not await utils.async_wait_until(check_responses, timeout=5, period=1, label="Waiting for latest tx from indexer"):
    raise Exception("Did not recognise latest tx")

use_step_matcher("re")

@then(u'I will receive a response containing the regex "(?P<reg>.*)" from the indexer')
def step_impl(context, reg):
  client = context.client
  def check_responses():
    if len(client.responses) > 0:
      x = re.search(reg, client.responses[-1:][0])
      if x:
        # found match
        return True
  if not utils.wait_until(check_responses, timeout=20, label="Waiting for node startup"):
    raise Exception("Did not receive response matching regex", reg)
