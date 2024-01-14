"""Bot supported commands."""
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from callbacks import FormStates, ClientFindChoice, ClientMenuChoice, ClientMakeRecommendationsChoice
from config import Config
from db import get_recommendations, setup_rec_data, update_client_by_id, get_client_by_name
from keyboards import get_start_keyboard, get_clients_keyboard, get_food_protocols_keyboard, \
    recommendations_keyboard_1, recommendations_keyboard_2, get_menu_settings_keyboard, get_clients_settings_keyboard, \
    get_set_recommendations_keyboard
from utils import make_gpt_request


async def send_welcome_keyboard(message: Message, state: FSMContext):
    await state.reset_state()
    await message.answer('Выберите действие:', reply_markup=get_start_keyboard())


async def send_clients_keyboard(message: Message):
    await message.answer('Выберите действие с клиентами:', reply_markup=get_clients_keyboard())


async def get_recommendations_1(message: Message):
    recommendations = get_recommendations(title_name='Витамины')
    msg = ''
    for i in recommendations:
        msg += f'{i["id"]}. {i["name"]}\n'

    await message.answer(text="Выберите рекомендации по <b>Витаминам</b>:\n\n" + msg,
                         reply_markup=recommendations_keyboard_2([]))

    await FormStates.RECOMMENDATION_2.set()


async def choose_user(message: types.Message, state: FSMContext):
    state_data = await state.get_data()

    if state_data['client'] == 'find_client':
        client_data = get_client_by_name(message.text)
        await ClientFindChoice.choosing_user.set()
        await state.update_data(chosen_user=client_data)

        if client_data['recommendations']:
            recommendations = setup_rec_data(client_data['recommendations'])
        else:
            recommendations = 'Нет'

        await message.answer(f'👤 Вы выбрали: {client_data["full_name"]}\n\n'
                             f'<b>Email:</b> {client_data["email"]}\n'
                             f'<b>Протокол питания:</b> {client_data["food_protocol_name"]}\n'
                             f'<b>Аллергии:</b> {client_data["allergic"]}\n'
                             f'<b>Рекомендации:</b> \n{recommendations}')
        await message.answer('Выберите действие: ', reply_markup=get_clients_settings_keyboard())
    elif state_data['client'] == 'upd_menu':
        await message.answer(f"Меню обновлено. \n\n {message.text} ")
        await state.update_data(menu=message.text)
        await message.answer("Выберите действие: ", reply_markup=get_menu_settings_keyboard())
    elif state_data['client'] == 'find_menu':
        client_data = get_client_by_name(message.text)
        await ClientMenuChoice.choosing_user.set()
        await state.update_data(chosen_user=client_data)
        if client_data['food_protocol_id'] is None:
            await message.answer('❗️ У пользователя не заполнен протокол питания ❗️')
            await state.finish()
            await message.answer('Выберите клиента', reply_markup=get_start_keyboard())

        else:
            temp_msg = await message.answer('.. Формируем меню ..')
            if client_data['allergic'] in Config.NO_ANSWER:
                msg = make_gpt_request(client_data['food_protocol_id'], None)
                await state.update_data(menu=msg)
                await temp_msg.edit_text(msg)
                await message.answer(f'Меню для <b>{client_data["full_name"]}</b> сформировано!')
                await message.answer("Выберите действие: ", reply_markup=get_menu_settings_keyboard())

            else:
                msg = make_gpt_request(client_data['food_protocol_id'], client_data['allergic'])
                await state.update_data(menu=msg)
                await temp_msg.edit_text(msg)
                await message.answer(f'Меню для <b>{client_data["full_name"]}</b> сформировано!')
                await message.answer("Выберите действие: ", reply_markup=get_menu_settings_keyboard())
    elif state_data['client'] == 'find_rec':
        client_data = get_client_by_name(message.text)

        await ClientMakeRecommendationsChoice.choosing_user.set()
        await state.update_data(chosen_user=client_data)
        if client_data['recommendations'] is None:
            await message.answer('Выберите действие:', reply_markup=get_set_recommendations_keyboard())

        elif len(client_data['recommendations']) > 0:
            if client_data['recommendations']:
                rec = setup_rec_data(client_data['recommendations'])
            else:
                rec = 'Нет'
            await message.answer(f'👤 Вы выбрали: {client_data["full_name"]}\n\n{rec}')
            await state.finish()
            await message.answer('Выберите действие:', reply_markup=get_start_keyboard())
        else:
            await message.answer('Выберите действие:', reply_markup=get_set_recommendations_keyboard())
    elif state_data['client'] == 'edit_allergic':
        data = await state.get_data()
        data['chosen_user']['allergic'] = message.text
        await state.update_data(**data)

        state_data = await state.get_data()
        update_client_by_id(state_data['chosen_user'])
        if state_data['chosen_user']['recommendations']:
            rec = setup_rec_data(state_data['chosen_user']['recommendations'])
        else:
            rec = 'Нет'
        await message.answer(f'Данные аллергических реакций обновлены! \n\n'
                             f'<b>ФИО:</b> {state_data["chosen_user"]["full_name"]}\n'
                             f'<b>Email:</b> {state_data["chosen_user"]["email"]}\n'
                             f'<b>Протокол питания:</b> {state_data["chosen_user"]["food_protocol_name"]}\n'
                             f'<b>Аллергии:</b> {state_data["chosen_user"]["allergic"]}\n'
                             f'<b>Рекомендации:</b> \n{rec}')
        await state.finish()
        await message.answer('Выберите действие с клиентами:', reply_markup=get_clients_keyboard())

    elif state_data['client'] == 'edit_email':
        data = await state.get_data()
        data['chosen_user']['email'] = message.text
        await state.update_data(**data)

        state_data = await state.get_data()
        update_client_by_id(state_data['chosen_user'])
        if state_data['chosen_user']['recommendations']:
            rec = setup_rec_data(state_data['chosen_user']['recommendations'])
        else:
            rec = 'Нет'
        await message.answer(f'Email обновлен! \n\n'
                             f'<b>ФИО:</b> {state_data["chosen_user"]["full_name"]}\n'
                             f'<b>Email:</b> {state_data["chosen_user"]["email"]}\n'
                             f'<b>Протокол питания:</b> {state_data["chosen_user"]["food_protocol_name"]}\n'
                             f'<b>Аллергии:</b> {state_data["chosen_user"]["allergic"]}\n'
                             f'<b>Рекомендации:</b> \n{rec}')
        await state.finish()
        await message.answer('Выберите действие с клиентами:', reply_markup=get_clients_keyboard())
    elif state_data['client'] == 'edit_name':
        data = await state.get_data()
        data['chosen_user']['full_name'] = message.text
        await state.update_data(**data)

        state_data = await state.get_data()
        update_client_by_id(state_data['chosen_user'])
        if state_data['chosen_user']['recommendations']:
            rec = setup_rec_data(state_data['chosen_user']['recommendations'])
        else:
            rec = 'Нет'
        await message.answer(f'ФИО обновлены! \n\n'
                             f'<b>ФИО:</b> {state_data["chosen_user"]["full_name"]}\n'
                             f'<b>Email:</b> {state_data["chosen_user"]["email"]}\n'
                             f'<b>Протокол питания:</b> {state_data["chosen_user"]["food_protocol_name"]}\n'
                             f'<b>Аллергии:</b> {state_data["chosen_user"]["allergic"]}\n'
                             f'<b>Рекомендации:</b> \n{rec}')
        await state.finish()
        await message.answer('Выберите действие с клиентами:', reply_markup=get_clients_keyboard())
    elif state_data['client'] == 'add_name':
        await FormStates.NAME.set()
        await state.update_data(full_name=message.text)
        await state.update_data(client='add_email')
        await message.answer('Введите email:')
    elif state_data['client'] == 'add_email':
        await state.update_data(email=message.text)
        await state.update_data(client='add_allergic')
        await message.answer('Выберите протоколы питания:', reply_markup=get_food_protocols_keyboard())
        await FormStates.FOOD_PROTOCOL.set()
    elif state_data['client'] == 'add_allergic':
        await state.update_data(allergies=message.text)
        recommendations = get_recommendations(title_name='Работа со стрессом')
        msg = ''
        for i in recommendations['Работа со стрессом']:
            msg += f'{str(i["id"])}. {i["name"]}\n'
        await message.answer(text="Выберите рекомендации по <b>Работе со стрессом</b>:\n\n" + msg,
                             reply_markup=recommendations_keyboard_1([]))
        await FormStates.RECOMMENDATION_1.set()


def register_commands(dp: Dispatcher):
    """Register bot commands."""
    dp.register_message_handler(send_welcome_keyboard, commands=['start'], state='*')
    dp.register_message_handler(send_clients_keyboard, commands=['clients'])
    dp.register_message_handler(send_clients_keyboard, commands=['add_client'])
    dp.register_message_handler(send_clients_keyboard, commands=['find_client'])
    dp.register_message_handler(send_clients_keyboard, commands=['find_client'])
    dp.register_message_handler(choose_user, lambda message: True, state="*")
    dp.register_message_handler(get_recommendations_1, state=FormStates.RECOMMENDATION_1)
