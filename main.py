"""App initialization."""
import asyncio
import logging

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault

from callbacks import register_callbacks
from commands import register_commands
from config import Config
from updates_worker import get_handled_updates_list

load_dotenv()


async def set_bot_commands(bot: Bot):
    """Menu bar commands."""
    commands = [
        BotCommand(command='start', description='Взаимодействие с ботом'),
        BotCommand(command='clients', description='Взаимодействие с клиентами'),
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())


async def main():
    """Bot app creation."""
    logging.basicConfig(level=logging.INFO)

    bot = Bot(Config.TOKEN, parse_mode='HTML')
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

    register_commands(dp)
    register_callbacks(dp)

    await set_bot_commands(bot)

    try:
        await dp.start_polling(allowed_updates=get_handled_updates_list(dp))
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


try:
    asyncio.run(main())
except (KeyboardInterrupt, SystemExit):
    logging.info('Bot stopped!')
