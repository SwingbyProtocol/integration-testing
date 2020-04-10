import utils

from behave import given, when, then, step
from models import BnbClient
from models import BtcClient
from models import testnet_node

btc_client = BtcClient()
bnb_client = BnbClient()

def get_balance(symbol):
  balance = 0
  if symbol.upper() == "BTC":
    balance = float(btc_client.get_balance())
  else:
    balance = float(bnb_client.get_balance(symbol))
  print ("Current", symbol, "balance is", balance)
  return balance

@given('each of my wallets has more than {value:f} coins')
def step_impl(context, value):
  btc_balance = btc_client.get_balance()
  bnb_account = bnb_client.get_account()
  print ("Expecting BTC {} > {}".format(btc_balance, value))
  assert btc_balance > value
  balances = bnb_client.get_account()['balances']
  for b in balances:
    if b['symbol'] in [ "BTC.B-918", "BNB" ]:
      print ("Expecting {} {} > {}".format(b['symbol'], b['free'], value))
      assert float(b['free']) > value

@given('each of the node TSS wallets has more than {value:f} coins')
def step_impl(context, value):
  bnb_addr = "tbnb1caxyefalyyv3ckyx9e5dgcrpwvuk3lepwvn7nu"
  btc_addr = "mygkAc6bzpeVc6Upzq1JQMUDxFuPEt2ThL"
  btc_balance = btc_client.get_address_balance(btc_addr)
  print ("Expecting BTC {} > {}".format(btc_balance, value))
  assert btc_balance > value
  balances = bnb_client.get_address_account(bnb_addr)['balances']
  for b in balances:
    if b['symbol'] in [ "BTC.B-918", "BNB" ]:
      print ("Expecting {} {} > {}".format(b['symbol'], b['free'], value))
      assert float(b['free']) > value

@step('I wait for my "{symbol}" balance to change')
def step_impl(context, symbol):
  timeout = 60 * 90 # 1hr 30mins
  if not context.last_balance:
    raise Exception("No balance recorded in context.last_balance")
  old_balance = context.last_balance
  def check_balance():
    new_bal = get_balance(symbol)
    if new_bal != old_balance:
      # stop waiting
      return True
  label = "Waiting for {} balance to change".format(symbol)
  if not utils.wait_until(check_balance, timeout=timeout, period=30, label=label):
    raise Exception("Waiting 30 mins for {} balance to change and it did not".format(symbol))

@step('my "{symbol}" balance is more than {value:f}')
def step_impl(context, symbol, value):
  balance = get_balance(symbol)
  context.last_balance = balance
  print ("Expecting {} > {}".format(balance, value))
  assert balance > value

@step('my "{symbol}" balance is less than {value:f}')
def step_impl(context, symbol, value):
  balance = get_balance(symbol)
  context.last_balance = balance
  print ("Expecting {} < {}".format(balance, value))
  assert balance < value

@then('my "{symbol}" balance has increased by {value:f}')
def step_impl(context, symbol, value):
  balance = get_balance(symbol)
  if not context.last_balance:
    raise Exception("No last_balance recorder, please save to context.last_balance")
  difference = balance - context.last_balance
  print ("Expecting {} == {}".format(difference, value))
  assert difference == value

@then('my "{symbol}" balance has decreased by {value:f}')
def step_impl(context, symbol, value):
  balance = get_balance(symbol)
  if not context.last_balance:
    raise Exception("No last_balance recorder, please save to context.last_balance")
  difference = context.last_balance - balance
  print ("Expecting {} == {}".format(difference, value))
  assert difference == value

@then('my "{symbol}" balance has decreased by at least {value:f}')
def step_impl(context, symbol, value):
  balance = get_balance(symbol)
  if not context.last_balance:
    raise Exception("No last_balance recorder, please save to context.last_balance")
  difference = context.last_balance - balance
  print ("Expecting {} > {}".format(difference, value))
  assert difference > value


@then('my "{symbol}" balance has increased by at least {value:f}')
def step_impl(context, symbol, value):
  balance = get_balance(symbol)
  if not context.last_balance:
    raise Exception("No last_balance recorder, please save to context.last_balance")
  difference = balance - context.last_balance
  print ("Expecting {} > {}".format(difference, value))
  assert difference > value

@step('I check my "{symbol}" balance')
def step_impl(context, symbol):
  balance = get_balance(symbol)
  context.last_balance = balance

@when('I send {value:f} "{symbol}" to the address "{address}"')
def step_impl(context, value, symbol, address):
  if symbol.upper() == "BTC":
    btc_client.send_transaction(address, value)
  else:
    bnb_client.send_transaction(address, symbol, value)

@when('I send {value:f} "{symbol}" to the address "{address}" with the memo "{memo}"')
def step_send_with_memo(context, value, symbol, address, memo):
  if symbol.upper() == "BTC":
    raise Exception("BTC does not support memo transactions")
  else:
    bnb_client.send_transaction(address, symbol, value, memo=memo)

@when('I send {value:f} "{symbol}" to the address "{address}" with that memo')
def step_send_with_context_memo(context, value, symbol, address):
  step_send_with_memo(context, value, symbol, address, context.memo)

@when('I send {value:f} "{symbol}" to the nodes TSS address')
def step_impl(context, value, symbol):
  node = testnet_node
  address = node.get_tss_address(symbol)
  if symbol.upper() == "BTC":
    btc_client.send_transaction(address, value)
  else:
    bnb_client.send_transaction(address, symbol, value)

@when('I send {value:f} "{symbol}" to the nodes TSS address with the memo "{memo}"')
def step_send_tss_with_memo(context, value, symbol, memo):
  node = testnet_node
  address = node.get_tss_address(symbol)
  if symbol.upper() == "BTC":
    raise Exception("BTC does not support memo transactions")
  else:
    bnb_client.send_transaction(address, symbol, value, memo=memo)

@when('I send {value:f} "{symbol}" to the nodes TSS address with the TSS address as the memo')
def step_impl(context, value, symbol, memo):
  if not context.swingby_node:
    raise Exception("No swingby node bound to context.swingby_node")
  node = context.swingby_node
  address = node.get_tss_address(symbol)
  if symbol.upper() == "BTC":
    raise Exception("BTC does not support memo transactions")
  else:
    bnb_client.send_transaction(address, symbol, value, memo=address)

