"""
Integration test bot

Running this file will start a telegram bot that listens for commands
integration test related commands such as "@swinbytester_bot run -t @swaps"
"""

import logging
import time
from behave.__main__ import main as behave_main

NAME = "swingbytester_bot"

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
default_behave_params = ["--no-snippets", "--no-skipped"]

def start_volume_loop():
    proc_id = "volume_loop"
    log_path = "./tmp/last_{}".format(proc_id)
    while True:
        print ("VOLUME loop running...")
        res = behave_main(["../integration-testing", "-t", "@volume", "--outfile", log_path] + default_behave_params)
        if res == 0:
            print ("VOLUME integration tests passed")
            time.sleep(60 * 5)
            continue
        else:
            print ("VOLUME integration tests failed")
            time.sleep(60 * 5)

if __name__ == '__main__':
  # start background tester processes
  # spawn run in a new thread
  try:
      start_volume_loop()
  except Exception as e:
      print("Fatal error when starting new thread")
      print(e)
