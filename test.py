from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Bot


import pprint


TLG_TOKEN = "1862241474:AAHk9KQZazCG_iWAcW_H2yt6L_4ahekUYs4"


def start(update, context):
    update.message.reply_text("App is running")


def telegram_bot(token):

    # create the updater, that will automatically create also a dispatcher and a queue to
    # make them dialog
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher

    # add handlers for start and help commands
    dispatcher.add_handler(CommandHandler("start", start))


    # start your shiny new bot
    updater.start_polling()
    # run the bot until Ctrl-C
    updater.idle()


if __name__ == '__main__':
    telegram_bot(token=TLG_TOKEN)
