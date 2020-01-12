#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, InlineQueryHandler
from telegram import InlineQueryResultCachedPhoto
from uuid import uuid4
import logging
import urllib.parse
import re

from private.private_conf import token_id, magic_chat_id

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

log_errors = './log/errors.log'

# Create the EventHandler and pass it your bot's token.
updater = Updater(token_id)

vocabulary = ["a", "kin", "akesi", "ala", "alasa", "ale", "ali", "anpa", "ante", "anu", "awen", "e", "en", "esun", "ijo", "ike", "ilo", "insa", "jaki", "jan", "jelo", "jo", "kala", "kalama", "kama", "kasi", "ken", "kepeken", "kili", "kiwen", "ko", "kon", "kule", "kulupu", "kute", "la", "lape", "laso", "lawa", "len", "lete", "li", "lili", "linja", "lipu", "loje", "lon", "luka", "lukin", "lupa", "ma", "mama", "mani", "meli", "mi", "mije", "moku", "moli", "monsi", "mu", "mun", "musi", "mute", "nanpa", "nasa", "nasin", "nena", "ni", "nimi", "noka", "o", "olin", "ona", "open", "pakala", "pali", "palisa", "pan", "pana", "pi", "pilin", "pimeja", "pini", "pipi", "poka", "poki", "pona", "pu", "sama", "seli", "selo", "seme", "sewi", "sijelo", "sike", "sin", "sina", "sinpin", "sitelen", "sona", "soweli", "suli", "suno", "supa", "suwi", "tan", "taso", "tawa", "telo", "tenpo", "toki", "tomo", "tu", "unpa", "uta", "utala", "walo", "wan", "waso", "wawa", "weka", "wile"]


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def generate_url(query):
    query = re.sub(r'/(\d*).*', r'/\1', query)
    query, arg = query.split('/',1)

    if arg:
        arg = int(arg)
        if not(1 <= arg <= 10):
            arg = ''

    query = re.sub(r'([a-zA-Z])([^a-zA-Z ])', r'\1 \2', query)
    query = re.sub(r'([^a-zA-Z ])([a-zA-Z])', r'\1 \2', query)

    # Heuristic to split lines, each line consists of 10 toki pona symbols or characters of words that are not in the vocabulary.
    # This does not work well words outside of toki pona that have more that 10 characters
    # After any modification, test this sentence: mi wile pali e nasin ni kepeken ilo Telegram.\n linja ni li wile jo e nimi luka luka a
    #
    # It also makes vocabulary words lowercase
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
            if '\n' in elem:
                i = 0
                nq.append(elem)
            elif i+len(elem) > 10:
                nq.append('\n')
                nq.append(elem)
                i=0
            else:
                nq.append(elem)
                i+= len(elem)
    query = ' '.join(nq)

    # oo is o in the website, so we change a single o by oo
    query = re.sub(r'(^| )o($| )', r'\1oo\2', query)
    # escape
    query = urllib.parse.quote(query)
    query = re.sub(r' +', r' ', query)
    query += '   &s=30'
    if arg:
        query += '&f={}'.format(arg)
    return "http://lp.plop.me/?m={}".format(query)


def inlinequery(bot, update):
    """Handle the inline query."""
    query = update.inline_query.query
    if '/' not in query:
        return

    messages = bot.sendPhoto(magic_chat_id, generate_url(query), timeout=60)
    results = [InlineQueryResultCachedPhoto(
        id=uuid4(),
        photo_file_id=messages.photo[-1].file_id,
    )]
    bot.answerInlineQuery(update.inline_query.id, results=results)


def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='toki! sina ken sitelen kepeken linja pona kepeken ilo ni! sitelen ni li pini, sina sitelen e "/".\n\nHi! You can use linja pona with this bot. Use it online and append "/" to your sentence. You can use enter for the generated images.')


def help(bot, update):
    bot.sendMessage(update.message.chat_id, text='tenpo kama lili la ni li kama.\n\nComing soon!')


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