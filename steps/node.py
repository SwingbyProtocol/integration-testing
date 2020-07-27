import os
import datetime
import time
import shutil
import utils
from behave import given, when, then, step, use_step_matcher
from models import SwingbyNode, testnet_node
from models import BnbClient
from models import BtcClient
import random

btc_client = BtcClient()
bnb_client = BnbClient()

start_time = datetime.datetime.now()
# collection of currently running nodes
running_nodes = {}
# count of nodes started (used for calculating port)
count_nodes_started = 0

def _get_node_executable():
  executable_path = os.environ.get("SW_EXEC", None)
  if executable_path == None:
    raise EnvironmentError("No executable file found for Swingby node")
  return executable_path

def _get_main_dir():
  return os.getcwd()

def _get_tmp_dir():
  time_str =  str(start_time)
  # 2019-10-24 17:16:26.474808 -> 2019-10-24_17-20-43-378372
  clean_str = time_str.replace(' ', '_', 1).replace(':', '-', 2).replace('.', '-', 1)
  return os.path.join(_get_main_dir(), 'tmp', clean_str)

def _copy_test_config_to_dir(tmp_dir, preset):
  test_cfg = os.path.join(_get_main_dir(), 'presets', 'test_cfg_{}.toml'.format(str(preset)))
  tmp_cfg = os.path.join(tmp_dir, 'config.toml')
  shutil.copyfile(test_cfg, tmp_cfg)

def _copy_test_keystore_to_dir(tmp_dir, preset):
  test_store = os.path.join(_get_main_dir(), 'presets', 'test_keystore_{}.json'.format(str(preset)))
  tmp_store = os.path.join(tmp_dir, 'data', 'keystore.json')
  shutil.copyfile(test_store, tmp_store)

def _create_node_tmp_home(path, node_id, preset=1):
  # create node tmp directory
  if not os.path.exists(path):
    os.makedirs(path)
    os.makedirs(os.path.join(path, 'data'))
  # copy tmp config into new path
  _copy_test_config_to_dir(path, preset)
  # copt tmp keystore into new path
  _copy_test_keystore_to_dir(path, preset)
  return path

def start_swingby_node(flags=""):
  global running_nodes
  global count_nodes_started
  node_exec = _get_node_executable()
  node_id = count_nodes_started
  node_home = os.path.join(_get_tmp_dir(), str(node_id))
  new_node = SwingbyNode(node_id, node_home, node_exec, flags=flags)
  # create new temp folder for node with test cfg
  _create_node_tmp_home(node_home, node_id, new_node.preset)
  # run os cmd to start binary and point to test cfg
  new_node = SwingbyNode(node_id, node_home, node_exec, flags=flags)
  new_node.start()
  # add to collection of running nodes
  running_nodes[node_id] = new_node
  count_nodes_started += 1
  return new_node

def stop_swingby_node(node):
  # run os cmd to kill binary
  # remove from running_nodes
  pass

def stop_all_swingby_nodes():
  for rn in running_nodes:
    stop_swingby_node(rn)

def start_count_nodes(count):
  node = None
  for _ in range(count):
    node = start_swingby_node()
  return node

@when('I start a new local Swingby node instance with the id "{id:S}"')
def step_impl(context, id):
  if not hasattr(context, 'swingby_nodes_map'):
    context.swingby_nodes = {}
  if not hasattr(context, 'swingby_nodes'):
    context.swingby_nodes = []
  node = start_swingby_node()
  context.swingby_node = node
  context.swingby_nodes_map[id] = node
  context.swingby_nodes += [node]

@when('I start a {number:d} local Swingby node instances')
def step_impl(context, number):
  context.swingby_node  = start_count_nodes(number)

@when('I perform a swap from "{from_ccy:S}" to "{to_ccy:S}" for {value:f}')
def step_impl(context, from_ccy, to_ccy, value):
  if from_ccy != "BTC":
    to_address = btc_client.get_address()
    swap = context.swingby_node.create_swap(value, from_ccy, to_ccy, to_address)
    bnb_client.send_transaction(swap["addressIn"], symbol, value, memo=to_address)
  else:
    if not context.swingby_node:
      raise Exception("No context.swingby_node running")
    to_address = bnb_client.get_address()
    swap = context.swingby_node.create_swap(value, from_ccy, to_ccy, to_address)
    btc_client.send_transaction(swap["addressIn"], swap["calc"]["send_amount"])

@when('I perform a swap from "{from_ccy:S}" to "{to_ccy:S}" for {value:f} on testnet')
def step_impl(context, from_ccy, to_ccy, value):
  if from_ccy.upper() != "BTC":
    to_address = btc_client.get_address()
    bnb_client.send_transaction("tbnb1u45hynte8t7tfmvsxd0x46x92tkucugnk4y7hv", from_ccy, value, memo=to_address)
  else:
    to_address = bnb_client.get_address()
    swap = testnet_node.create_swap(value, from_ccy, to_ccy, to_address)
    btc_client.send_transaction(swap["addressIn"], swap["calc"]["send_amount"])

@when('I perform a swap from "{from_ccy:S}" to "{to_ccy:S}" for a random small amount on testnet')
def step_impl(context, from_ccy, to_ccy):
  value = round(random.uniform(0.05, 0.5), 8)
  if from_ccy.upper() != "BTC":
    to_address = btc_client.get_address()
    bnb_client.send_transaction("tbnb1u45hynte8t7tfmvsxd0x46x92tkucugnk4y7hv", from_ccy, value, memo=to_address)
  else:
    to_address = bnb_client.get_address()
    swap = testnet_node.create_swap(value, from_ccy, to_ccy, to_address)
    btc_client.send_transaction(swap["addressIn"], swap["calc"]["send_amount"])

@given('a local Swingby node is running')
def step_impl(context):
  global conext_node
  if len(running_nodes) == 0:
    conext_node = start_swingby_node()
  else:
    conext_node = running_nodes[0]

@then('the testnet network has more than {count:d} nodes')
def step_impl(context, count):
  def check_peers():
    peers = testnet_node.fetch_peers()
    print ("Got peer count", len(peers))
    return len(peers) > count
  label = "Waiting for {} > peers.count".format(count)
  if not utils.wait_until(check_peers, timeout=60, period=1, label=label):
    raise Exception("Expecting {} > peers.count".format(count))

@then('the testnet network has less than {count:d} nodes')
def step_impl(context, count):
  def check_peers():
    peers = testnet_node.fetch_peers()
    print ("Got peer count", len(peers))
    return len(peers) < count
  label = "Waiting for {} < peers.count".format(count)
  if not utils.wait_until(check_peers, timeout=60, period=1, label=label):
    raise Exception("Expecting {} < peers.count".format(count))

@then('I stop all running Swingby nodes')
def step_impl(context):
  stop_all_swingby_nodes()

@given('I request the Swingby node status for the instances')
def step_impl(context):
  context.table_node_statuses = {}
  for row in context.table:
    moniker = row["Moniker"]
    host = row["Host"]
    port = row["ApiPort"]
    # start a client connected to the given node
    sn = SwingbyNode("", "", "", host="https://{}".format(host), flags="--rest.port={}".format(port))
    # request status
    print ("GET status for node {} ({}:{})".format(moniker, host, port))
    try:
      status = sn.fetch_status()
      if not status:
        print ("Node status {} ({}:{}) was None".format(moniker, host, port))
    except Exception as e:
      print ("Node status {} ({}:{}) had error: {}".format(moniker, host, port, e))
      status = None # will fail in assertion
    context.table_node_statuses[moniker] = status

@then('all the Swingby nodes return a valid status with the version "{version}"')
def step_impl(context, version):
  statuses = context.table_node_statuses
  if not statuses:
    raise Exception("Expected context to have table_node_statuses")
  errors = []
  for moniker in statuses.keys():
    status = statuses[moniker]
    if not status:
      errors += ["FAILED_GET_STATUS: " + moniker]
      continue
    if version != status["nodeInfo"]["version"]:
      errors += ["VERSION_MISMATCH: {} != {} {}".format(version, status["version"], moniker)]
      continue
  if len(errors) > 0:
    raise Exception(", ".join(errors))


use_step_matcher("re")
###### regex matchin below this

@when('I start a new local Swingby node instance with the flags "(?P<flags>.*)"')
def step_impl(context, flags):
  node = start_swingby_node(flags)
  context.swingby_node = node
  if hasattr(context, 'swingby_nodes'):
    context.swingby_nodes += [node]
  else:
    context.swingby_nodes = [node]
