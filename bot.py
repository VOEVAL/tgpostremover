import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
from datetime import datetime

# Загрузка переменных окружения
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
KEY_PHRASE = "bo_white is online"
DELETE_DELAY = 18000  # секунд

# Настройка логгирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота
bot = Bot(
    token=BOT_TOKEN,
    session=AiohttpSession(),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()

# ✅ Обновлённый хендлер, проверяющий и text, и caption
@dp.channel_post()
async def handle_channel_post(message: Message):
    content = message.text or message.caption  # Берём текст поста или подпись к фото

    if content and KEY_PHRASE in content:
        logging.info(f"[{datetime.now()}] Найдена фраза '{KEY_PHRASE}' в сообщении ID {message.message_id}")
        await asyncio.sleep(DELETE_DELAY)

        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            logging.info(f"[{datetime.now()}] Сообщение удалено: {message.message_id}")
        except Exception as e:
            logging.error(f"Ошибка при удалении сообщения: {e}")

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
