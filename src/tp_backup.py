#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, InlineQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultCachedPhoto, InlineQueryResultPhoto, InputTextMessageContent, InlineQueryResultArticle, ParseMode
from telegram.utils.helpers import escape_markdown
from uuid import uuid4
import logging
import threading
import urllib.parse
import re

from private.private_conf import token_id

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

log_errors = './log/errors.log'

# Create the EventHandler and pass it your bot's token.
updater = Updater(token_id)

vocabulary = ["a", "kin", "akesi",  "ala",  "alasa",    "ale", "ali", "anpa",   "ante",     "anu",  "awen",     "e", "en",  "esun",     "ijo",  "ike",  "ilo",  "insa",     "jaki",     "jan",  "jelo",     "jo",   "kala",     "kalama",   "kama",     "kasi",     "ken",  "kepeken", "kili",  "kiwen",    "ko",   "kon",  "kule",     "kulupu",   "kute",     "la",   "lape",     "laso",     "lawa",     "len",  "lete",     "li", "lili",   "linja",    "lipu",     "loje",     "lon",  "luka",     "lukin", "lupa",    "ma", "mama",   "mani",     "meli",     "mi", "mije",   "moku",     "moli",     "monsi",    "mu", "mun",    "musi",     "mute",     "nanpa",    "nasa",     "nasin",    "nena",     "ni", "nimi",   "noka",     "o", "olin",    "ona",  "open",     "pakala",   "pali",     "palisa",   "pan",  "pana",     "pi", "pilin",  "pimeja",   "pini",     "pipi",     "poka",     "poki",     "pona",     "pu", "sama",   "seli",     "selo",     "seme",     "sewi",     "sijelo",   "sike",     "sin", "sina",  "sinpin",   "sitelen", "sona",  "soweli",   "suli",     "suno",     "supa",     "suwi",     "tan",  "taso",     "tawa",     "telo",     "tenpo",    "toki",     "tomo",     "tu", "unpa",   "uta",  "utala",    "walo",     "wan",  "waso",     "wawa",     "weka",     "wile"]


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def generate_url(query):
    return "http://lp.plop.me/?m={}".format(query)
    return 'https://i.imgur.com/6xs9P9.jpg'
    pass

def inlinequery(bot, update):
    """Handle the inline query."""
    query = update.inline_query.query
    if '/' not in query:
        return

    query = re.sub(r'/.*', r'', query)
    query = re.sub(r'([a-zA-Z])([^a-zA-Z ])', r'\1 \2', query)
    query = re.sub(r'([^a-zA-Z ])([a-zA-Z])', r'\1 \2', query)

    nq = []
    i = 0
    for elem in query.split(sep=' '):
        if i >= 10:
            nq.append('\n')
            i=0
        if elem.lower() in vocabulary:
            nq.append(elem.lower())
            i += 1
        else:
            nq.append(elem)
            if len(elem) > 2:
                i+=len(elem)
            elif '\n' in elem:
                i = 0
    query = ' '.join(nq)
    query = re.sub(r'(^| )o($| )', r'\1oo\2', query)
    query = urllib.parse.quote(query)
    query = re.sub(r' +', r' ', query)
    query += '   &s=30'

    messages = bot.sendPhoto(109907133, generate_url(query), timeout=60)

    results = [InlineQueryResultCachedPhoto(
        id=uuid4(),
        photo_file_id=messages.photo[-1].file_id,
    )]
    bot.answerInlineQuery(update.inline_query.id, results=results)


def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='toki! sina ken sitelen kepeken linja pona kepeken ilo ni! sitelen ni li pini, sina sitelen e "/".\n\nHi! You can use linja pona with this bot. Use it online and append "/" to your sentence. You can use enter for the generated images.')

def main():

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(InlineQueryHandler(inlinequery))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()
