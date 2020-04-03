#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, InlineQueryHandler, ChosenInlineResultHandler, CallbackQueryHandler
from telegram import InlineQueryResultCachedPhoto, InlineQueryResultCachedSticker
from uuid import uuid4
import logging
import urllib.parse
import re

from private.private_conf import token_id, magic_chat_id, id_photo_help

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

log_errors = './log/errors.log'

# Create the EventHandler and pass it your bot's token.
updater = Updater(token_id)

# Extended vocabulary
vocabulary = ["a", "akesi", "alasa", "anpa", "ante", "awen", "ala", "ali", "ale", "anu", "e", "en", "esun", "insa", "ijo", "ike", "ilo", "jaki", "jelo", "jan", "jo", "kalama", "kulupu", "kiwen", "kala", "kama", "kasi", "ken", "kepeken", "kili", "kule", "kute", "kon", "ko", "linja", "lukin", "lape", "laso", "lawa", "lete", "lili", "lipu", "loje", "luka", "lupa", "len", "lon", "la", "li", "monsi", "mama", "mani", "meli", "mije", "moku", "moli", "musi", "mute", "mun", "ma", "mi", "mu", "nanpa", "nasin", "nasa", "nena", "nimi", "noka", "ni", "oo", "olin", "open", "ona", "pakala", "palisa", "pimeja", "pilin", "pali", "pana", "pini", "pipi", "poka", "poki", "pona", "pan", "pi", "pu", "sitelen", "sijelo", "sinpin", "soweli", "sama", "seli", "selo", "seme", "sewi", "sike", "sina", "sona", "suli", "suno", "supa", "suwi", "sin", "tenpo", "taso", "tawa", "telo", "toki", "tomo", "tan", "tu", "utala", "unpa", "uta", "walo", "waso", "wawa", "weka", "wile", "wan", "zz", "_65535", "spacespace", "commaspace", "periodspace", "colonspace", "exclamspace", "questionspace", "kin", "kinexclam", "kipisi", "leko", "monsuta", "namako", "oko", "pake", "anpalawa", "ijoike", "ijolili", "ijopona", "ijouta", "ilokipisi", "ilolape", "ilomusi", "ilonanpa", "iloopen", "ilosuno", "ilotoki", "ilolukin", "ilomoli", "ilooko", "janala", "janalasa", "janali", "janale", "janike", "jankala", "jankasi", "jankalama", "jankulupu", "janlawa", "janlili", "janmute", "jannasa", "janolin", "janpakala", "janpali", "janpoka", "janpona", "jansama", "janseme", "jansewi", "jansin", "jansona", "jansuli", "jansuwi", "jantoki", "janunpa", "janutala", "janwawa", "janante", "kalalili", "kalalete", "kalamamusi", "kasilili", "kilijelo", "kililaso", "kililili", "kililoje", "kilipalisa", "kilisuwi", "kilipimeja", "kiliwalo", "kokasi", "kokule", "kojaki", "kolete", "kolili", "koseli", "konasa", "kowalo", "kojelo", "kolaso", "koloje", "kopimeja", "konlete", "lenjelo", "lenlaso", "lenloje", "lenjan", "lenlawa", "lenluka", "lennoka", "lenpimeja", "lensin", "lenwalo", "linjalili", "linjapona", "lipukasi", "liputoki", "lipusona", "lipunanpa", "lipusewi", "lukaluka", "lupakiwen", "lupajaki", "lupakute", "lupameli", "lupamonsi", "lupanena", "lupalili", "lupatomo", "mamamama", "mamameli", "mamamije", "meliike", "melipona", "melilili", "melisama", "meliunpa", "mijeike", "mijepona", "mijelili", "mijesama", "mijeunpa", "mijewawa", "musilili", "nenakon", "nenakute", "nenalili", "nenamama", "nenameli", "palisalili", "pilinala", "pilinike", "pilinnasa", "pilinpakala", "pilinpona", "pilinsama", "pokikon", "pokilete", "pokiseli", "pokitelo", "pokilili", "pokilen", "sikelili", "sitelentawa", "sonaala", "sonalili", "sonaike", "sonama", "sonananpa", "sonapona", "sonasijelo", "sonatenpo", "sonatoki", "sonautala", "selolen", "selosoweli", "supalape", "supalawa", "supamoku", "supamonsi", "supapali", "supalupa", "telolete", "telolili", "tokiala", "tokiike", "tokipona", "tokisona", "tokiutala", "tokisin", "tomolape", "tomomani", "tomomoku", "tomonasin", "tomopali", "tomosona", "tomotawa", "tomounpa", "tomoutala", "tutu", "tuwan", "wantu", "ijomonsuta", "janmonsuta", "tomomonsuta", "sitelenmonsuta", "sitelenike", "sitelenpona", "sitelenma", "sitelensitelen", "sitelentoki", "maali", "maale", "makasi", "matomo", "kiwenjelo", "kiwenlaso", "kiwenlili", "kiwenloje", "kiwenmun", "kiwenpimeja", "kiwensuno", "kiwenwalo", "kiwenkasi", "kiwenlete", "kiwenseli", "ikeala", "ikelili", "ikelukin", "ponaala", "ponalili", "ponalukin", "lenlili", "ijoakesi", "ijoala", "ijoalasa", "ijoali", "ijoale", "ijoanpa", "ijoante", "ijoanu", "ijoawen", "ijoen", "ijoesun", "ijoilo", "ijoinsa", "ijojaki", "ijojan", "ijojelo", "ijojo", "ijokala", "ijokalama", "ijokama", "ijokasi", "ijoken", "ijokepeken", "ijokili", "ijokiwen", "ijoko", "ijokon", "ijokule", "ijokulupu", "ijokute", "ijolape", "ijolaso", "ijolawa", "ijolen", "ijolete", "ijolinja", "ijolipu", "ijoloje", "ijolon", "ijoluka", "ijolukin", "ijolupa", "ijoma", "ijomama", "ijomani", "ijomeli", "ijomi", "ijomije", "ijomoku", "ijomoli", "ijomonsi", "ijomu", "ijomun", "ijomusi", "ijomute", "ijonanpa", "ijonasa", "ijonasin", "ijonena", "ijoni", "ijonimi", "ijonoka", "ijoolin", "ijoona", "ijoopen", "ijopakala", "ijopali", "ijopalisa", "ijopan", "ijopana", "ijopilin", "ijopimeja", "ijopini", "ijopipi", "ijopoka", "ijopoki", "ijopu", "ijosama", "ijoseli", "ijoselo", "ijoseme", "ijosewi", "ijosijelo", "ijosike", "ijosin", "ijosina", "ijosinpin", "ijositelen", "ijosona", "ijosoweli", "ijosuli", "ijosuno", "ijosupa", "ijosuwi", "ijotan", "ijotaso", "ijotawa", "ijotelo", "ijotenpo", "ijotoki", "ijotomo", "ijotu", "ijounpa", "ijoutala", "ijowalo", "ijowan", "ijowaso", "ijowawa", "ijoweka", "ijowile", "ijokin", "ijokipisi", "ijoleko", "ijonamako", "ijooko", "ijopake"]


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def generate_url(query):
    #query = re.sub(r'/(\d*).*', r'/\1', query)
    query, arg = query.split('/', 1)

    query = re.sub(r'_+', r'_', query)
    query = re.sub(r'([a-zA-Z])([^a-zA-Z ])', r'\1 \2', query)
    query = re.sub(r'([^a-zA-Z ])([a-zA-Z])', r'\1 \2', query)

    # Heuristic to split lines, each line consists of 10 toki pona symbols or characters of words that are not in the vocabulary.
    # This does not work well words outside of toki pona that have more that 10 characters
    # After any modification, test this sentence: mi wile pali e nasin ni kepeken ilo Telegram.\n linja ni li wile jo e nimi luka luka a
    #
    # It also makes vocabulary words lowercase
    nq = []
    i = 0
    split_q = query.split(sep=' ')
    for idx, elem in enumerate(split_q):
        if i >= 10:
            nq.append('\n')
            i=0
        if elem.lower() in vocabulary:
            nq.append(elem.lower())
            i += 1
        else:
            if elem == '_' and len(split_q) > idx+1 and split_q[idx+1] in vocabulary:
                nq.append(elem)
            elif '\n' in elem:
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
    query = re.sub(r' +', r' ', query)
    query += ' '*(9-i)
    query = urllib.parse.quote(query)
    query += '    &s=30&t=webp'

    return "http://lp.plop.me/?m={}".format(query)


def inlinequery(bot, update):
    """Handle the inline query."""
    query = update.inline_query.query
    if '/' not in query:
        return

    message = bot.sendSticker(magic_chat_id, generate_url(query), timeout=60)
    results = [InlineQueryResultCachedSticker(
        id=uuid4(),
        sticker_file_id=message.sticker.file_id,
    )]

    bot.answerInlineQuery(update.inline_query.id, results=results)

    bot.delete_message(chat_id=magic_chat_id, message_id=message.message_id)


def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='toki! sina wile kama sona e ilo ni la o luka e ni: /help. sina ken sitelen kepeken linja pona kepeken ilo ni! sitelen ni li pini, sina sitelen e "/".\n\nHi! I you want to learn all you can do with the bot, click here: /help. You can use linja pona with this bot. Use it online and append "/" to your sentence. You can add enters for the generated images.')


def help(bot, update):
    with open('help.txt', 'r') as f:
        text = f.read()

    url_photo_help = '''http://lp.plop.me/?m=%0D%0Ani+li+pona+mute+tawa+mi%20%0D%0A%0D%0Atoki-pona+li+pona+tawa+mi%20%0D%0A%0D%0Ama+[_%20kasi+_%20alasa+_%20nasin+_%20awen+_%20telo+_%20a%20]+li+suli%20%0D%0A%0D%0Ajan+pi+sona+ala+li+ken+kama+sona+kepeken+ni%20%20%20%20%20%20%20%20%20%20%20%20%20%0D%0A%0D%0A%0D%0A%0D%0A&s=200&f=1&t=jpg'''

    result = bot.send_photo(update.message.chat_id, photo=url_photo_help, caption=text, parse_mode='Markdown')
    print(result)

def main():
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(InlineQueryHandler(inlinequery))
    #dp.add_handler(ChosenInlineResultHandler(subtitle))

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
