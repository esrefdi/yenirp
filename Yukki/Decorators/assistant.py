import random
from typing import Dict, List, Union

from pyrogram import filters
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, InputMediaPhoto, Message)

from Yukki import BOT_ID, MUSIC_BOT_NAME, app, random_assistant
from Yukki.Database import get_assistant, save_assistant
from Yukki.Utilities.assistant import get_assistant_details


@app.on_callback_query(filters.regex("ban_köməkçisi"))
async def unban_assistant_(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    query, user_id = callback_request.split("|")
    a = await app.get_chat_member(CallbackQuery.message.chat.id, BOT_ID)
    if not a.can_restrict_members:
        return await CallbackQuery.answer(
            "İstifadəçinin qadağası/bandan çıxarılması icazəm yoxdur.  İstənilən admindən köməkçinin qadağanını ləğv etməsini xahiş edin.",
            show_alert=True,
        )
    else:
        try:
            await app.unban_chat_member(
                CallbackQuery.message.chat.id, user_id
            )
        except:
            return await CallbackQuery.answer(
                "Qadağanı ləğv etmək alınmadı",
                show_alert=True,
            )
        return await CallbackQuery.edit_message_text(
            "Assistent Qadağan Edildi.  İndi Oynamağa cəhd edin."
        )


def AssistantAdd(mystic):
    async def wrapper(_, message):
        _assistant = await get_assistant(message.chat.id, "köməkçi")
        if not _assistant:
            ran_ass = random.choice(random_assistant)
            assis = {
                "xilasedici köməkçi": ran_ass,
            }
            await save_assistant(message.chat.id, "köməkçi", assis)
        else:
            ran_ass = _assistant["xilasedici köməkçi"]
        if ran_ass not in random_assistant:
            ran_ass = random.choice(random_assistant)
            assis = {
                "xilasedici köməkçi": ran_ass,
            }
            await save_assistant(message.chat.id, "köməkçi", assis)
        ASS_ID, ASS_NAME, ASS_USERNAME, ASS_ACC = await get_assistant_details(
            ran_ass
        )
        try:
            b = await app.get_chat_member(message.chat.id, ASS_ID)
            key = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="🗑 Köməkçinin qadağasını aradan qaldırın",
                            callback_data=f"unban_assistant a|{ASS_ID}",
                        )
                    ],
                ]
            )
            if b.status == "kicked":
                return await message.reply_text(
                    f"Assistent Hesabı[{ASS_ID}] qadağan edilib.\nMusiqi Botundan istifadə etmək üçün əvvəlcə onu blokdan çıxarın\n\nİstifadəçi adı: @{ASS_USERNAME}",
                    reply_markup=key,
                )
            if b.status == "qadağan edilib":
                return await message.reply_text(
                    f"Assistent Hesabı[{ASS_ID}] qadağan edilib.\nMusiqi Botundan istifadə etmək üçün əvvəlcə onu blokdan çıxarın\n\nİstifadəçi adı: @{ASS_USERNAME}",
                    reply_markup=key,
                )
        except UserNotParticipant:
            if message.chat.username:
                try:
                    await ASS_ACC.join_chat(message.chat.username)
                except UserAlreadyParticipant:
                    pass
                except Exception as e:
                    await message.reply_text(
                        f"__Assistent qoşula bilmədi__\n\n**Səbəb**: {e}"
                    )
                    return
            else:
                try:
                    invitelink = await app.export_chat_invite_link(
                        message.chat.id
                    )
                    if invitelink.startswith("https://t.me/+"):
                        invitelink = invitelink.replace(
                            "https://t.me/+", "https://t.me/joinchat/"
                        )
                    await ASS_ACC.join_chat(invitelink)
                    await message.reply(
                        f"{ASS_NAME} Uğurla Qoşuldu",
                    )
                except UserAlreadyParticipant:
                    pass
                except Exception as e:
                    await message.reply_text(
                        f"__Assistent qoşula bilmədi__\n\n**Səbəb**: {e}"
                    )
                    return
        return await mystic(_, message)

    return wrapper
