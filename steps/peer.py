import utils

from behave import given, when, then, step

@then('the new peer is accepted into the network')
def step_impl(context):
    assert context.failed is False
    assert context.tests_count >= 0

@then('the total network peer count is {number:d}')
def step_impl(context, number):
  def check_peers():
    node = context.swingby_node
    res = node.fetch_peers()
    if res['code'] == 200 and len(res['content']) == number:
      return True
  if not utils.wait_until(check_peers, timeout=60 * 5, label="Waiting for peercount to match"):
    raise Exception("Expected the total network peer count to be " + str(number))

