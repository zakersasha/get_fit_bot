"""App initialization."""
import asyncio
import logging

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types
from aiogram.types import BotCommand, BotCommandScopeDefault, InputTextMessageContent

from callbacks import register_callbacks, ClientFind, ClientFindMenu, ClientFindRec
from commands import register_commands
from config import Config
from db import get_clients_data
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

    getfit_menu_bot = Bot(Config.TOKEN, parse_mode='HTML', timeout=600)
    storage = MemoryStorage()
    dp = Dispatcher(getfit_menu_bot, storage=storage)

    register_commands(dp)
    register_callbacks(dp)

    @dp.inline_handler(state=ClientFind.user)
    async def inline_query(query: types.InlineQuery, state: FSMContext):
        query_text = query.query.lower()
        results = []

        users = await get_clients_data()

        for user in users:
            if query_text in user['full_name'].lower():
                results.append(
                    types.InlineQueryResultArticle(
                        id=str(hash(user['full_name'])),
                        title=user['full_name'],
                        input_message_content=InputTextMessageContent(message_text=user['full_name']),
                    )
                )

        await state.update_data(client='find_client')
        await query.answer(results=results, cache_time=5)

    @dp.inline_handler(state=ClientFindMenu.user)
    async def inline_query(query: types.InlineQuery, state: FSMContext):
        query_text = query.query.lower()
        results = []

        users = await get_clients_data()

        for user in users:
            if query_text in user['full_name'].lower():
                results.append(
                    types.InlineQueryResultArticle(
                        id=str(hash(user['full_name'])),
                        title=user['full_name'],
                        input_message_content=InputTextMessageContent(message_text=user['full_name']),
                    )
                )

        await state.update_data(client='find_menu')
        await query.answer(results=results, cache_time=5)

    @dp.inline_handler(state=ClientFindRec.user)
    async def inline_query(query: types.InlineQuery, state: FSMContext):
        query_text = query.query.lower()
        results = []

        users = await get_clients_data()

        for user in users:
            if query_text in user['full_name'].lower():
                results.append(
                    types.InlineQueryResultArticle(
                        id=str(hash(user['full_name'])),
                        title=user['full_name'],
                        input_message_content=InputTextMessageContent(message_text=user['full_name']),
                    )
                )

        await state.update_data(client='find_rec')
        await query.answer(results=results, cache_time=5)

    await set_bot_commands(getfit_menu_bot)
    try:
        await dp.start_polling(allowed_updates=get_handled_updates_list(dp))
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await getfit_menu_bot.session.close()


try:
    asyncio.run(main())
except (KeyboardInterrupt, SystemExit):
    logging.info('Bot stopped!')
