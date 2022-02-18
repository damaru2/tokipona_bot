#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, InlineQueryHandler, ChosenInlineResultHandler, CallbackQueryHandler
from telegram import InlineQueryResultCachedPhoto, InlineQueryResultCachedSticker, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from uuid import uuid4
import logging
import urllib.parse
import re
import os

from private.private_conf import token_id, magic_chat_id, fonts, id_photo_nasin_sitelen, id_photo_kule, id_photo_help, render_directory

from image_utils import ImageText
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

def error(update, context):
    # import traceback
    # traceback.print_exception(context.error)
    logger.warning('Update "%s" caused error "%s"' % (update, context.error))


def insert_underscores_in_name(matchobj):
    name = matchobj.group(1)
    words = name.split()
    return "[_{}]".format("_".join(words))


def hex_to_rgb(hex):
  return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))


def fix_font_quirks(query, font_type):
    if font_type == 12: # linja pi tomo lipu can't handle single letter words in some cases
        query = re.sub(r'(^|\s)o($|[^a-z])', r'\1oo\2', query)
        query = re.sub(r'(^|\s)a($|[^a-z])', r'\1aa\2', query)
        query = re.sub(r'(^|\s)e($|[^a-z])', r'\1ee\2', query)

    if font_type in [1, 15, 12, 17]: # fonts that support cartouches with underscores
        query = re.sub(r'\[(.+)\]', insert_underscores_in_name, query)

    if font_type == 4: # sitelen pona doesn't have a ligature for "ale", only "ali" *shrug*
        query = re.sub(r'([^a-zA-Z])ale([^a-zA-Z])', r'\1ali\2', query)

    return query


def generate_pic(query, id_chat, image_format='webp', size=80):
    db = TokiPonaDB()
    try:
        font_type, font_color, background_color = db.get_data(id_chat)
    except TypeError: # User non existent
        db.insert_new_user(id_chat)
        font_type, font_color, background_color = db.get_data(id_chat)

    font_color = str(font_color)
    if len(font_color) != 6:
        font_color = '0'*(6-len(font_color)) + str(font_color)

    background_color = str(background_color)
    if len(background_color) != 6:
        background_color = '0'*(6-len(background_color)) + str(background_color)

    query, arg = query.split('/', 1)
    
    query = fix_font_quirks(query, font_type)

    fg = hex_to_rgb(font_color) + (255,)
    bg = hex_to_rgb(background_color) + (255,)

    font_file = fonts.get(str(font_type), fonts['default'])
    img_width = 512
    img = ImageText(img_width, size, font_file, foreground=fg, background=bg, mode="RGB",padding = 20, padding_bottom=60)
    filename = "{}/{}.{}".format(render_directory, id_chat, image_format)
    img.render(query, filename)
    return filename


def inlinequery(update, context):
    """Handle the inline query."""
    query = update.inline_query.query
    if '/' not in query:
        return

    id_chat = update.effective_user.id
    filename = generate_pic(query, id_chat)
    message = context.bot.sendSticker(magic_chat_id, open(filename, 'rb'), timeout=60, disable_notification=True)

    results = [InlineQueryResultCachedSticker(
        id=uuid4(),
        sticker_file_id=message.sticker.file_id,
    )]

    context.bot.answerInlineQuery(update.inline_query.id, results=results)
    os.remove(filename)
    context.bot.delete_message(chat_id=magic_chat_id, message_id=message.message_id)


def start(update, context):
    context.bot.sendMessage(update.message.chat_id, text='toki! sina wile kama sona e ilo ni la o luka e ni: /help. sina ken sitelen kepeken linja pona kepeken ilo ni! sitelen ni li pini, sina sitelen e "/".\n\nHi! I you want to learn all you can do with the bot, click here: /help. You can use linja pona with this bot. Use it online and append "/" to your sentence. You can add line breaks.')


def settings(update, context, edit_message_or_not=False, extra_text=''):
    # This is only allowed in private chats
    if not edit_message_or_not and update.message.chat_id != update.message.from_user.id:
        context.bot.sendMessage(update.message.chat_id,
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
        filename = generate_pic(query=photo_query, id_chat=query.message.chat_id, image_format='jpg', size=50)
        context.bot.edit_message_media(chat_id=query.message.chat_id,
                               message_id=query.message.message_id,
                               media=InputMediaPhoto(open(filename, 'rb'), caption=text),
                               reply_markup=reply_markup,
                               )
    else:
        filename = generate_pic(query=photo_query, id_chat=update.message.chat_id, image_format='jpg', size=50)
        results = context.bot.send_photo(update.message.chat_id, photo=open(filename, 'rb'), caption=text, parse_mode='Markdown', reply_markup=reply_markup, timeout=60)
    os.remove(filename)


def buttons(update, context):
    query = update.callback_query
    data = query.data.split('|')
    if len(data) == 1:
        if data[0] == Selectable.change_font_type.value:
            fonts_available = Fonts
            fonts_available = [Fonts.linja_pona_jan_same, Fonts.linja_leko_jan_selano, Fonts.sitelen_luka_tu_tu_jan_inkepa, Fonts.sitelen_pona_jan_wesi, Fonts.linja_pimeja_jan_inkepa, Fonts.sitelen_pi_linja_ko_jan_inkepa,Fonts.sitelen_pona_pona_jan_jaku, Fonts.insa_pi_supa_lape_int_main, Fonts.linja_pi_tomo_lipu, Fonts.linja_sike, Fonts.linja_suwi, Fonts.linja_pi_pu_lukin]
            keyboard = []
            for font in fonts_available:
                keyboard.append([InlineKeyboardButton(fonts_dict[font.value], callback_data="{}|{}".format(Selectable.change_font_type.value, font.value))])
            keyboard.append([InlineKeyboardButton('Go back', callback_data="{}".format(Selectable.go_back.value))])

            reply_markup = InlineKeyboardMarkup(keyboard)
            db = TokiPonaDB()
            font_type, _, _ = db.get_data(query.message.chat_id)
            font_type = str(font_type)

            text = '''o luka e nasin. tenpo ni la sina kepeken {}\n\nPick a font. Current is {}.'''.format(fonts_dict.get(font_type, "sona ala"), fonts_dict.get(font_type, "unknown"))
            context.bot.edit_message_media(chat_id=query.message.chat_id,
                                   message_id=query.message.message_id,
                                   media=InputMediaPhoto(id_photo_nasin_sitelen, caption=text),
                                   reply_markup=reply_markup,
                                   )
        elif data[0] == Selectable.change_font_color.value:
            colors_available = [Colors.pimeja, Colors.loje, Colors.jelo, Colors.loje_walo, Colors.laso_kasi, Colors.laso_kasi_walo, Colors.laso_sewi, Colors.laso_sewi_walo, Colors.pimeja_walo_walo, Colors.pimeja_walo, Colors.pimeja_pimeja_walo, Colors.pimeja_pimeja_pimeja_walo, Colors.walo, ]
            keyboard = []
            for color in colors_available:
                keyboard.append([InlineKeyboardButton(colors_dict[color.value], callback_data="{}|{}".format(Selectable.change_font_color.value, color.value))])
            keyboard.append([InlineKeyboardButton('Go back', callback_data="{}".format(Selectable.go_back.value))])

            reply_markup = InlineKeyboardMarkup(keyboard)
            db = TokiPonaDB()
            _, font_color, _ = db.get_data(query.message.chat_id)
            font_color = str(font_color)
            if len(font_color) != 6:
                font_color = '0'*(6-len(font_color)) + str(font_color)

            text = '''o luka e kule sitelen. tenpo ni la sina kepeken {}\n\nPick a color for the font. Current is {}.'''.format(colors_dict[font_color], colors_dict[font_color])
            context.bot.edit_message_media(chat_id=query.message.chat_id,
                                   message_id=query.message.message_id,
                                   media=InputMediaPhoto(id_photo_kule, caption=text),
                                   reply_markup=reply_markup,
                                   )
        elif data[0] == Selectable.change_background_color.value:
            colors_available = [Colors.pimeja, Colors.loje, Colors.jelo, Colors.loje_walo, Colors.laso_kasi, Colors.laso_kasi_walo, Colors.laso_sewi, Colors.laso_sewi_walo, Colors.pimeja_walo_walo, Colors.pimeja_walo, Colors.pimeja_pimeja_walo, Colors.pimeja_pimeja_pimeja_walo, Colors.walo, ]
            keyboard = []
            for color in colors_available:
                keyboard.append([InlineKeyboardButton(colors_dict[color.value], callback_data="{}|{}".format(Selectable.change_background_color.value, color.value))])
            keyboard.append([InlineKeyboardButton('Go back', callback_data="{}".format(Selectable.go_back.value))])


            reply_markup = InlineKeyboardMarkup(keyboard)
            db = TokiPonaDB()
            _, _, background_color = db.get_data(query.message.chat_id)
            background_color = str(background_color)
            if len(background_color) != 6:
                background_color = '0'*(6-len(background_color)) + str(background_color)


            text = '''o luka e kule lipu. tenpo ni la sina kepeken {}\n\nPick a color for the background. Current is {}.'''.format(colors_dict[background_color], colors_dict[background_color])
            context.bot.edit_message_media(chat_id=query.message.chat_id,
                                   message_id=query.message.message_id,
                                   media=InputMediaPhoto(id_photo_kule, caption=text),
                                   reply_markup=reply_markup,
                                   )
        elif data[0] == Selectable.go_back.value:
            settings(update, context, True)
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
        settings(update, context, True, extra_text=success_message)
    else:
        raise TypeError("Button query got a number of arguments different from 1 or 2: {}".format(data))


def help_english(update, context):
    help(update, context, 'en')


def help_toki_pona(update, context):
    help(update, context, 'tp')


def help(update, context, language):
    # This is only allowed in private chats
    if update.message.chat_id != update.message.from_user.id:
        context.bot.sendMessage(update.message.chat_id,
                parse_mode='Markdown',
                text='o toki tawa mi lon [tomo mi](t.me/tokipona_bot) a! (Talk to me in [my private chat](t.me/tokipona_bot)).')
        return
    if language == 'en':
        help_filename = 'help.txt'
    else:
        help_filename = 'sona.txt'

    with open(help_filename , 'r') as f:
        text = f.read()

    result = context.bot.send_photo(update.message.chat_id, photo=id_photo_help, caption=text, parse_mode='Markdown')


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
