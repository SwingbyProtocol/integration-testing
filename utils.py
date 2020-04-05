import time
import asyncio

def wait_until(somepredicate, timeout=10, period=0.5, label="wait_until", fail_on_error=False, *args, **kwargs):
  mustend = time.time() + timeout
  start = time.time()
  now = time.time()
  count = 0
  while time.time() < mustend:
    try:
      if somepredicate(*args, **kwargs):
        return True
    except Exception as e:
      print (e)
      if fail_on_error:
        return False
    if time.time() >= mustend:
      return False
    time.sleep(period)
    count += 1
    delta = int(time.time() - start)
    print (label + "- waited for {}s and still waiting".format(delta))
    count = 0
  return False

async def async_wait_until(somepredicate, timeout=10, period=0.5, label="wait_until", fail_on_error=False, *args, **kwargs):
  mustend = time.time() + timeout
  start = time.time()
  now = time.time()
  count = 0
  while time.time() < mustend:
    try:
      res = await somepredicate(*args, **kwargs)
      if res == True:
        return True
    except Exception as e:
      print (e)
      if fail_on_error:
        return False
    if time.time() >= mustend:
      return False
    await asyncio.sleep(period)
    count += 1
    delta = int(time.time() - start)
    print (label + "- waited for {}s and still waiting".format(delta))
    count = 0
  return False
