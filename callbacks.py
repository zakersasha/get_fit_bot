"""Keyboard manipulation callbacks"""
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from config import Config
from db import get_protocol_by_id, get_recommendations_by_ids, save_new_client, get_client_by_id, delete_client_by_id
from keyboards import get_clients_keyboard, get_recommendations_keyboard, get_clients_list_keyboard, \
    get_clients_settings_keyboard, get_remove_question_keyboard, get_start_keyboard


class FormStates(StatesGroup):
    NAME = State()
    EMAIL = State()
    FOOD_PROTOCOL = State()
    ALLERGIES = State()
    RECOMMENDATIONS = State()


async def process_callback_inline(call: types.CallbackQuery):
    if call.data == 'clients':
        await call.message.edit_reply_markup(reply_markup=get_clients_keyboard())
    elif call.data == 'menu':
        await call.message.edit_text('📝 Формируем меню.')
    elif call.data == 'recommendations':
        await call.message.edit_text('💬 Формируем рекоммендации.')
    elif call.data == 'add_client':
        await call.message.edit_text('➕ 👤 Добавление нового клиента.')
        await call.message.answer('Введите ФИО:')
        await FormStates.NAME.set()
    elif call.data == 'find_client':
        await call.message.answer('Выберите клиента:', reply_markup=get_clients_list_keyboard())
    elif call.data.startswith('client_'):
        client_data = get_client_by_id(int(call.data.replace('client_', '')))
        Config.CLIENT_ID_TO_DELETE = int(call.data.replace('client_', ''))
        await call.message.edit_text(f'👤 Вы выбрали: {client_data["full_name"]}')
        await call.message.answer('Выберите действие: ', reply_markup=get_clients_settings_keyboard())
    elif call.data == 'edit_client':
        await call.message.edit_text('Редактирование профиля клиента.')
        await call.message.answer('Введите ФИО:')
        await FormStates.NAME.set()
    elif call.data == 'remove_client':
        await call.message.edit_text('Вы уверены, что хотите удалить клиента?',
                                     reply_markup=get_remove_question_keyboard())
    elif call.data == 'removal_yes':
        delete_client_by_id(Config.CLIENT_ID_TO_DELETE)
        await call.message.edit_text(f'Клиент удален!')
        await call.message.answer('Выберите действие:', reply_markup=get_start_keyboard())
    elif call.data == 'removal_no':
        await call.message.answer('Выберите действие: ', reply_markup=get_clients_settings_keyboard())


async def process_food_protocol(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        protocol = call.data.replace('protocol_', '')
        if 'food_protocol' in data:
            data['food_protocol'].append(protocol)
            Config.NEW_CLIENT['food_protocol'] = protocol
        else:
            data['food_protocol'] = [protocol]
            Config.NEW_CLIENT['food_protocol'] = protocol

    await call.message.edit_text('Введите информацию об аллергических реакциях:')
    await FormStates.ALLERGIES.set()


async def process_recommendations(call: types.CallbackQuery):
    option = call.data.replace('recommendation_', '')

    if option in Config.RECOMMENDATIONS_CHOICES:
        Config.RECOMMENDATIONS_CHOICES.remove(option)
    else:
        Config.RECOMMENDATIONS_CHOICES.append(option)

    keyboard = get_recommendations_keyboard(Config.RECOMMENDATIONS_CHOICES)
    await call.message.edit_reply_markup(reply_markup=keyboard)


async def apply_timings(call: types.CallbackQuery, state: FSMContext):
    Config.NEW_CLIENT['recommendations'] = Config.RECOMMENDATIONS_CHOICES
    recommendation_ids = [int(i) for i in Config.NEW_CLIENT['recommendations']]
    recommendations = get_recommendations_by_ids(recommendation_ids)
    food_protocol_name = get_protocol_by_id(int(Config.NEW_CLIENT["food_protocol"]))
    save_new_client(name=Config.NEW_CLIENT["name"],
                    email=Config.NEW_CLIENT["email"],
                    food_protocol_id=int(Config.NEW_CLIENT["food_protocol"]),
                    food_protocol_name=food_protocol_name,
                    allergic=Config.NEW_CLIENT["allergies"],
                    recommendations=recommendations,
                    recommendations_ids=recommendation_ids)

    await call.message.edit_text(f'Данные сохранены! \n'
                                 f'ФИО: {Config.NEW_CLIENT["name"]}\n'
                                 f'Email: {Config.NEW_CLIENT["email"]}\n'
                                 f'Протокол питания: {food_protocol_name}\n'
                                 f'Аллергии: {Config.NEW_CLIENT["allergies"]}\n'
                                 f'Рекомендации: {", ".join(recommendations)}')

    Config.NEW_CLIENT.clear()
    Config.RECOMMENDATIONS_CHOICES.clear()
    await state.finish()
    await call.message.answer('Выберите действие:', reply_markup=get_start_keyboard())


def register_callbacks(dp: Dispatcher):
    """Register bot callbacks and triggers."""
    dp.register_callback_query_handler(process_callback_inline, lambda c: True)
    dp.register_callback_query_handler(process_food_protocol, lambda c: c.data.startswith('protocol_'),
                                       state=FormStates.FOOD_PROTOCOL)
    dp.register_callback_query_handler(process_recommendations, lambda c: c.data.startswith('recommendation_'),
                                       state=FormStates.RECOMMENDATIONS)
    dp.register_callback_query_handler(apply_timings, lambda c: c.data in 'save_client',
                                       state=FormStates.RECOMMENDATIONS)
