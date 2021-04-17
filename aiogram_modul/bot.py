"""Run bot."""

import asyncio
import logging
from os import getenv
from sys import exit

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiogram_modul.constants import COMMANDS
from aiogram_modul.new_entry import register_handlers_budgeting
from aiogram_modul.common import register_handlers_common

logger = logging.getLogger(__name__)


async def set_commands(bot: Bot):
    """Set commands for run dot."""
    command_list = []
    for command, description in COMMANDS.items():
        command_list.append(
            BotCommand(command=command, description=description)
        )
    await bot.set_my_commands(command_list)


async def main():
    """Run bot."""
    # Settings logging in stdout
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")

    # Declaring and initializing bot and dispatcher objects
    bot_token = getenv("BOT_TOKEN")
    if not bot_token:
        exit("Error: no token provided")

    bot = Bot(token=bot_token)
    dp = Dispatcher(bot, storage=MemoryStorage())

    # Register handler
    register_handlers_budgeting(dp)
    register_handlers_common(dp)
    # Set command bot
    await set_commands(bot)

    # Run polling
    await dp.skip_updates()  # skip updates (optional)
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())
