#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, InlineQueryHandler, ChosenInlineResultHandler, CallbackQueryHandler
from telegram import InlineQueryResultCachedPhoto, InlineQueryResultCachedSticker, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from uuid import uuid4
import logging
import urllib.parse
import re

from private.private_conf import token_id, magic_chat_id, id_photo_nasin_sitelen, id_photo_kule, id_photo_help

from database import TokiPonaDB
from enums import Colors, Selectable, Fonts, fonts_dict, colors_dict


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


def prepend_underscores_in_names(query):
    split_q = query.split(sep=' ')
    result = []
    name_enabled = False
    for elem in split_q:
        aux = re.search(r'\[[^\]]*$', elem)
        if aux:
            name_enabled = True
        else:
            aux = re.search(r'\].*$', elem)
            if aux:
                name_enabled = False
            elif name_enabled and elem in vocabulary:
                result.append('_')
        result.append(elem)

    return ' '.join(result)


def generate_url(query, id_chat, image_format='webp', size=30):
    db = TokiPonaDB()
    try:
        font_type, font_color, background_color = db.get_data(id_chat)
    except TypeError: # User non existent
        db.insert_new_user(id_chat)
        font_type, font_color, background_color = db.get_data(id_chat)

    #query = re.sub(r'/(\d*).*', r'/\1', query)
    query, arg = query.split('/', 1)

    query = re.sub(r'_+', r'_', query)
    query = re.sub(r'([a-zA-Z])([^a-zA-Z ])', r'\1 \2', query)
    query = re.sub(r'([^a-zA-Z ])([a-zA-Z])', r'\1 \2', query)

    if int(font_type) == 1:
        query = re.sub(r'_', r'', query)
        query = prepend_underscores_in_names(query)


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
    if i in [1,2]:
        size = 60
    elif i in [3, 4]:
        size = 50



    font_color = str(font_color)
    if len(font_color) != 6:
        font_color = '0'*(6-len(font_color)) + str(font_color)

    background_color = str(background_color)
    if len(background_color) != 6:
        background_color = '0'*(6-len(background_color)) + str(background_color)

    if int(font_type) == 1:
        # oo is o in the website, so we change a single o by oo
        query = re.sub(r'(^| )o($| )', r'\1oo\2', query)
        query = re.sub(r'(^| )O($| )', r'\1oo\2', query)

    # escape
    query = re.sub(r' +', r' ', query)
    query += ' '*(9-i)
    query = urllib.parse.quote(query)

    query += '    &s={}&f={}&c={}&b={}&t={}'.format(size, font_type, font_color, background_color, image_format)

    return "http://lp.plop.me/?m={}".format(query)


def inlinequery(bot, update):
    """Handle the inline query."""
    query = update.inline_query.query
    if '/' not in query:
        return

    id_chat = update.effective_user.id
    message = bot.sendSticker(magic_chat_id, generate_url(query, id_chat), timeout=60)
    results = [InlineQueryResultCachedSticker(
        id=uuid4(),
        sticker_file_id=message.sticker.file_id,
    )]

    bot.answerInlineQuery(update.inline_query.id, results=results)

    bot.delete_message(chat_id=magic_chat_id, message_id=message.message_id)


def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='toki! sina wile kama sona e ilo ni la o luka e ni: /help. sina ken sitelen kepeken linja pona kepeken ilo ni! sitelen ni li pini, sina sitelen e "/".\n\nHi! I you want to learn all you can do with the bot, click here: /help. You can use linja pona with this bot. Use it online and append "/" to your sentence. You can add line breaks.')


def settings(bot, update, edit_message_or_not=False, extra_text=''):
    # This is only allowed in private chats
    if not edit_message_or_not and update.message.chat_id != update.message.from_user.id:
        bot.sendMessage(update.message.chat_id,
                parse_mode='Markdown',
                text='o toki tawa mi lon [tomo mi](t.me/tokipona_bot) a! (Talk to me in [my private chat](t.me/tokipona_bot)).')
        return

    keyboard = [[InlineKeyboardButton("nasin sitelen - Font Type", callback_data=str(Selectable.change_font_type.value))],
                [InlineKeyboardButton("kule sitelen - Font Color", callback_data=str(Selectable.change_font_color.value))],
                [InlineKeyboardButton("kule lipu - Background Color", callback_data=str(Selectable.change_background_color.value))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = '{}sina wile ala wile ante e nasin sitelen e kule sitelen tawa sitelen sina pi toki pona?\n\nDo you want to change the font type or the color of your Toki Pona messages?'.format(extra_text)

    photo_query = 'ni li wile sina a /'
    if edit_message_or_not:
        query = update.callback_query
        bot.edit_message_media(chat_id=query.message.chat_id,
                               message_id=query.message.message_id,
                               media=InputMediaPhoto(generate_url(query=photo_query, id_chat=query.message.chat_id, image_format='jpg', size=50), caption=text),
                               reply_markup=reply_markup,
                               )
    else:
        results = bot.send_photo(update.message.chat_id, photo=generate_url(query=photo_query, id_chat=update.message.chat_id, image_format='jpg', size=50), caption=text, parse_mode='Markdown', reply_markup=reply_markup, timeout=60)


def buttons(bot, update):
    query = update.callback_query
    data = query.data.split('|')
    if len(data) == 1:
        if data[0] == Selectable.change_font_type.value:
            fonts_available = [Fonts.linja_pona_jan_same, Fonts.linja_leko_jan_selano, Fonts.sitelen_luka_tu_tu_jan_inkepa, Fonts.sitelen_pona_jan_wesi, Fonts.linja_pimeja_jan_inkepa, Fonts.sitelen_pi_linja_ko_jan_inkepa,Fonts.sitelen_pona_pona_jan_jaku, Fonts.insa_pi_supa_lape_int_main]
            keyboard = []
            for font in fonts_available:
                keyboard.append([InlineKeyboardButton(fonts_dict[font.value], callback_data="{}|{}".format(Selectable.change_font_type.value, font.value))])
            keyboard.append([InlineKeyboardButton('o tawa monsi - Go back', callback_data="{}".format(Selectable.go_back.value))])

            reply_markup = InlineKeyboardMarkup(keyboard)
            db = TokiPonaDB()
            font_type, _, _ = db.get_data(query.message.chat_id)
            font_type = str(font_type)

            text = '''o luka e nasin. tenpo ni la sina kepeken {}\n\nPick a font. Current is {}.'''.format(fonts_dict[font_type], fonts_dict[font_type])
            bot.edit_message_media(chat_id=query.message.chat_id,
                                   message_id=query.message.message_id,
                                   media=InputMediaPhoto(id_photo_nasin_sitelen, caption=text),
                                   reply_markup=reply_markup,
                                   )
        elif data[0] == Selectable.change_font_color.value:
            colors_available = [Colors.pimeja, Colors.jelo, Colors.loje, Colors.loje_walo, Colors.laso_kasi, Colors.laso_kasi_walo, Colors.laso_sewi, Colors.laso_sewi_walo, Colors.pimeja_walo_walo, Colors.pimeja_walo, Colors.pimeja_pimeja_walo, Colors.pimeja_pimeja_pimeja_walo, Colors.walo, ]
            keyboard = []
            for color in colors_available:
                keyboard.append([InlineKeyboardButton(colors_dict[color.value], callback_data="{}|{}".format(Selectable.change_font_color.value, color.value))])
            keyboard.append([InlineKeyboardButton('o tawa monsi - Go back', callback_data="{}".format(Selectable.go_back.value))])

            reply_markup = InlineKeyboardMarkup(keyboard)
            db = TokiPonaDB()
            _, font_color, _ = db.get_data(query.message.chat_id)
            font_color = str(font_color)
            if len(font_color) != 6:
                font_color = '0'*(6-len(font_color)) + str(font_color)

            text = '''o luka e kule sitelen. tenpo ni la sina kepeken {}\n\nPick a color for the font. Current is {}.'''.format(colors_dict[font_color], colors_dict[font_color])
            bot.edit_message_media(chat_id=query.message.chat_id,
                                   message_id=query.message.message_id,
                                   media=InputMediaPhoto(id_photo_kule, caption=text),
                                   reply_markup=reply_markup,
                                   )
        elif data[0] == Selectable.change_background_color.value:
            colors_available = [Colors.pimeja, Colors.jelo, Colors.loje, Colors.loje_walo, Colors.laso_kasi, Colors.laso_kasi_walo, Colors.laso_sewi, Colors.laso_sewi_walo, Colors.pimeja_walo_walo, Colors.pimeja_walo, Colors.pimeja_pimeja_walo, Colors.pimeja_pimeja_pimeja_walo, Colors.walo, ]
            keyboard = []
            for color in colors_available:
                keyboard.append([InlineKeyboardButton(colors_dict[color.value], callback_data="{}|{}".format(Selectable.change_background_color.value, color.value))])
            keyboard.append([InlineKeyboardButton('o tawa monsi - Go back', callback_data="{}".format(Selectable.go_back.value))])


            reply_markup = InlineKeyboardMarkup(keyboard)
            db = TokiPonaDB()
            _, _, background_color = db.get_data(query.message.chat_id)
            background_color = str(background_color)
            if len(background_color) != 6:
                background_color = '0'*(6-len(background_color)) + str(background_color)


            text = '''o luka e kule lipu. tenpo ni la sina kepeken {}\n\nPick a color for the background. Current is {}.'''.format(colors_dict[background_color], colors_dict[background_color])
            bot.edit_message_media(chat_id=query.message.chat_id,
                                   message_id=query.message.message_id,
                                   media=InputMediaPhoto(id_photo_kule, caption=text),
                                   reply_markup=reply_markup,
                                   )
        elif data[0] == Selectable.go_back.value:
            settings(bot, update, True)
    elif len(data) == 2:
        db = TokiPonaDB()
        if data[0] == Selectable.change_font_type.value:
            db.update_font_type(query.message.chat_id, int(data[1]))
            success_message = 'tenpo ni la sina kepeken nasin sitelen pi {}\n\nYour font type is now {}\n\n'.format(fonts_dict[str(data[1])], fonts_dict[str(data[1])])
        elif data[0] == Selectable.change_font_color.value:
            db.update_font_color(query.message.chat_id, str(data[1]))
            success_message = 'tenpo ni la sina kepeken kule sitelen pi {}\n\nYour font color is now {}\n\n'.format(colors_dict[str(data[1])], colors_dict[str(data[1])])
        elif data[0] == Selectable.change_background_color.value:
            db.update_background_color(query.message.chat_id, str(data[1]))
            success_message = 'tenpo ni la sina kepeken kule lipu pi {}\n\nYour background color is now {}\n\n'.format(colors_dict[str(data[1])], colors_dict[str(data[1])])
        settings(bot, update, True, extra_text=success_message)
    else:
        raise TypeError("Button query got a number of arguments different from 1 or 2: {}".format(data))


def help_english(bot, update):
    help(bot, update, 'en')


def help_toki_pona(bot, update):
    help(bot, update, 'tp')


def help(bot, update, language):
    # This is only allowed in private chats
    if update.message.chat_id != update.message.from_user.id:
        bot.sendMessage(update.message.chat_id,
                parse_mode='Markdown',
                text='o toki tawa mi lon [tomo mi](t.me/tokipona_bot) a! (Talk to me in [my private chat](t.me/tokipona_bot)).')
        return
    if language == 'en':
        help_filename = 'help.txt'
    else:
        help_filename = 'sona.txt'

    with open(help_filename , 'r') as f:
        text = f.read()

    result = bot.send_photo(update.message.chat_id, photo=id_photo_help, caption=text, parse_mode='Markdown')


def main():
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("sona", help_toki_pona))
    dp.add_handler(CommandHandler("help", help_english))
    dp.add_handler(CommandHandler("settings", settings))
    dp.add_handler(CommandHandler("wilemi", settings))
    dp.add_handler(InlineQueryHandler(inlinequery))
    #dp.add_handler(ChosenInlineResultHandler(subtitle))

    updater.dispatcher.add_handler(CallbackQueryHandler(buttons))

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
