"""Run bot."""
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import BotCommand
from aiogram.utils import executor

from aiogram_modul.constants import MENU_COMMANDS
from config import bot_token
from database.db import create_async_database
from aiogram_modul.new_entry import register_handlers_new_entry
from aiogram_modul.base_command import register_handlers_common
from aiogram_modul.statistics import register_handlers_statistics

logger = logging.getLogger(__name__)


bot = Bot(token=bot_token)
dp = Dispatcher(bot, storage=MemoryStorage())


async def on_startup(dispatcher):
    bot['session'] = await create_async_database()
    await set_commands(bot)


async def on_shutdown(dispatcher):
    await dp.bot.get('session').close()
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

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
