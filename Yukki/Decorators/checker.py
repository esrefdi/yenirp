from Yukki import BOT_USERNAME, LOG_GROUP_ID, app
from Yukki.Database import blacklisted_chats, is_gbanned_user, is_on_off


def checker(mystic):
    async def wrapper(_, message):
        if message.sender_chat:
            return await message.reply_text(
                "Siz bu Çat Qrupunda __Anonim Admin__siniz!\nİdarəetmə Hüquqlarından İstifadəçi Hesabına qayıdın."
            )
        blacklisted_chats_list = await blacklisted_chats()
        if message.chat.id in blacklisted_chats_list:
            await message.reply_text(
                f"**Qara Siyahıya salınmış Söhbət**\n\nSöhbətiniz Sudo İstifadəçiləri tərəfindən qara siyahıya salınıb. İstənilən __SUDO USER__-dan ağ siyahıya salınmasını istəyin.\nSudo İstifadəçilərinin Siyahısını yoxlayın [Buradan](https://t.me/{BOT_USERNAME}?start=sudolist)"
            )
            return await app.leave_chat(message.chat.id)
        if await is_on_off(1):
            if int(message.chat.id) != int(LOG_GROUP_ID):
                return await message.reply_text(
                    f"Bot baxım altındadır.  Narahatçılığa görə üzr istəyirik!"
                )
        if await is_gbanned_user(message.from_user.id):
            return await message.reply_text(
                f"**Qanlanmış İstifadəçi**\n\nSiz Botdan istifadə etməkdən məhrum olmusunuz. İstənilən __SUDO USER__-dan ungban-a müraciət edin.\nSudo İstifadəçilərinin Siyahısını Yoxlayın [Buradan](https://t.me/{BOT_USERNAME}?start=sudolist)"
            )
        return await mystic(_, message)

    return wrapper


def checkerCB(mystic):
    async def wrapper(_, CallbackQuery):
        blacklisted_chats_list = await blacklisted_chats()
        if CallbackQuery.message.chat.id in blacklisted_chats_list:
            return await CallbackQuery.answer(
                "Blacklisted Chat", show_alert=True
            )
        if await is_on_off(1):
            if int(CallbackQuery.message.chat.id) != int(LOG_GROUP_ID):
                return await CallbackQuery.answer(
                    "Bot baxım altındadır.  Narahatçılığa görə üzr istəyirik!",
                    show_alert=True,
                )
        if await is_gbanned_user(CallbackQuery.from_user.id):
            return await CallbackQuery.answer(
                "You're Gbanned", show_alert=True
            )
        return await mystic(_, CallbackQuery)

    return wrapper
