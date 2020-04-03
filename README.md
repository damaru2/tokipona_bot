# tokipona_bot (ilo sitelen lon ilo Telegram)

[@tokipona_bot](https://t.me/tokipona_bot)

toki a! sina ken sitelen kepeken linja pona kepeken ilo ni a! sitelen ni li pini, sina sitelen e "/".

Hi! I you want to learn all you can do with the bot, click here: /help. You can use linja pona with this bot. Use it online and append "/" to your sentence. You can add enters for the generated images.

---

This is in early stages of development. For some reason Telegram's API only allows online bots to send images or stickers that are on Telegram servers already. So media is sent to a `magic chat` first, used for the online query and then they are deleted. So to make this work, you need a file called `private_conf.py` in `/src/private`. The file should contain three variables:
 + One with a `token_id` string indicating the Telegram bot token
 + An integer `magic_chat_id` indicating your chat id in Telegram to perform the aforementioned trick of uploading images first.
 + The id of an image for the help message. You can get it by sending an image and observe the returned result. Otherwise remove the image from the help and send the text only.

Currently using [lp.plop.me](lp.plop.me) for extracting the images. 
