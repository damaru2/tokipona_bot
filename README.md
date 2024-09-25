# tokipona_bot (ilo sitelen lon ilo Telegram)

[@tokipona_bot](https://t.me/tokipona_bot)

toki a! sina ken sitelen kepeken linja pona kepeken ilo ni a! sitelen ni li pini, o sitelen e sitelen "/".

Hi! If you want to learn all you can do with the bot, go send /help or /sona to the bot. You can use linja pona with this bot. Use it online and append "/" to your sentence. You can add enters for the generated images.

---

There are some hacks you must know if you want to use this. For some reason, Telegram's API only allows online bots to send images or stickers that are on Telegram servers already. So media is sent to a `magic chat` first, used for the online query and then they are deleted immeditely after. So to make this work, you need a file called `private_conf.py` in `/src/private`. The file should contain three things:
 + One variable with a `token_id` string indicating the Telegram bot token.
 + An integer `magic_chat_id` indicating your chat id in Telegram to perform the aforementioned trick of uploading images first.
 + The ids of images for the messages in the settings and help. You can get them by sending the images and observing the returned result. Otherwise change the code to prevent sending the images. The last time I remembered to update this the images' variables were `id_photo_help`, `id_photo_nasin_sitelen`, `id_photo_kule`. But you can check the `import` of the main file.
