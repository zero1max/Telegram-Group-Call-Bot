from aiogram import F
from aiogram.types import Message, ChatMemberUpdated
from aiogram.filters import Command, CommandStart
from loader import router, bot
from collections import defaultdict
import random


user_data = defaultdict(dict)

emojies = ['💀', '🤖', '👻', '👨🏻‍💻', '🧚🏻‍♀️', '🦁', '🦅', '🐼', '🐻', '🦋', '🦧', '🦦']

@router.message(CommandStart())
async def start_msg(msg: Message):
    await msg.answer("Salom! Meni guruhga qo'shib administrator qiling va /call buyrug'idan foydalaning.")

@router.chat_member()
async def track_members_and_add_existing(chat_member_update: ChatMemberUpdated):
    chat_id = chat_member_update.chat.id
    
    # Botning o'zi guruhga qo'shilsa, barcha a'zolarni yuklab olish
    if chat_member_update.new_chat_member.user.id == (await bot.me()).id:
        await add_all_members(chat_id, bot)
        return

    # Yangi qo'shilgan foydalanuvchilarni qo'shish
    if chat_member_update.new_chat_member.status in ["member", "administrator"]:
        user = chat_member_update.new_chat_member.user
        if not user.is_bot:
            name = user.first_name or "NoName"
            user_data[chat_id][user.id] = name
            print(f"Yangi foydalanuvchi qo'shildi: {name} ({user.id})")

async def add_all_members(chat_id: int):
    """Guruhdagi barcha mavjud foydalanuvchilarni ro'yxatga oladi."""
    async for member in bot.get_chat_administrators(chat_id):
        if not member.user.is_bot:
            name = member.user.first_name or "NoName"
            user_data[chat_id][member.user.id] = name
            print(f"Mavjud foydalanuvchi qo'shildi: {name} ({member.user.id})")

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
