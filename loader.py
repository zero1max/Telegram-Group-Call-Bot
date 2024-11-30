from aiogram import Dispatcher , Router, Bot
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
import os

load_dotenv('.env')

token = os.getenv("BOT_TOKEN")

# db_pro = Database_Product()
dp = Dispatcher()
router = Router()
bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp.include_router(router=router)