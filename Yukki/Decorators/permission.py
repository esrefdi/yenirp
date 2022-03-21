from typing import Dict, List, Union

from Yukki import BOT_ID, app


def PermissionCheck(mystic):
    async def wrapper(_, message):
        if message.chat.type == "private":
            return await mystic(_, message)
        a = await app.get_chat_member(message.chat.id, BOT_ID)
        if a.status != "administrator":
            return await message.reply_text(
                "Bəzi icazələrlə admin olmalıyam:\n"
                + "\n- **can_manage_voice_chats:** Səsli söhbətləri idarə etmək üçün ♻️"
                + "\n- **can_delete_messages:** Botun Axtardığı Tullantıları silmək üçün 🚮"
                + "\n- **can_invite_users**: Köməkçini söhbətə dəvət etmək üçün."
            )
        if not a.can_manage_voice_chats:
            await message.reply_text(
                "Bu əməliyyatı yerinə yetirmək üçün tələb olunan icazəm yoxdur."
                + "\n**İcazə:** __MANAGE VOICE CHATS__"
            )
            return
        if not a.can_delete_messages:
            await message.reply_text(
                "Bu əməliyyatı yerinə yetirmək üçün tələb olunan icazəm yoxdur."
                + "\n**İcazə:** __DELETE MESSAGES__"
            )
            return
        if not a.can_invite_users:
            await message.reply_text(
                "Bu əməliyyatı yerinə yetirmək üçün tələb olunan icazəm yoxdur."
                + "\n**İcazə:** __INVITE USERS VIA LINK__"
            )
            return
        return await mystic(_, message)

    return wrapper
