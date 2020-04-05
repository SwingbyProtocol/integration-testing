import time
import asyncio
import re

from behave import given, when, then, step, use_step_matcher
from behave.api.async_step import async_run_until_complete

@step('I wait for {seconds:d} seconds')
@async_run_until_complete
@asyncio.coroutine
async def step_impl(context, seconds):
  for i in range(seconds):
    await asyncio.sleep(1)

@step('I wait for {mins:d} minutes')
@async_run_until_complete
@asyncio.coroutine
async def step_impl(context, mins):
  for i in range(mins60):
    await asyncio.sleep(1)

@step('I wait for {hrs:d} hours')
@async_run_until_complete
@asyncio.coroutine
async def step_impl(context, hrs):
  for i in range(hrs * 60 * 60):
    await asyncio.sleep(1)
