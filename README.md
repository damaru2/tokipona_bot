# tokipona_bot

[@tokipona_bot](t.me/tokipona_bot)

toki! sina ken sitelen kepeken linja pona kepeken ilo ni! sitelen ni li pini, sina sitelen e "/".

Hi! You can use linja pona with this bot. Use it online and append "/" to your sentence. You can use enter for the generated images.

---

This is in early stages of development, at the moment the images have to be sent to telegram first and then they can be used online, while this should not be necessary at all in principle. To make this work, you need a file called `private_conf.py` in `/src/private`. The file should contain two variables, one with a token_id string indicating the Telegram bot token, and an integer `magic_chat_id` indicating your chat id in Telegram to perform the aforementioned trick of uploading images first.

Currently using lp.plop.me for the images. 
