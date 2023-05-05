import asyncio
import logging
import random
import string
import sys

from db_utils import insert_data, get_link, get_user_links

from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = ''

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("URL shortener")


@dp.message_handler(commands=['my_links'])
async def my_links(message: types.Message):
    links = await get_user_links(message.from_user.id)
    await message.answer('\n'.join(links))


@dp.message_handler(commands=['my_id'])
async def my_id(message: types.Message):
    await message.reply(message.from_user.id)


@dp.message_handler()
async def my_id(message: types.Message):
    old_url = message.text
    if old_url.startswith('http://') or old_url.startswith('https://'):
        letters_and_digits = string.ascii_lowercase + string.digits
        new_url = ''.join(random.choice(letters_and_digits) for _ in range(6))
        await insert_data(old_url, new_url, message.from_user.id)
        await message.reply(f'http://127.0.0.1:8080/{new_url}')
    else:
        await message.reply('Link should start with "http://" or "https://"')

if __name__ == '__main__':
    if sys.version_info >= (3, 8) and sys.platform.lower().startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    executor.start_polling(dp, skip_updates=True)
