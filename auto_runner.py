"""
Integration test bot

Running this file will start a telegram bot that listens for commands
integration test related commands such as "@swinbytester_bot run -t @swaps"
"""

import logging
import time
import _thread
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from behave.__main__ import main as behave_main
import emoji

NAME = "swingbytester_bot"
CHAT_ID = -333896573 # Test chat
# CHAT_ID = -304493545 # Swingby DEV group

# Create the Updater and pass it your bot's token.
# Make sure to set use_context=True to use the new context based callbacks
# Post version 12 this will no longer be necessary
token = "1085500250:AAFYElMvsntjbYUxvH_86uIJUQCkbRIkxME"
updater = Updater(token, use_context=True)
bot = telegram.Bot(token=token)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
default_behave_params = ["--no-snippets", "--no-skipped"]
is_running_test = False

def submit_file(chat_id, filepath):
    # send file to chat
    with open(filepath, 'rb') as file:
        bot.send_document(chat_id=chat_id, document=file)

def start_swap_test_loop():
    proc_id = "swap_loop"
    log_path = "./tmp/last_{}".format(proc_id)
    while True:
        print ("SWAP tests starting...")
        res = behave_main(["./", "-t", "@spend", "--outfile", log_path] + default_behave_params)
        if res == 0:
            print ("SWAP integration tests passed")
            time.sleep(60 * 5)
            continue
        else:
            # send message to chat with logs
            bot.send_message(chat_id=CHAT_ID, text=emoji.emojize(':bangbang: Continuous test run failed for @swaps. Uploading logs...', use_aliases=True))
            submit_file(CHAT_ID, log_path)
            print ("SWAP integration tests failed")

def start_indexer_test_loop():
    proc_id = "btc_indexer_loop"
    log_path = "./tmp/last_{}".format(proc_id)
    while True:
        print ("INDEXER tests starting...")
        res = behave_main(["./", "-t", "@btc_indexer", "--outfile", log_path] + default_behave_params)
        if res == 0:
            print ("INDEXER integration tests passed")
            time.sleep(60 * 10)
            continue
        else:
            # send message to chat with logs
            bot.send_message(chat_id=CHAT_ID, text=emoji.emojize(':bangbang: Continuous test run failed for @btc_indexer. Uploading logs...', use_aliases=True))
            submit_file(CHAT_ID, log_path)
            print ("INDEXER integration tests failed")
            # wait 30 min if there is an error
            time.sleep(60 * 30)

def start_peers_test_loop():
    proc_id = "peers_loop"
    log_path = "./tmp/last_{}".format(proc_id)
    while True:
        print ("PEER tests starting...")
        res = behave_main(["./", "-t", "@peers", "--outfile", log_path] + default_behave_params)
        if res == 0:
            print ("PEER integration tests passed")
            time.sleep(60 * 10)
            continue
        else:
            # send message to chat with logs
            bot.send_message(chat_id=CHAT_ID, text=emoji.emojize(':bangbang: Continuous test run failed for @peers. Uploading logs...', use_aliases=True))
            submit_file(CHAT_ID, log_path)
            print ("PEER integration tests failed")
             # wait 30 min if there is an error
            time.sleep(60 * 30)

if __name__ == '__main__':
  # start background tester processes
  # spawn run in a new thread
  try:
      _thread.start_new_thread(start_swap_test_loop, ())
      _thread.start_new_thread(start_indexer_test_loop, ())
      start_peers_test_loop()
  except Exception as e:
      print("Fatal error when starting new thread")
      print(e)
