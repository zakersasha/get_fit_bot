"""Bot supported commands."""
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from callbacks import FormStates
from db import get_recommendations
from keyboards import get_start_keyboard, get_clients_keyboard, get_food_protocols_keyboard, \
    recommendations_keyboard_1, recommendations_keyboard_2


async def send_welcome_keyboard(message: Message, state: FSMContext):
    await state.reset_state()
    await message.answer('Выберите действие:', reply_markup=get_start_keyboard())


async def send_clients_keyboard(message: Message):
    await message.answer('Выберите действие с клиентами:', reply_markup=get_clients_keyboard())


async def get_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer('Введите email:')
    await FormStates.EMAIL.set()


async def get_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)

    await message.answer('Выберите протоколы питания:', reply_markup=get_food_protocols_keyboard())
    await FormStates.FOOD_PROTOCOL.set()


async def get_allergies(message: Message, state: FSMContext):
    await state.update_data(allergies=message.text)

    recommendations = get_recommendations(title_name='Работа со стрессом')
    msg = ''
    for i in recommendations['Работа со стрессом']:
        msg += f'{str(i["id"])}. {i["name"]}\n'

    await message.answer(text="Выберите рекомендации по <b>Работе со стрессом</b>:\n\n" + msg,
                         reply_markup=recommendations_keyboard_1([]))
    await FormStates.RECOMMENDATION_1.set()


async def get_recommendations_1(message: Message):
    recommendations = get_recommendations(title_name='Витамины')
    msg = ''
    for i in recommendations:
        msg += f'{i["id"]}. {i["name"]}\n'

    await message.answer(text="Выберите рекомендации по <b>Витаминам</b>:\n\n" + msg,
                         reply_markup=recommendations_keyboard_2([]))

    await FormStates.RECOMMENDATION_2.set()


def register_commands(dp: Dispatcher):
    """Register bot commands."""
    dp.register_message_handler(send_welcome_keyboard, commands=['start'], state='*')
    dp.register_message_handler(send_clients_keyboard, commands=['clients'])
    dp.register_message_handler(send_clients_keyboard, commands=['add_client'])
    dp.register_message_handler(send_clients_keyboard, commands=['find_client'])
    dp.register_message_handler(get_name, state=FormStates.NAME)
    dp.register_message_handler(get_email, state=FormStates.EMAIL)
    dp.register_message_handler(get_allergies, state=FormStates.ALLERGIES)
    dp.register_message_handler(get_recommendations_1, state=FormStates.RECOMMENDATION_1)
