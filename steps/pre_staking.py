import utils

from behave import given, when, then, step
from swingby import StakesHttpClient

pre_staking_sdk = StakesHttpClient("https://staking-api.swingby.network")

@when('I request the current weeks pre-staking rewards for the address "{address}"')
def step_get_rewards_history(context, address):
    context.response = pre_staking_sdk.get_rewards_history(address)

@when('I request the current weeks pre-staking memo')
def step_get_weekly_memo(context):
    context.response = pre_staking_sdk.get_weekly_memo()
    context.memo = context.response

@when('I request the current weeks pre-staking payout')
def step_get_payout(context):
    context.response = pre_staking_sdk.get_payout()

@when('I request the current weeks pre-staking leaderboard')
def step_get_leaderboard(context):
    context.response = pre_staking_sdk.get_leaderboard()

@when('I request the network floats')
def step_get_floats(context):
    context.response = pre_staking_sdk.get_floats()

@when('I request the network platform status')
def step_get_platform_status(context):
    context.response = pre_staking_sdk.get_platform_status()

@when('I request the Swingby asset info')
def step_get_token_info(context):
    context.response = pre_staking_sdk.get_token_info()

@when('I request the current weeks pre-staking stakes for the address "{address}"')
def step_get_stakes(context, address):
    context.response = pre_staking_sdk.get_stakes(address)

@when('I request the current weeks pre-staking holders')
def step_get_holders(context):
    context.response = pre_staking_sdk.get_holders()
