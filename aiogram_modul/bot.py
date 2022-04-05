"""Run bot."""
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import BotCommand
from aiogram.utils import executor
from aiogram.utils.executor import start_webhook

from aiogram_modul.constants import MENU_COMMANDS, USER_IDS
from database.db import create_async_database
from aiogram_modul.middlewares import AccessMiddleware
from aiogram_modul.new_entry import register_handlers_new_entry
from aiogram_modul.base_command import register_handlers_common
from aiogram_modul.statistics import register_handlers_statistics

logger = logging.getLogger(__name__)


TOKEN = os.getenv('BOT_TOKEN', '5152082846:AAFT8l2UXHcr0uEL6LDqGTfyN0XAY9EAGyw')
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(AccessMiddleware(list(USER_IDS.keys())))

HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME', 'budgeting-bot')

# webhook settings
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT', 8000)


async def on_startup(dispatcher):
    bot['session'] = await create_async_database()
    await set_commands(bot)
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


async def on_shutdown(dispatcher):
    await dp.bot.get('session').close()
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()


async def set_commands(bot: Bot):
    """Set commands for run dot."""
    command_list = []
    for command, description in MENU_COMMANDS.items():
        command_list.append(
            BotCommand(command=command, description=description)
        )
    await bot.set_my_commands(command_list)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # Register handler
    register_handlers_new_entry(dp)
    register_handlers_common(dp)
    register_handlers_statistics(dp)

    # executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
