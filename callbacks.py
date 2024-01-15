"""Keyboard manipulation callbacks"""
import os
import zipfile

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from config import Config
from db import get_protocol_by_id, get_recommendations_by_ids, save_new_client, get_client_by_id, delete_client_by_id, \
    get_recommendations, update_user_recommendations, setup_rec_data, update_client_by_id
from keyboards import get_clients_keyboard, \
    get_clients_settings_keyboard, get_remove_question_keyboard, get_start_keyboard, recommendations_keyboard_1, \
    recommendations_keyboard_2, recommendations_keyboard_3, recommendations_keyboard_4, recommendations_keyboard_5, \
    recommendations_keyboard_6, get_clients_list_keyboard_rec, \
    recommendation_edit_keyboard_1, recommendation_edit_keyboard_2, recommendation_edit_keyboard_3, \
    recommendation_edit_keyboard_4, recommendation_edit_keyboard_5, recommendation_edit_keyboard_6, \
    get_edit_list_keyboard, get_edit_food_protocols_keyboard, \
    edit_recommendation_keyboard_1, edit_recommendation_keyboard_2, edit_recommendation_keyboard_3, \
    edit_recommendation_keyboard_4, edit_recommendation_keyboard_5, edit_recommendation_keyboard_6, \
    get_menu_settings_keyboard, get_back_keyboard, get_reply_bot, get_reply_bot_clients
from utils import execute_fusion_api, remove_all_files_and_folders


class FormStates(StatesGroup):
    NAME = State()
    EMAIL = State()
    FOOD_PROTOCOL = State()
    ALLERGIES = State()
    RECOMMENDATION_1 = State()
    RECOMMENDATION_2 = State()
    RECOMMENDATION_3 = State()
    RECOMMENDATION_4 = State()
    RECOMMENDATION_5 = State()
    RECOMMENDATION_6 = State()


class ClientFind(StatesGroup):
    user = State()


class ClientFindMenu(StatesGroup):
    user = State()


class ClientFindRec(StatesGroup):
    user = State()


class RecStates(StatesGroup):
    REC_1 = State()
    REC_2 = State()
    REC_3 = State()
    REC_4 = State()
    REC_5 = State()
    REC_6 = State()


class ClientFindChoice(StatesGroup):
    choosing_user = State()
    name = State()
    email = State()
    allergic = State()
    food = State()
    RECOMMENDATION_1 = State()
    RECOMMENDATION_2 = State()
    RECOMMENDATION_3 = State()
    RECOMMENDATION_4 = State()
    RECOMMENDATION_5 = State()
    RECOMMENDATION_6 = State()


class ClientMenuChoice(StatesGroup):
    choosing_user = State()


class ClientMenuEdit(StatesGroup):
    menu = State()


class ClientMakeRecommendationsChoice(StatesGroup):
    choosing_user = State()


async def process_start_callback_clients(call: types.CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=await get_clients_keyboard())


async def process_start_callback_menu(call: types.CallbackQuery):
    await ClientFindMenu.user.set()
    await call.message.edit_text('Выберите клиента:', reply_markup=await get_reply_bot())


async def process_start_callback_recommendations(call: types.CallbackQuery):
    await ClientFindRec.user.set()
    await call.message.edit_text('💬 Формируем рекоммендации.\n Выберите клиента:', reply_markup=await get_reply_bot())


async def process_generate_pictures(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    await call.message.edit_text("... Генерируем картинки по меню ... ")
    path_list = await execute_fusion_api(state_data['chosen_user']['full_name'], state_data['menu'])
    with zipfile.ZipFile(Config.ZIP_PATH, 'w') as zipf:
        for path in path_list:
            zipf.write(path, arcname=os.path.basename(path))

    with open(Config.ZIP_PATH, 'rb') as file:
        await call.message.edit_text("Архив с картинками готов!")
        await call.message.answer_document(file)
        await remove_all_files_and_folders(os.path.join(Config.IMAGES_PATH, state_data['chosen_user']['full_name']))

    await state.finish()
    await call.message.answer('Выберите действие:', reply_markup=await get_start_keyboard())


async def process_edit_menu(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(client='upd_menu')
    await call.message.edit_text("Введите обновленное меню", reply_markup=await get_back_keyboard())
    await ClientMenuEdit.menu.set()


async def process_back_menu(call: types.CallbackQuery):
    await call.message.edit_text("Выберите действие: ", reply_markup=await get_menu_settings_keyboard())


async def process_client_back(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.answer('Выберите клиента:', reply_markup=await get_clients_list_keyboard_rec())


async def process_clients_callback_add(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(client='add_name')
    await call.message.edit_text('➕ 👤 Добавление нового клиента.')
    await call.message.answer('Введите ФИО:')
    await FormStates.NAME.set()


async def process_clients_callback_find(call: types.CallbackQuery):
    await ClientFind.user.set()
    await call.message.edit_text('Выберите клиента:', reply_markup=await get_reply_bot_clients())


async def process_clients_find_callback(call: types.CallbackQuery, state: FSMContext):
    client_data = await get_client_by_id(int(call.data.replace('client_', '')))
    await ClientFindChoice.choosing_user.set()
    await state.update_data(chosen_user=client_data)

    if client_data['recommendations']:
        recommendations = await setup_rec_data(client_data['recommendations'])
    else:
        recommendations = 'Нет'

    await call.message.edit_text(f'👤 Вы выбрали: {client_data["full_name"]}\n\n'
                                 f'<b>Email:</b> {client_data["email"]}\n'
                                 f'<b>Протокол питания:</b> {client_data["food_protocol_name"]}\n'
                                 f'<b>Аллергии:</b> {client_data["allergic"]}\n'
                                 f'<b>Рекомендации:</b> \n{recommendations}')

    await call.message.answer('Выберите действие: ', reply_markup=await get_clients_settings_keyboard())


async def process_client_edit_callback(call: types.CallbackQuery):
    await call.message.edit_text('Выберите пункт для редактирования: ', reply_markup=await get_edit_list_keyboard())


async def process_client_remove_callback(call: types.CallbackQuery):
    await call.message.edit_text('Вы уверены, что хотите удалить клиента?',
                                 reply_markup=await get_remove_question_keyboard())


async def process_edit_name(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(client='edit_name')
    await call.message.edit_text('Введите новые ФИО:')
    await ClientFindChoice.name.set()


async def process_edit_email(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(client='edit_email')
    await call.message.edit_text('Введите новый Email:')
    await ClientFindChoice.email.set()


async def process_edit_allergic(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(client='edit_allergic')
    await call.message.edit_text(
        'Введите продукты, которые не соответствуют вкусовым предпочтениям, вызывают аллергическую реакцию или '
        'непереносимость:')
    await ClientFindChoice.allergic.set()


async def process_edit_food(call: types.CallbackQuery):
    await call.message.edit_text('Выберите новый протокол питания:', reply_markup=await get_edit_food_protocols_keyboard())
    await ClientFindChoice.food.set()


async def process_edit_food_protocol(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    data['chosen_user']['food_protocol_id'] = int(call.data.replace('edit_protocol_', ''))
    data['chosen_user']['food_protocol_name'] = await get_protocol_by_id(int(call.data.replace('edit_protocol_', '')))
    await state.update_data(**data)

    state_data = await state.get_data()
    await update_client_by_id(state_data['chosen_user'])
    if state_data['chosen_user']['recommendations']:
        rec = await setup_rec_data(state_data['chosen_user']['recommendations'])
    else:
        rec = 'Нет'
    await call.message.answer(f'ФИО обновлены! \n\n'
                              f'<b>ФИО:</b> {state_data["chosen_user"]["full_name"]}\n'
                              f'<b>Email:</b> {state_data["chosen_user"]["email"]}\n'
                              f'<b>Протокол питания:</b> {state_data["chosen_user"]["food_protocol_name"]}\n'
                              f'<b>Аллергии:</b> {state_data["chosen_user"]["allergic"]}\n'
                              f'<b>Рекомендации:</b> \n{rec}')
    await state.finish()
    await call.message.answer('Выберите действие с клиентами:', reply_markup=await get_clients_keyboard())


async def process_client_remove_yes_callback(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    await delete_client_by_id(state_data['chosen_user']['id'])
    await call.message.edit_text(f'Клиент удален!')
    await state.finish()
    await call.message.answer('Выберите действие:', reply_markup=await get_start_keyboard())


async def process_client_remove_no_callback(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.answer('Выберите действие:', reply_markup=await get_start_keyboard())


async def process_food_protocol(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(food_protocol=call.data.replace('protocol_', ''))
    await call.message.edit_text(
        'Введите продукты, которые не соответствуют вкусовым предпочтениям, вызывают аллергическую реакцию или '
        'непереносимость:')
    await FormStates.ALLERGIES.set()


async def process_recommendation_1(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    my_list = state_data.get("RECOMMENDATION_1", [])
    option = call.data.replace('recommendation_1_', '')

    if option in my_list:
        my_list.remove(option)
    else:
        my_list.append(option)

    await state.update_data(RECOMMENDATION_1=my_list)
    await call.message.edit_reply_markup(reply_markup=await recommendations_keyboard_1(my_list))


async def process_save_recommendation_1(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    try:
        await state.update_data(RECOMMENDATION_1=list(map(int, state_data['RECOMMENDATION_1'])))
    except KeyError:
        await state.update_data(RECOMMENDATION_1=[])

    recommendations = await get_recommendations(title_name='Витамины')
    msg = ''
    for i in recommendations['Витамины']:
        msg += f'{i["id"]}. {i["name"]}\n'

    await call.message.edit_text(text="Выберите рекомендации по <b>Витаминам</b>:\n\n" + msg,
                                 reply_markup=await recommendations_keyboard_2([]))
    await FormStates.RECOMMENDATION_2.set()


async def process_recommendation_2(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    my_list = state_data.get("RECOMMENDATION_2", [])
    option = call.data.replace('recommendation_2_', '')

    if option in my_list:
        my_list.remove(option)
    else:
        my_list.append(option)

    await state.update_data(RECOMMENDATION_2=my_list)

    await call.message.edit_reply_markup(reply_markup=await recommendations_keyboard_2(my_list))


async def process_save_recommendation_2(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()

    try:
        await state.update_data(RECOMMENDATION_2=list(map(int, state_data['RECOMMENDATION_2'])))
    except KeyError:
        await state.update_data(RECOMMENDATION_2=[])

    recommendations = await get_recommendations(title_name='Режим дня и сон')
    msg = ''
    for i in recommendations['Режим дня и сон']:
        msg += f'{i["id"]}. {i["name"]}\n'

    await call.message.edit_text(text="Выберите рекомендации по <b>Режим дня и сон</b>:\n\n" + msg,
                                 reply_markup=await recommendations_keyboard_3([]))
    await FormStates.RECOMMENDATION_3.set()


async def process_recommendation_3(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()

    my_list = state_data.get("RECOMMENDATION_3", [])
    option = call.data.replace('recommendation_3_', '')

    if option in my_list:
        my_list.remove(option)
    else:
        my_list.append(option)

    await state.update_data(RECOMMENDATION_3=my_list)

    await call.message.edit_reply_markup(reply_markup=await recommendations_keyboard_3(my_list))


async def process_save_recommendation_3(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()

    try:
        await state.update_data(RECOMMENDATION_3=list(map(int, state_data['RECOMMENDATION_3'])))
    except KeyError:
        await state.update_data(RECOMMENDATION_3=[])

    recommendations = await get_recommendations(title_name='Активность')
    msg = ''
    for i in recommendations['Активность']:
        msg += f'{i["id"]}. {i["name"]}\n'

    await call.message.edit_text(text="Выберите рекомендации по <b>Активность</b>:\n\n" + msg,
                                 reply_markup=await recommendations_keyboard_4([]))
    await FormStates.RECOMMENDATION_4.set()


async def process_recommendation_4(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()

    my_list = state_data.get("RECOMMENDATION_4", [])
    option = call.data.replace('recommendation_4_', '')

    if option in my_list:
        my_list.remove(option)
    else:
        my_list.append(option)

    await state.update_data(RECOMMENDATION_4=my_list)

    await call.message.edit_reply_markup(reply_markup=await recommendations_keyboard_4(my_list))


async def process_save_recommendation_4(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()

    try:
        await state.update_data(RECOMMENDATION_4=list(map(int, state_data['RECOMMENDATION_4'])))
    except KeyError:
        await state.update_data(RECOMMENDATION_4=[])

    recommendations = await get_recommendations(title_name='Слизистые')
    msg = ''
    for i in recommendations['Слизистые']:
        msg += f'{i["id"]}. {i["name"]}\n'

    await call.message.edit_text(text="Выберите рекомендации по <b>Слизистые</b>:\n\n" + msg,
                                 reply_markup=await recommendations_keyboard_5([]))

    await FormStates.RECOMMENDATION_5.set()


async def process_recommendation_5(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()

    my_list = state_data.get("RECOMMENDATION_5", [])
    option = call.data.replace('recommendation_5_', '')

    if option in my_list:
        my_list.remove(option)
    else:
        my_list.append(option)

    await state.update_data(RECOMMENDATION_5=my_list)

    await call.message.edit_reply_markup(reply_markup=await recommendations_keyboard_5(my_list))


async def process_save_recommendation_5(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()

    try:
        await state.update_data(RECOMMENDATION_5=list(map(int, state_data['RECOMMENDATION_5'])))
    except KeyError:
        await state.update_data(RECOMMENDATION_5=[])

    recommendations = await get_recommendations(title_name='Кислотность и желчеотток')
    msg = ''
    for i in recommendations['Кислотность и желчеотток']:
        msg += f'{i["id"]}. {i["name"]}\n'

    await call.message.edit_text(text="Выберите рекомендации по <b>Кислотность и желчеотток</b>:\n\n" + msg,
                                 reply_markup=await recommendations_keyboard_6([]))
    await FormStates.RECOMMENDATION_6.set()


async def process_recommendation_6(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()

    my_list = state_data.get("RECOMMENDATION_6", [])
    option = call.data.replace('recommendation_6_', '')

    if option in my_list:
        my_list.remove(option)
    else:
        my_list.append(option)

    await state.update_data(RECOMMENDATION_6=my_list)

    await call.message.edit_reply_markup(reply_markup=await recommendations_keyboard_6(my_list))


async def process_save_recommendation_6(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()

    try:
        await state.update_data(RECOMMENDATION_6=list(map(int, state_data['RECOMMENDATION_6'])))
    except KeyError:
        await state.update_data(RECOMMENDATION_6=[])

    state_data = await state.get_data()
    recommendation_ids = []
    for key, value in state_data.items():
        if isinstance(value, list):
            recommendation_ids.extend(value)
    recommendations = await get_recommendations_by_ids(recommendation_ids)

    food_protocol_name = await get_protocol_by_id(int(state_data["food_protocol"]))
    await save_new_client(name=state_data["full_name"],
                          email=state_data["email"],
                          food_protocol_id=int(state_data["food_protocol"]),
                          food_protocol_name=food_protocol_name,
                          allergic=state_data["allergies"],
                          recommendations=recommendations,
                          recommendations_ids=recommendation_ids)

    if recommendations:
        rec = await setup_rec_data(recommendations)
    else:
        rec = 'Нет'
    await call.message.edit_text(f'Данные сохранены! \n'
                                 f'<b>ФИО:</b> {state_data["full_name"]}\n'
                                 f'<b>Email:</b> {state_data["email"]}\n'
                                 f'<b>Протокол питания:</b> {food_protocol_name}\n'
                                 f'<b>Аллергии:</b> {state_data["allergies"]}\n'
                                 f'<b>Рекомендации:</b> \n{rec}')

    await state.finish()
    await call.message.answer('Выберите действие:', reply_markup=await get_start_keyboard())


async def process_client_set_rec(call: types.CallbackQuery):
    recommendations = await get_recommendations(title_name='Работа со стрессом')
    msg = ''
    for i in recommendations['Работа со стрессом']:
        msg += f'{str(i["id"])}. {i["name"]}\n'

    await call.message.answer(text="Выберите рекомендации по <b>Работе со стрессом</b>:\n\n" + msg,
                              reply_markup=await recommendation_edit_keyboard_1([]))
    await FormStates.RECOMMENDATION_1.set()


async def process_edit_recs(call: types.CallbackQuery):
    recommendations = await get_recommendations(title_name='Работа со стрессом')
    msg = ''
    for i in recommendations['Работа со стрессом']:
        msg += f'{str(i["id"])}. {i["name"]}\n'
    await call.message.edit_text(text="Выберите рекомендации по <b>Работе со стрессом</b>:\n\n" + msg,
                                 reply_markup=await edit_recommendation_keyboard_1([]))
    await ClientFindChoice.RECOMMENDATION_1.set()


async def process_choose_recommendation_1(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    my_list = state_data.get("REC_1", [])
    option = call.data.replace('edit_rec_1_', '')

    if option in my_list:
        my_list.remove(option)
    else:
        my_list.append(option)

    await state.update_data(REC_1=my_list)
    await call.message.edit_reply_markup(reply_markup=await recommendation_edit_keyboard_1(my_list))


async def process_edit_choose_recommendation_1(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    my_list = state_data.get("REC_1", [])
    option = call.data.replace('rec_1_edit_', '')

    if option in my_list:
        my_list.remove(option)
    else:
        my_list.append(option)

    await state.update_data(REC_1=my_list)
    await call.message.edit_reply_markup(reply_markup=await edit_recommendation_keyboard_1(my_list))


async def process_edit_recommendation_1(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    try:
        await state.update_data(REC_1=list(map(int, state_data['REC_1'])))
    except KeyError:
        await state.update_data(REC_1=[])

    recommendations = await get_recommendations(title_name='Витамины')
    msg = ''
    for i in recommendations['Витамины']:
        msg += f'{i["id"]}. {i["name"]}\n'

    await call.message.edit_text(text="Выберите рекомендации по <b>Витаминам</b>:\n\n" + msg,
                                 reply_markup=await recommendation_edit_keyboard_2([]))
    await FormStates.RECOMMENDATION_2.set()


async def process_save_edit_recommendation_1(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    try:
        await state.update_data(REC_1=list(map(int, state_data['REC_1'])))
    except KeyError:
        await state.update_data(REC_1=[])

    recommendations = await get_recommendations(title_name='Витамины')
    msg = ''
    for i in recommendations['Витамины']:
        msg += f'{i["id"]}. {i["name"]}\n'

    await call.message.edit_text(text="Выберите рекомендации по <b>Витаминам</b>:\n\n" + msg,
                                 reply_markup=await edit_recommendation_keyboard_2([]))
    await ClientFindChoice.RECOMMENDATION_2.set()


async def process_choose_recommendation_2(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    my_list = state_data.get("REC_2", [])
    option = call.data.replace('edit_rec_2_', '')

    if option in my_list:
        my_list.remove(option)
    else:
        my_list.append(option)

    await state.update_data(REC_2=my_list)

    await call.message.edit_reply_markup(reply_markup=await recommendation_edit_keyboard_2(my_list))


async def process_edit_choose_recommendation_2(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    my_list = state_data.get("REC_2", [])
    option = call.data.replace('rec_2_edit_', '')

    if option in my_list:
        my_list.remove(option)
    else:
        my_list.append(option)

    await state.update_data(REC_2=my_list)

    await call.message.edit_reply_markup(reply_markup=await edit_recommendation_keyboard_2(my_list))


async def process_edit_recommendation_2(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()

    try:
        await state.update_data(REC_2=list(map(int, state_data['REC_2'])))
    except KeyError:
        await state.update_data(REC_2=[])

    recommendations = await get_recommendations(title_name='Режим дня и сон')
    msg = ''
    for i in recommendations['Режим дня и сон']:
        msg += f'{i["id"]}. {i["name"]}\n'

    await call.message.edit_text(text="Выберите рекомендации по <b>Режим дня и сон</b>:\n\n" + msg,
                                 reply_markup=await recommendation_edit_keyboard_3([]))
    await FormStates.RECOMMENDATION_3.set()


async def process_save_edit_recommendation_2(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()

    try:
        await state.update_data(REC_2=list(map(int, state_data['REC_2'])))
    except KeyError:
        await state.update_data(REC_2=[])

    recommendations = await get_recommendations(title_name='Режим дня и сон')
    msg = ''
    for i in recommendations['Режим дня и сон']:
        msg += f'{i["id"]}. {i["name"]}\n'

    await call.message.edit_text(text="Выберите рекомендации по <b>Режим дня и сон</b>:\n\n" + msg,
                                 reply_markup=await edit_recommendation_keyboard_3([]))
    await ClientFindChoice.RECOMMENDATION_3.set()


async def process_choose_recommendation_3(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    my_list = state_data.get("REC_3", [])
    option = call.data.replace('edit_rec_3_', '')

    if option in my_list:
        my_list.remove(option)
    else:
        my_list.append(option)

    await state.update_data(REC_3=my_list)
    await call.message.edit_reply_markup(reply_markup=await recommendation_edit_keyboard_3(my_list))


async def process_edit_choose_recommendation_3(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    my_list = state_data.get("REC_3", [])
    option = call.data.replace('rec_3_edit_', '')

    if option in my_list:
        my_list.remove(option)
    else:
        my_list.append(option)

    await state.update_data(REC_3=my_list)
    await call.message.edit_reply_markup(reply_markup=await edit_recommendation_keyboard_3(my_list))


async def process_edit_recommendation_3(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    try:
        await state.update_data(REC_3=list(map(int, state_data['REC_3'])))
    except KeyError:
        await state.update_data(REC_3=[])

    recommendations = await get_recommendations(title_name='Активность')
    msg = ''
    for i in recommendations['Активность']:
        msg += f'{i["id"]}. {i["name"]}\n'

    await call.message.edit_text(text="Выберите рекомендации по <b>Активность</b>:\n\n" + msg,
                                 reply_markup=await recommendation_edit_keyboard_4([]))
    await FormStates.RECOMMENDATION_4.set()


async def process_save_edit_recommendation_3(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    try:
        await state.update_data(REC_3=list(map(int, state_data['REC_3'])))
    except KeyError:
        await state.update_data(REC_3=[])

    recommendations = await get_recommendations(title_name='Активность')
    msg = ''
    for i in recommendations['Активность']:
        msg += f'{i["id"]}. {i["name"]}\n'

    await call.message.edit_text(text="Выберите рекомендации по <b>Активность</b>:\n\n" + msg,
                                 reply_markup=await edit_recommendation_keyboard_4([]))
    await ClientFindChoice.RECOMMENDATION_4.set()


async def process_choose_recommendation_4(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    my_list = state_data.get("REC_4", [])
    option = call.data.replace('edit_rec_4_', '')

    if option in my_list:
        my_list.remove(option)
    else:
        my_list.append(option)

    await state.update_data(REC_4=my_list)
    await call.message.edit_reply_markup(reply_markup=await recommendation_edit_keyboard_4(my_list))


async def process_edit_choose_recommendation_4(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    my_list = state_data.get("REC_4", [])
    option = call.data.replace('rec_4_edit_', '')

    if option in my_list:
        my_list.remove(option)
    else:
        my_list.append(option)

    await state.update_data(REC_4=my_list)
    await call.message.edit_reply_markup(reply_markup=await edit_recommendation_keyboard_4(my_list))


async def process_edit_recommendation_4(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    try:
        await state.update_data(REC_4=list(map(int, state_data['REC_4'])))
    except KeyError:
        await state.update_data(REC_4=[])

    recommendations = await get_recommendations(title_name='Слизистые')
    msg = ''
    for i in recommendations['Слизистые']:
        msg += f'{i["id"]}. {i["name"]}\n'

    await call.message.edit_text(text="Выберите рекомендации по <b>Слизистые</b>:\n\n" + msg,
                                 reply_markup=await recommendation_edit_keyboard_5([]))
    await FormStates.RECOMMENDATION_5.set()


async def process_save_edit_recommendation_4(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    try:
        await state.update_data(REC_4=list(map(int, state_data['REC_4'])))
    except KeyError:
        await state.update_data(REC_4=[])

    recommendations = await get_recommendations(title_name='Слизистые')
    msg = ''
    for i in recommendations['Слизистые']:
        msg += f'{i["id"]}. {i["name"]}\n'

    await call.message.edit_text(text="Выберите рекомендации по <b>Слизистые</b>:\n\n" + msg,
                                 reply_markup=await edit_recommendation_keyboard_5([]))
    await ClientFindChoice.RECOMMENDATION_5.set()


async def process_choose_recommendation_5(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    my_list = state_data.get("REC_5", [])
    option = call.data.replace('edit_rec_5_', '')

    if option in my_list:
        my_list.remove(option)
    else:
        my_list.append(option)

    await state.update_data(REC_5=my_list)
    await call.message.edit_reply_markup(reply_markup=await recommendation_edit_keyboard_5(my_list))


async def process_edit_choose_recommendation_5(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    my_list = state_data.get("REC_5", [])
    option = call.data.replace('rec_5_edit_', '')

    if option in my_list:
        my_list.remove(option)
    else:
        my_list.append(option)

    await state.update_data(REC_5=my_list)
    await call.message.edit_reply_markup(reply_markup=await edit_recommendation_keyboard_5(my_list))


async def process_edit_recommendation_5(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    try:
        await state.update_data(REC_5=list(map(int, state_data['REC_5'])))
    except KeyError:
        await state.update_data(REC_5=[])

    recommendations = await get_recommendations(title_name='Кислотность и желчеотток')
    msg = ''
    for i in recommendations['Кислотность и желчеотток']:
        msg += f'{i["id"]}. {i["name"]}\n'

    await call.message.edit_text(text="Выберите рекомендации по <b>Кислотность и желчеотток</b>:\n\n" + msg,
                                 reply_markup=await recommendation_edit_keyboard_6([]))
    await FormStates.RECOMMENDATION_6.set()


async def process_save_edit_recommendation_5(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    try:
        await state.update_data(REC_5=list(map(int, state_data['REC_5'])))
    except KeyError:
        await state.update_data(REC_5=[])

    recommendations = await get_recommendations(title_name='Кислотность и желчеотток')
    msg = ''
    for i in recommendations['Кислотность и желчеотток']:
        msg += f'{i["id"]}. {i["name"]}\n'

    await call.message.edit_text(text="Выберите рекомендации по <b>Кислотность и желчеотток</b>:\n\n" + msg,
                                 reply_markup=await edit_recommendation_keyboard_6([]))
    await ClientFindChoice.RECOMMENDATION_6.set()


async def process_choose_recommendation_6(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    my_list = state_data.get("REC_6", [])
    option = call.data.replace('edit_rec_6_', '')

    if option in my_list:
        my_list.remove(option)
    else:
        my_list.append(option)

    await state.update_data(REC_6=my_list)
    await call.message.edit_reply_markup(reply_markup=await recommendation_edit_keyboard_6(my_list))


async def process_edit_choose_recommendation_6(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    my_list = state_data.get("REC_6", [])
    option = call.data.replace('rec_6_edit_', '')

    if option in my_list:
        my_list.remove(option)
    else:
        my_list.append(option)

    await state.update_data(REC_6=my_list)
    await call.message.edit_reply_markup(reply_markup=await edit_recommendation_keyboard_6(my_list))


async def process_edit_recommendation_6(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()

    try:
        await state.update_data(REC_6=list(map(int, state_data['REC_6'])))
    except KeyError:
        await state.update_data(REC_6=[])

    state_data = await state.get_data()
    recommendation_ids = []
    for key, value in state_data.items():
        if isinstance(value, list):
            recommendation_ids.extend(value)

    recommendations = await get_recommendations_by_ids(recommendation_ids)

    await update_user_recommendations(user_id=state_data["chosen_user"]["id"],
                                      recommendations=recommendations,
                                      recommendations_ids=recommendation_ids)

    if recommendations:
        rec = await setup_rec_data(recommendations)
    else:
        rec = 'Нет'
    await call.message.edit_text(f'Рекомендации обновлены! \n'
                                 f'ФИО: {state_data["chosen_user"]["full_name"]}\n\n'
                                 f'Рекомендации: \n{rec}')

    await state.finish()
    await call.message.edit_text('Выберите действие:', reply_markup=await get_start_keyboard())


async def process_save_edit_recommendation_6(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()

    try:
        await state.update_data(REC_6=list(map(int, state_data['REC_6'])))
    except KeyError:
        await state.update_data(REC_6=[])

    state_data = await state.get_data()
    recommendation_ids = []
    for key, value in state_data.items():
        if isinstance(value, list):
            recommendation_ids.extend(value)

    recommendations = await get_recommendations_by_ids(recommendation_ids)

    await update_user_recommendations(user_id=state_data["chosen_user"]["id"],
                                      recommendations=recommendations,
                                      recommendations_ids=recommendation_ids)

    if recommendations:
        rec = await setup_rec_data(recommendations)
    else:
        rec = 'Нет'
    await call.message.edit_text(f'Рекомендации обновлены! \n\n'
                                 f'<b>ФИО:</b> {state_data["chosen_user"]["full_name"]}\n'
                                 f'<b>Email:</b> {state_data["chosen_user"]["email"]}\n'
                                 f'<b>Протокол питания:</b> {state_data["chosen_user"]["food_protocol_name"]}\n'
                                 f'<b>Аллергии:</b> {state_data["chosen_user"]["allergic"]}\n'
                                 f'<b>Рекомендации:</b> \n{rec}')

    await state.finish()
    await call.message.answer('Выберите действие:', reply_markup=await get_start_keyboard())


async def process_back_to_start_menu(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text('Выберите действие:', reply_markup=await get_start_keyboard())


async def process_back_to_clients_menu(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text('Выберите действие:', reply_markup=await get_clients_keyboard())


def register_callbacks(dp: Dispatcher):
    """Register bot callbacks and triggers."""
    # Start
    dp.register_callback_query_handler(process_start_callback_clients, lambda c: c.data == 'clients')
    dp.register_callback_query_handler(process_start_callback_menu, lambda c: c.data == 'menu')
    dp.register_callback_query_handler(process_start_callback_recommendations, lambda c: c.data == 'recommendations')

    dp.register_callback_query_handler(process_client_set_rec, lambda c: c.data == 'set_rec',
                                       state='*')
    dp.register_callback_query_handler(process_client_back, lambda c: c.data == 'back',
                                       state=ClientMakeRecommendationsChoice.choosing_user)

    # Clients
    dp.register_callback_query_handler(process_clients_callback_add, lambda c: c.data == 'add_client')
    dp.register_callback_query_handler(process_clients_callback_find, lambda c: c.data == 'find_client')
    dp.register_callback_query_handler(process_back_to_start_menu, lambda c: c.data == 'back_start', state='*')
    dp.register_callback_query_handler(process_back_to_clients_menu, lambda c: c.data == 'back_clients', state='*')

    # Find
    dp.register_callback_query_handler(process_clients_find_callback, lambda c: c.data.startswith('client_'), state='*')
    dp.register_callback_query_handler(process_client_edit_callback, lambda c: c.data == 'edit_client',
                                       state=ClientFindChoice.choosing_user)

    # Find - Remove
    dp.register_callback_query_handler(process_client_remove_callback, lambda c: c.data == 'remove_client',
                                       state=ClientFindChoice.choosing_user)
    dp.register_callback_query_handler(process_client_remove_yes_callback, lambda c: c.data == 'removal_yes',
                                       state=ClientFindChoice.choosing_user)
    dp.register_callback_query_handler(process_client_remove_no_callback, lambda c: c.data == 'removal_no',
                                       state=ClientFindChoice.choosing_user)

    dp.register_callback_query_handler(process_food_protocol, lambda c: c.data.startswith('protocol_'),
                                       state='*')
    dp.register_callback_query_handler(process_edit_food_protocol, lambda c: c.data.startswith('edit_protocol_'),
                                       state='*')

    # Set recommendations
    dp.register_callback_query_handler(process_recommendation_1, lambda c: c.data.startswith('recommendation_1_'),
                                       state='*')
    dp.register_callback_query_handler(process_save_recommendation_1, lambda c: c.data == 'save_rec1',
                                       state='*')
    dp.register_callback_query_handler(process_recommendation_2, lambda c: c.data.startswith('recommendation_2_'),
                                       state='*')
    dp.register_callback_query_handler(process_save_recommendation_2, lambda c: c.data == 'save_rec2',
                                       state='*')
    dp.register_callback_query_handler(process_recommendation_3, lambda c: c.data.startswith('recommendation_3_'),
                                       state='*')
    dp.register_callback_query_handler(process_save_recommendation_3, lambda c: c.data == 'save_rec3',
                                       state='*')
    dp.register_callback_query_handler(process_recommendation_4, lambda c: c.data.startswith('recommendation_4_'),
                                       state='*')
    dp.register_callback_query_handler(process_save_recommendation_4, lambda c: c.data == 'save_rec4',
                                       state='*')
    dp.register_callback_query_handler(process_recommendation_5, lambda c: c.data.startswith('recommendation_5_'),
                                       state='*')
    dp.register_callback_query_handler(process_save_recommendation_5, lambda c: c.data == 'save_rec5',
                                       state='*')
    dp.register_callback_query_handler(process_recommendation_6, lambda c: c.data.startswith('recommendation_6_'),
                                       state='*')
    dp.register_callback_query_handler(process_save_recommendation_6, lambda c: c.data == 'save_client',
                                       state='*')

    # Edit recommendations
    dp.register_callback_query_handler(process_choose_recommendation_1, lambda c: c.data.startswith('edit_rec_1_'),
                                       state='*')
    dp.register_callback_query_handler(process_edit_recommendation_1, lambda c: c.data == 'rec1_save',
                                       state='*')
    dp.register_callback_query_handler(process_choose_recommendation_2, lambda c: c.data.startswith('edit_rec_2_'),
                                       state='*')
    dp.register_callback_query_handler(process_edit_recommendation_2, lambda c: c.data == 'rec2_save',
                                       state='*')
    dp.register_callback_query_handler(process_choose_recommendation_3, lambda c: c.data.startswith('edit_rec_3_'),
                                       state='*')
    dp.register_callback_query_handler(process_edit_recommendation_3, lambda c: c.data == 'rec3_save',
                                       state='*')
    dp.register_callback_query_handler(process_choose_recommendation_4, lambda c: c.data.startswith('edit_rec_4_'),
                                       state='*')
    dp.register_callback_query_handler(process_edit_recommendation_4, lambda c: c.data == 'rec4_save',
                                       state='*')
    dp.register_callback_query_handler(process_choose_recommendation_5, lambda c: c.data.startswith('edit_rec_5_'),
                                       state='*')
    dp.register_callback_query_handler(process_edit_recommendation_5, lambda c: c.data == 'rec5_save',
                                       state='*')
    dp.register_callback_query_handler(process_choose_recommendation_6, lambda c: c.data.startswith('edit_rec_6_'),
                                       state='*')
    dp.register_callback_query_handler(process_edit_recommendation_6, lambda c: c.data == 'rec6_save',
                                       state='*')

    # Edit recs in profile settings
    dp.register_callback_query_handler(process_edit_choose_recommendation_1, lambda c: c.data.startswith('rec_1_edit_'),
                                       state='*')
    dp.register_callback_query_handler(process_save_edit_recommendation_1, lambda c: c.data == '1rec_save',
                                       state='*')
    dp.register_callback_query_handler(process_edit_choose_recommendation_2, lambda c: c.data.startswith('rec_2_edit_'),
                                       state='*')
    dp.register_callback_query_handler(process_save_edit_recommendation_2, lambda c: c.data == '2rec_save',
                                       state='*')
    dp.register_callback_query_handler(process_edit_choose_recommendation_3, lambda c: c.data.startswith('rec_3_edit_'),
                                       state='*')
    dp.register_callback_query_handler(process_save_edit_recommendation_3, lambda c: c.data == '3rec_save',
                                       state='*')
    dp.register_callback_query_handler(process_edit_choose_recommendation_4, lambda c: c.data.startswith('rec_4_edit_'),
                                       state='*')
    dp.register_callback_query_handler(process_save_edit_recommendation_4, lambda c: c.data == '4rec_save',
                                       state='*')
    dp.register_callback_query_handler(process_edit_choose_recommendation_5, lambda c: c.data.startswith('rec_5_edit_'),
                                       state='*')
    dp.register_callback_query_handler(process_save_edit_recommendation_5, lambda c: c.data == '5rec_save',
                                       state='*')
    dp.register_callback_query_handler(process_edit_choose_recommendation_6, lambda c: c.data.startswith('rec_6_edit_'),
                                       state='*')
    dp.register_callback_query_handler(process_save_edit_recommendation_6, lambda c: c.data == '6rec_save',
                                       state='*')

    # Editing selected fields
    dp.register_callback_query_handler(process_edit_name, lambda c: c.data == 'edit_name',
                                       state=ClientFindChoice.choosing_user)
    dp.register_callback_query_handler(process_edit_email, lambda c: c.data == 'edit_mail',
                                       state=ClientFindChoice.choosing_user)
    dp.register_callback_query_handler(process_edit_food, lambda c: c.data == 'edit_food',
                                       state=ClientFindChoice.choosing_user)
    dp.register_callback_query_handler(process_edit_allergic, lambda c: c.data == 'edit_allergic',
                                       state=ClientFindChoice.choosing_user)
    dp.register_callback_query_handler(process_edit_recs, lambda c: c.data == 'recs_edit',
                                       state=ClientFindChoice.choosing_user)

    # Menu keyboard processing
    dp.register_callback_query_handler(process_generate_pictures, lambda c: c.data == 'gen_pic',
                                       state='*')
    dp.register_callback_query_handler(process_edit_menu, lambda c: c.data == 'edit_menu',
                                       state='*')
    dp.register_callback_query_handler(process_back_menu, lambda c: c.data == 'back_menu',
                                       state='*')
