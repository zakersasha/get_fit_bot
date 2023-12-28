"""Bot supported commands."""
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from callbacks import FormStates
from config import Config
from keyboards import get_start_keyboard, get_clients_keyboard, get_food_protocols_keyboard, \
    get_recommendations_keyboard


async def send_welcome_keyboard(message: Message):
    await message.answer('Выберите действие:', reply_markup=get_start_keyboard())


async def send_clients_keyboard(message: Message):
    await message.answer('Выберите действие с клиентами:', reply_markup=get_clients_keyboard())


async def get_name(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
        Config.NEW_CLIENT['name'] = message.text

    await message.answer('Введите email:')
    await FormStates.EMAIL.set()


async def get_email(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['email'] = message.text
        Config.NEW_CLIENT['email'] = message.text

    await message.answer('Выберите протоколы питания:', reply_markup=get_food_protocols_keyboard())
    await FormStates.FOOD_PROTOCOL.set()


async def get_allergies(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['allergies'] = message.text
        Config.NEW_CLIENT['allergies'] = message.text
    await message.answer(text="Выберите рекомендации:",
                         reply_markup=get_recommendations_keyboard(Config.RECOMMENDATIONS_CHOICES))
    await FormStates.RECOMMENDATIONS.set()


def register_commands(dp: Dispatcher):
    """Register bot commands."""
    dp.register_message_handler(send_welcome_keyboard, commands=['start'])
    dp.register_message_handler(send_clients_keyboard, commands=['clients'])
    dp.register_message_handler(get_name, state=FormStates.NAME)
    dp.register_message_handler(get_email, state=FormStates.EMAIL)
    dp.register_message_handler(get_allergies, state=FormStates.ALLERGIES)
