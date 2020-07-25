"""
Integration test bot

Running this file will start a telegram bot that listens for commands
integration test related commands such as "@swinbytester_bot run -t @swaps"
"""

import logging
import os
import time
import _thread
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from behave.__main__ import main as behave_main
import emoji
from .models import btc_address
from .models import bnb_address

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

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('''
start <flags> - Start a new test run
logs          - Get the logs from the last test run
wallets       - Get the wallet used for testing

Tags:
@btc_indexer       - All indexer tests
@local             - All tests that use a local swingby net
@testnet           - All tests that use the test network
@swaps             - All swap tests
@peers             - All peers tests
@sub_hour          - Tests that take just under an hour
@sub_minute        - Tests that take just under a minute


Example:
@{0} start -t "not @sub_hour or @local"
    '''.format(NAME))

def handle_run(update, context):
    global is_running_test
    # check if we are already running a test
    if is_running_test:
        update.message.reply_text(emoji.emojize(':stopwatch: Still running tests - please wait', use_aliases=True))
        return
    # parse the text into a set of command args
    cmd = update.message.text.replace('@{} run '.format(NAME), '')
    behave_args = ["./"] + default_behave_params + cmd.split(' ') + ["--outfile", "./tmp/last_run.txt"]
    # spawn run in a new thread
    try:
        _thread.start_new_thread(run_behave, (update, context, behave_args))
    except:
        update.message.reply_text("Fatal error when starting new thread")

def handle_log(update, context):
    # load last run output
    submit_file(update.message.chat_id, './tmp/last_run.txt')

def submit_file(chat_id, filepath):
    # send file to chat
    with open(filepath, 'rb') as file:
        bot.send_document(chat_id=chat_id, document=file)

def run_behave(update, context, args):
    global is_running_test
    update.message.reply_text(emoji.emojize(':man_running: Starting test run - this might take a while', use_aliases=True))
    before = time.time()
    is_running_test = True
    # start tests
    res = behave_main(args)
    print (res)
    is_running_test = False
    execution_time = int(time.time() - before)
    result = int(res)
    if res > 0:
        update.message.reply_text(emoji.emojize(':bangbang: Integration tests failed ({}s)'.format(execution_time), use_aliases=True))
    else:
        update.message.reply_text(emoji.emojize(':white_check_mark: Integration tests passed ({}s)'.format(execution_time), use_aliases=True))

def handle_Wallets(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('''
This client's wallet:
BNB: {}
BTC: {}

All test client wallets:
BNB: tbnb1dedxffvl324ggfdpxl0gw5hwylc848ztuy7g7c
BTC: n37eRzDmZhDcLxRixwEvmemeWBHUUoRSRM
BNB: tbnb1hzmm62lape793rju0dek5ecr83qlh6q608uuzn
BTC: mwHvpLswinucSRUHKZeoi2pLuGKjv6EWS8
BNB: tbnb1yj5pv0plj6qkuwx6ejgk4z3ux2eytuaz3xl7c7
BTC: mjZ7Qbo3s6H1jvu3yo6Y75HK3DawzbPhAv
BNB: tbnb1d5cmd25sjff858d70r0vy7g7mrumrpf9c494tt
BTC: mvhBkh9QiVwCW5eK3MBB8AyBZcMfRTcmwa

Testnet TSS wallets:
BNB: tbnb1ws2z8n9ygrnaeqwng69cxfpnundneyjze9cjsy
BTC: mr6ioeUxNMoavbr2VjaSbPAovzzgDT7Su9

Test local TSS wallets:
BNB: tbnb1f54dc6vpvc5wmqxyqzjh6d44qmfuy4edaaqjz5
BTC: mnYyfrjv7rmddqGYLr7nVDvKaWSpV2LsnX
    '''.format(bnb_address, btc_address))


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def start_bot():
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.regex('@{} run .*'.format(NAME)), handle_run))
    dp.add_handler(MessageHandler(Filters.regex('@{} wallets'.format(NAME)), handle_Wallets))
    dp.add_handler(MessageHandler(Filters.regex('@{} help'.format(NAME)), help))
    dp.add_handler(MessageHandler(Filters.regex('@{} log'.format(NAME)), handle_log))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    # start bot
    start_bot()
