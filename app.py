import json
import logging
import requests
import threading
import time
import typing

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Bot

from multiprocessing import Process
from threading import Thread
from conf import TA_API_TOKEN, TLG_TOKEN, SYMBOLS, INTERVAL, INDICATORS, CHAT_ID

logger = logging.getLogger(__name__)

symbols: typing.List = SYMBOLS
indicators: typing.List = INDICATORS
interval: str = INTERVAL
ta_api_token: str = TA_API_TOKEN
tlg_token: str = TLG_TOKEN
chat_id: str = CHAT_ID

bot: Bot = Bot(token=tlg_token)

exit_event = threading.Event()


def app_binance(indicators, symbols, interval, ta_api_token, chat_id, value_indicators):
    while True:
        for symbol in symbols:
            for indicator in indicators:
                indicator_value = value_indicators(
                    indicator=indicator,
                    symbol=symbol,
                    inter=interval,
                    token=ta_api_token,
                )
                if indicator_value:
                    value = indicator_value.get("value", "No data")
                    if isinstance(value, float):
                        value = round(value)
                    expected_value = indicator_value.get("expected_value", "Set expected data")
                    if value != expected_value:
                        bot.sendMessage(
                            chat_id=chat_id,
                            text=f"{indicator}\nValue: {value}\nExpected value: {expected_value}"
                        )
                        logger.info(f"Send message: {indicator}\nValue: {value}\nExpected value: {expected_value}")
                time.sleep(16)
        if exit_event.is_set():
            logger.info("Thread is shutting down")
            break


def get_value_indicator(indicator, symbol, inter, token):
    inds = {
        "macd": {
            "url": f"https://api.taapi.io/macd?secret={token}&exchange=binance&symbol={symbol}&interval={inter}",
            "value": "valueMACD",
            "expected_value": 0,
        },
        "rsi": {
            "url": f"https://api.taapi.io/rsi?secret={token}&exchange=binance&symbol={symbol}&interval={inter}",
            "value": "value",
            "expected_value": 0,
        },
        "aroon": {
            "url": f"https://api.taapi.io/aroon?secret={token}&exchange=binance&symbol={symbol}&interval={inter}",
            "value": "value",  # TODO какоое значение valueAroonDown, valueAroonUp
            "expected_value": 0,
        },
        "stoch": {
            "url": f"https://api.taapi.io/stoch?secret={token}&exchange=binance&symbol={symbol}&interval={inter}",
            "value": "value",  # TODO какоое значение valueSlowK, valueSlowD
            "expected_value": 0,
        },
        "ultosc": {
            "url": f"https://api.taapi.io/ultosc?secret={token}&exchange=binance&symbol={symbol}&interval={inter}",
            "value": "value",
            "expected_value": 0,
        },
    }
    resource = requests.get(
        url=inds.get(indicator).get("url")
    )
    data = json.loads(resource.text)
    if data:
        return {
            "value": data.get(
                inds.get(indicator).get("value")
            ),
            "expected_value": inds.get(indicator).get("expected_value"),
        }
    return


process = Process(target=app_binance, args=(
        indicators,
        symbols,
        interval,
        ta_api_token,
        chat_id,
        get_value_indicator,
    )
                           )

thread = None


def start(update, context):
    global thread
    thread = Thread(target=app_binance, args=(
        indicators,
        symbols,
        interval,
        ta_api_token,
        chat_id,
        get_value_indicator,
    ))
    thread.start()
    exit_event.clear()
    update.message.reply_text("App is running")
    logger.info("Start app")


def stop(update, context):
    global thread
    if thread:
        exit_event.set()
        update.message.reply_text(f"App is stopped")
    else:
        update.message.reply_text(f"Nothing to stop")


# function to handle normal text
def text(update, context):
    text_received = update.message.text
    update.message.reply_text(f'Did you said "{text_received}" ?')


def telegram_bot(token):

    # create the updater, that will automatically create also a dispatcher and a queue to
    # make them dialoge
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher

    # add handlers for start and help commands
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("stop", stop))

    # add an handler for normal text (not commands)
    dispatcher.add_handler(MessageHandler(Filters.text, text))

    # start your shiny new bot
    updater.start_polling()
    # run the bot until Ctrl-C
    updater.idle()


if __name__ == '__main__':
    telegram_bot(token=TLG_TOKEN)

