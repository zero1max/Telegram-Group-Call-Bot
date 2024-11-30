from aiogram import F
from aiogram.types import Message, ChatMemberUpdated
from aiogram.filters import Command, CommandStart
from loader import router, bot
from collections import defaultdict


user_data = defaultdict(dict)

@router.message(CommandStart())
async def start_msg(msg: Message):
    await msg.answer("Salom! Meni guruhga qo'shib administrator qiling va /call buyrug'idan foydalaning.")

# Guruhga yangi foydalanuvchi qo'shilganda ma'lumotni saqlash
@router.chat_member()
async def track_new_members(chat_member_update: ChatMemberUpdated):
    if chat_member_update.new_chat_member.status in ["member", "administrator"]:
        user = chat_member_update.new_chat_member.user
        chat_id = chat_member_update.chat.id
        if not user.is_bot:
            user_data[chat_id][user.id] = user.first_name
            print(f"Foydalanuvchi qo'shildi: {user.first_name} ({user.id})")

# Guruhdagi barcha foydalanuvchilarni "mention" qilish
@router.message(Command("call"))
async def call_members(msg: Message):
    chat_id = msg.chat.id
    if chat_id not in user_data or not user_data[chat_id]:
        await msg.answer("Hozircha hech qanday foydalanuvchi ma'lumotini to'plamadim!")
        return

    # Foydalanuvchilarni Markdown formatida tayyorlash
    mentions = [
        f"[{name}](tg://user?id={user_id})"
        for user_id, name in user_data[chat_id].items()
    ]
    mention_text = "\n".join(mentions)

    if len(mention_text) > 4096:  # Telegram xabar cheklovi
        await msg.answer("Juda ko'p foydalanuvchi bor. Xabarni qisqartirish kerak.")
    else:
        await msg.answer(mention_text, parse_mode="Markdown")

# Stiker ustiga foydalanuvchini bog'lash
@router.message(F.content_type == "sticker")
async def sticker_reply(msg: Message):
    chat_id = msg.chat.id
    user_id = msg.from_user.id
    user_name = msg.from_user.first_name

    if chat_id in user_data and user_id in user_data[chat_id]:
        await msg.answer_sticker(msg.sticker.file_id)
        await msg.answer(user_name, f"tg://user?id={user_id})" + " bu yerda!")
    else:
        await msg.answer("Sizning ma'lumotlaringiz saqlanmagan!")
