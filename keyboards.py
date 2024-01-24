from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from db import get_food_titles, get_recommendations, get_clients_data


async def get_clients_keyboard():
    """Notification settings keyboard creation."""
    keyboard = InlineKeyboardMarkup(row_width=1)
    btn_add_client = InlineKeyboardButton('Добавить нового клиента', callback_data='add_client')
    btn_find_client = InlineKeyboardButton('Найти клиента', callback_data='find_client')
    btn_back = InlineKeyboardButton('⬅️ Назад', callback_data='back_start')
    keyboard.add(btn_add_client, btn_find_client, btn_back)
    return keyboard


async def get_reply_bot():
    keyboard = InlineKeyboardMarkup(row_width=1)
    btn_find_client = InlineKeyboardButton('Найти клиента', switch_inline_query_current_chat="")
    btn_back = InlineKeyboardButton('⬅️ Назад', callback_data='back_start')
    keyboard.add(btn_find_client, btn_back)
    return keyboard


async def get_reply_bot_clients():
    keyboard = InlineKeyboardMarkup(row_width=1)
    btn_find_client = InlineKeyboardButton('Найти клиента', switch_inline_query_current_chat="")
    btn_back = InlineKeyboardButton('⬅️ Назад', callback_data='back_clients')
    keyboard.add(btn_find_client, btn_back)
    return keyboard


async def get_start_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    btn_clients = InlineKeyboardButton('Список клиентов', callback_data='clients')
    btn_menu = InlineKeyboardButton('Сформировать меню', callback_data='menu')
    btn_recommendations = InlineKeyboardButton('Сформировать рекомендации', callback_data='recommendations')
    btn_receipt = InlineKeyboardButton('Сформировать рецепт к блюду', callback_data='receipt')

    keyboard.add(btn_clients, btn_menu, btn_recommendations, btn_receipt)

    return keyboard


async def get_food_protocols_keyboard():
    keyboard = InlineKeyboardMarkup()
    protocols = await get_food_titles()
    for protocol_id, protocol_title in protocols.items():
        keyboard.add(InlineKeyboardButton(protocol_title, callback_data=f'protocol_{protocol_id}'))
    return keyboard


async def get_edit_food_protocols_keyboard():
    keyboard = InlineKeyboardMarkup()
    protocols = await get_food_titles()
    for protocol_id, protocol_title in protocols.items():
        keyboard.add(InlineKeyboardButton(protocol_title, callback_data=f'edit_protocol_{protocol_id}'))
    return keyboard


async def recommendations_keyboard_1(user_data):
    keyboard = InlineKeyboardMarkup(row_width=3)
    recommendations = await get_recommendations('Работа со стрессом')

    on = '✅ '
    off = '❌ '

    buttons = []
    for option in recommendations['Работа со стрессом']:
        button_text = f"{on if str(option['id']) in user_data else off}{option['id']}"
        button = InlineKeyboardButton(button_text, callback_data=f'recommendation_1_{option["id"]}')
        buttons.append(button)

    column1 = buttons[:len(buttons) // 3]
    column2 = buttons[len(buttons) // 3: 2 * len(buttons) // 3]
    column3 = buttons[2 * len(buttons) // 3:]

    for btn1, btn2, btn3 in zip(column1, column2, column3):
        keyboard.add(btn1, btn2, btn3)

    save_button = InlineKeyboardButton(text='Сохранить', callback_data='save_rec1')
    keyboard.add(save_button)

    return keyboard


async def recommendations_keyboard_2(user_data):
    keyboard = InlineKeyboardMarkup(row_width=3)
    recommendations = await get_recommendations('Витамины')

    on = '✅ '
    off = '❌ '

    buttons = []
    for option in recommendations['Витамины']:
        button_text = f"{on if str(option['id']) in user_data else off}{option['id']}"
        button = InlineKeyboardButton(button_text, callback_data=f'recommendation_2_{option["id"]}')
        keyboard.add(button)

    column1 = buttons[:len(buttons) // 3]
    column2 = buttons[len(buttons) // 3: 2 * len(buttons) // 3]
    column3 = buttons[2 * len(buttons) // 3:]

    for btn1, btn2, btn3 in zip(column1, column2, column3):
        keyboard.add(btn1, btn2, btn3)

    save_button = InlineKeyboardButton(text='Сохранить', callback_data='save_rec2')
    keyboard.add(save_button)

    return keyboard


async def recommendations_keyboard_3(user_data):
    keyboard = InlineKeyboardMarkup(row_width=3)
    recommendations = await get_recommendations('Режим дня и сон')

    on = '✅ '
    off = '❌ '

    buttons = []
    for option in recommendations['Режим дня и сон']:
        button_text = f"{on if str(option['id']) in user_data else off}{option['id']}"
        button = InlineKeyboardButton(button_text, callback_data=f'recommendation_3_{option["id"]}')
        keyboard.add(button)

    column1 = buttons[:len(buttons) // 3]
    column2 = buttons[len(buttons) // 3: 2 * len(buttons) // 3]
    column3 = buttons[2 * len(buttons) // 3:]

    for btn1, btn2, btn3 in zip(column1, column2, column3):
        keyboard.add(btn1, btn2, btn3)

    save_button = InlineKeyboardButton(text='Сохранить', callback_data='save_rec3')
    keyboard.add(save_button)

    return keyboard


async def recommendations_keyboard_4(user_data):
    keyboard = InlineKeyboardMarkup(row_width=3)
    recommendations = await get_recommendations('Активность')

    on = '✅ '
    off = '❌ '

    buttons = []
    for option in recommendations['Активность']:
        button_text = f"{on if str(option['id']) in user_data else off}{option['id']}"
        button = InlineKeyboardButton(button_text, callback_data=f'recommendation_4_{option["id"]}')
        keyboard.add(button)

    column1 = buttons[:len(buttons) // 3]
    column2 = buttons[len(buttons) // 3: 2 * len(buttons) // 3]
    column3 = buttons[2 * len(buttons) // 3:]

    for btn1, btn2, btn3 in zip(column1, column2, column3):
        keyboard.add(btn1, btn2, btn3)

    save_button = InlineKeyboardButton(text='Сохранить', callback_data='save_rec4')
    keyboard.add(save_button)

    return keyboard


async def recommendations_keyboard_5(user_data):
    keyboard = InlineKeyboardMarkup(row_width=3)
    recommendations = await get_recommendations('Слизистые')

    on = '✅ '
    off = '❌ '

    buttons = []
    for option in recommendations['Слизистые']:
        button_text = f"{on if str(option['id']) in user_data else off}{option['id']}"
        button = InlineKeyboardButton(button_text, callback_data=f'recommendation_5_{option["id"]}')
        keyboard.add(button)

    column1 = buttons[:len(buttons) // 3]
    column2 = buttons[len(buttons) // 3: 2 * len(buttons) // 3]
    column3 = buttons[2 * len(buttons) // 3:]

    for btn1, btn2, btn3 in zip(column1, column2, column3):
        keyboard.add(btn1, btn2, btn3)

    save_button = InlineKeyboardButton(text='Сохранить', callback_data='save_rec5')
    keyboard.add(save_button)

    return keyboard


async def recommendations_keyboard_6(user_data):
    keyboard = InlineKeyboardMarkup(row_width=3)
    recommendations = await get_recommendations('Кислотность и желчеотток')

    on = '✅ '
    off = '❌ '

    buttons = []
    for option in recommendations['Кислотность и желчеотток']:
        button_text = f"{on if str(option['id']) in user_data else off}{option['id']}"
        button = InlineKeyboardButton(button_text, callback_data=f'recommendation_6_{option["id"]}')
        keyboard.add(button)

    column1 = buttons[:len(buttons) // 3]
    column2 = buttons[len(buttons) // 3: 2 * len(buttons) // 3]
    column3 = buttons[2 * len(buttons) // 3:]

    for btn1, btn2, btn3 in zip(column1, column2, column3):
        keyboard.add(btn1, btn2, btn3)

    save_button = InlineKeyboardButton(text='Сохранить', callback_data='save_client')
    keyboard.add(save_button)

    return keyboard


async def get_clients_list_keyboard():
    keyboard = InlineKeyboardMarkup()
    clients = await get_clients_data()
    for client in clients:
        keyboard.add(InlineKeyboardButton(client['full_name'], callback_data=f'client_{str(client["id"])}'))
    btn_back = InlineKeyboardButton('⬅️ Назад', callback_data='back_clients')
    keyboard.add(btn_back)
    return keyboard


async def get_set_recommendations_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    btn_set = InlineKeyboardButton('Задать рекомендации', callback_data='set_rec')
    btn_back = InlineKeyboardButton('⬅️ Назад', callback_data='back_start')

    keyboard.add(btn_set, btn_back)

    return keyboard


async def get_menu_settings_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    btn_gen = InlineKeyboardButton('Cгенерировать фото по меню', callback_data='gen_pic')
    btn_edit_menu = InlineKeyboardButton('Редактировать меню', callback_data='edit_menu')
    btn_back = InlineKeyboardButton('⬅️ Назад', callback_data='back_start')

    keyboard.add(btn_gen, btn_edit_menu, btn_back)

    return keyboard


async def get_back_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    btn_back = InlineKeyboardButton('⬅️ Назад', callback_data='back_start')

    keyboard.add(btn_back)

    return keyboard


async def get_clients_list_keyboard_rec():
    keyboard = InlineKeyboardMarkup()
    clients = await get_clients_data()
    for client in clients:
        keyboard.add(InlineKeyboardButton(client['full_name'], callback_data=f'clients_rec_{str(client["id"])}'))
    btn_back = InlineKeyboardButton('⬅️ Назад', callback_data='back_start')
    keyboard.add(btn_back)
    return keyboard


async def get_clients_list_keyboard_menu():
    keyboard = InlineKeyboardMarkup()
    clients = await get_clients_data()
    for client in clients:
        keyboard.add(InlineKeyboardButton(client['full_name'], callback_data=f'menu_clients_{str(client["id"])}'))
    btn_back = InlineKeyboardButton('⬅️ Назад', callback_data='back_start')
    keyboard.add(btn_back)
    return keyboard


async def get_clients_settings_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    btn_edit = InlineKeyboardButton('Редактировать данные клиента', callback_data='edit_client')
    btn_delete = InlineKeyboardButton('Удалить клиента', callback_data='remove_client')
    btn_back = InlineKeyboardButton('⬅️ Назад', callback_data='back_clients')

    keyboard.add(btn_edit, btn_delete, btn_back)

    return keyboard


async def get_edit_list_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    btn_edit_name = InlineKeyboardButton('ФИО', callback_data='edit_name')
    btn_edit_mail = InlineKeyboardButton('Email', callback_data='edit_mail')
    btn_edit_food = InlineKeyboardButton('Протокол питания', callback_data='edit_food')
    btn_edit_allergic = InlineKeyboardButton('Аллергии', callback_data='edit_allergic')
    btn_edit_rec = InlineKeyboardButton('Рекомендации', callback_data='recs_edit')
    btn_back = InlineKeyboardButton('⬅️ Назад', callback_data='back_clients')

    keyboard.add(btn_edit_name, btn_edit_mail, btn_edit_food, btn_edit_allergic, btn_edit_rec, btn_back)

    return keyboard


async def get_remove_question_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    btn_edit = InlineKeyboardButton('Да', callback_data='removal_yes')
    btn_delete = InlineKeyboardButton('Нет', callback_data='removal_no')

    keyboard.add(btn_edit, btn_delete)

    return keyboard


async def recommendation_edit_keyboard_1(user_data):
    keyboard = InlineKeyboardMarkup(row_width=3)
    recommendations = await get_recommendations('Работа со стрессом')

    on = '✅ '
    off = '❌ '

    buttons = []
    for option in recommendations['Работа со стрессом']:
        button_text = f"{on if str(option['id']) in user_data else off}{option['id']}"
        button = InlineKeyboardButton(button_text, callback_data=f'edit_rec_1_{option["id"]}')
        buttons.append(button)

    column1 = buttons[:len(buttons) // 3]
    column2 = buttons[len(buttons) // 3: 2 * len(buttons) // 3]
    column3 = buttons[2 * len(buttons) // 3:]

    for btn1, btn2, btn3 in zip(column1, column2, column3):
        keyboard.add(btn1, btn2, btn3)

    save_button = InlineKeyboardButton(text='Сохранить', callback_data='rec1_save')
    keyboard.add(save_button)

    return keyboard


async def edit_recommendation_keyboard_1(user_data):
    keyboard = InlineKeyboardMarkup(row_width=3)
    recommendations = await get_recommendations('Работа со стрессом')

    on = '✅ '
    off = '❌ '

    buttons = []
    for option in recommendations['Работа со стрессом']:
        button_text = f"{on if str(option['id']) in user_data else off}{option['id']}"
        button = InlineKeyboardButton(button_text, callback_data=f'rec_1_edit_{option["id"]}')
        buttons.append(button)

    column1 = buttons[:len(buttons) // 3]
    column2 = buttons[len(buttons) // 3: 2 * len(buttons) // 3]
    column3 = buttons[2 * len(buttons) // 3:]

    for btn1, btn2, btn3 in zip(column1, column2, column3):
        keyboard.add(btn1, btn2, btn3)

    save_button = InlineKeyboardButton(text='Сохранить', callback_data='1rec_save')
    keyboard.add(save_button)

    return keyboard


async def recommendation_edit_keyboard_2(user_data):
    keyboard = InlineKeyboardMarkup(row_width=3)
    recommendations = await get_recommendations('Витамины')

    on = '✅ '
    off = '❌ '

    buttons = []
    for option in recommendations['Витамины']:
        button_text = f"{on if str(option['id']) in user_data else off}{option['id']}"
        button = InlineKeyboardButton(button_text, callback_data=f'edit_rec_2_{option["id"]}')
        keyboard.add(button)

    column1 = buttons[:len(buttons) // 3]
    column2 = buttons[len(buttons) // 3: 2 * len(buttons) // 3]
    column3 = buttons[2 * len(buttons) // 3:]

    for btn1, btn2, btn3 in zip(column1, column2, column3):
        keyboard.add(btn1, btn2, btn3)

    save_button = InlineKeyboardButton(text='Сохранить', callback_data='rec2_save')
    keyboard.add(save_button)

    return keyboard


async def edit_recommendation_keyboard_2(user_data):
    keyboard = InlineKeyboardMarkup(row_width=3)
    recommendations = await get_recommendations('Витамины')

    on = '✅ '
    off = '❌ '

    buttons = []
    for option in recommendations['Витамины']:
        button_text = f"{on if str(option['id']) in user_data else off}{option['id']}"
        button = InlineKeyboardButton(button_text, callback_data=f'rec_2_edit_{option["id"]}')
        keyboard.add(button)

    column1 = buttons[:len(buttons) // 3]
    column2 = buttons[len(buttons) // 3: 2 * len(buttons) // 3]
    column3 = buttons[2 * len(buttons) // 3:]

    for btn1, btn2, btn3 in zip(column1, column2, column3):
        keyboard.add(btn1, btn2, btn3)

    save_button = InlineKeyboardButton(text='Сохранить', callback_data='2rec_save')
    keyboard.add(save_button)

    return keyboard


async def recommendation_edit_keyboard_3(user_data):
    keyboard = InlineKeyboardMarkup(row_width=3)
    recommendations = await get_recommendations('Режим дня и сон')

    on = '✅ '
    off = '❌ '

    buttons = []
    for option in recommendations['Режим дня и сон']:
        button_text = f"{on if str(option['id']) in user_data else off}{option['id']}"
        button = InlineKeyboardButton(button_text, callback_data=f'edit_rec_3_{option["id"]}')
        keyboard.add(button)

    column1 = buttons[:len(buttons) // 3]
    column2 = buttons[len(buttons) // 3: 2 * len(buttons) // 3]
    column3 = buttons[2 * len(buttons) // 3:]

    for btn1, btn2, btn3 in zip(column1, column2, column3):
        keyboard.add(btn1, btn2, btn3)

    save_button = InlineKeyboardButton(text='Сохранить', callback_data='rec3_save')
    keyboard.add(save_button)

    return keyboard


async def edit_recommendation_keyboard_3(user_data):
    keyboard = InlineKeyboardMarkup(row_width=3)
    recommendations = await get_recommendations('Режим дня и сон')

    on = '✅ '
    off = '❌ '

    buttons = []
    for option in recommendations['Режим дня и сон']:
        button_text = f"{on if str(option['id']) in user_data else off}{option['id']}"
        button = InlineKeyboardButton(button_text, callback_data=f'rec_3_edit_{option["id"]}')
        keyboard.add(button)

    column1 = buttons[:len(buttons) // 3]
    column2 = buttons[len(buttons) // 3: 2 * len(buttons) // 3]
    column3 = buttons[2 * len(buttons) // 3:]

    for btn1, btn2, btn3 in zip(column1, column2, column3):
        keyboard.add(btn1, btn2, btn3)

    save_button = InlineKeyboardButton(text='Сохранить', callback_data='3rec_save')
    keyboard.add(save_button)

    return keyboard


async def recommendation_edit_keyboard_4(user_data):
    keyboard = InlineKeyboardMarkup(row_width=3)
    recommendations = await get_recommendations('Активность')

    on = '✅ '
    off = '❌ '

    buttons = []
    for option in recommendations['Активность']:
        button_text = f"{on if str(option['id']) in user_data else off}{option['id']}"
        button = InlineKeyboardButton(button_text, callback_data=f'edit_rec_4_{option["id"]}')
        keyboard.add(button)

    column1 = buttons[:len(buttons) // 3]
    column2 = buttons[len(buttons) // 3: 2 * len(buttons) // 3]
    column3 = buttons[2 * len(buttons) // 3:]

    for btn1, btn2, btn3 in zip(column1, column2, column3):
        keyboard.add(btn1, btn2, btn3)

    save_button = InlineKeyboardButton(text='Сохранить', callback_data='rec4_save')
    keyboard.add(save_button)

    return keyboard


async def edit_recommendation_keyboard_4(user_data):
    keyboard = InlineKeyboardMarkup(row_width=3)
    recommendations = await get_recommendations('Активность')

    on = '✅ '
    off = '❌ '

    buttons = []
    for option in recommendations['Активность']:
        button_text = f"{on if str(option['id']) in user_data else off}{option['id']}"
        button = InlineKeyboardButton(button_text, callback_data=f'rec_4_edit_{option["id"]}')
        keyboard.add(button)

    column1 = buttons[:len(buttons) // 3]
    column2 = buttons[len(buttons) // 3: 2 * len(buttons) // 3]
    column3 = buttons[2 * len(buttons) // 3:]

    for btn1, btn2, btn3 in zip(column1, column2, column3):
        keyboard.add(btn1, btn2, btn3)

    save_button = InlineKeyboardButton(text='Сохранить', callback_data='4rec_save')
    keyboard.add(save_button)

    return keyboard


async def recommendation_edit_keyboard_5(user_data):
    keyboard = InlineKeyboardMarkup(row_width=3)
    recommendations = await get_recommendations('Слизистые')

    on = '✅ '
    off = '❌ '

    buttons = []
    for option in recommendations['Слизистые']:
        button_text = f"{on if str(option['id']) in user_data else off}{option['id']}"
        button = InlineKeyboardButton(button_text, callback_data=f'edit_rec_5_{option["id"]}')
        keyboard.add(button)

    column1 = buttons[:len(buttons) // 3]
    column2 = buttons[len(buttons) // 3: 2 * len(buttons) // 3]
    column3 = buttons[2 * len(buttons) // 3:]

    for btn1, btn2, btn3 in zip(column1, column2, column3):
        keyboard.add(btn1, btn2, btn3)

    save_button = InlineKeyboardButton(text='Сохранить', callback_data='rec5_save')
    keyboard.add(save_button)

    return keyboard


async def edit_recommendation_keyboard_5(user_data):
    keyboard = InlineKeyboardMarkup(row_width=3)
    recommendations = await get_recommendations('Слизистые')

    on = '✅ '
    off = '❌ '

    buttons = []
    for option in recommendations['Слизистые']:
        button_text = f"{on if str(option['id']) in user_data else off}{option['id']}"
        button = InlineKeyboardButton(button_text, callback_data=f'rec_5_edit_{option["id"]}')
        keyboard.add(button)

    column1 = buttons[:len(buttons) // 3]
    column2 = buttons[len(buttons) // 3: 2 * len(buttons) // 3]
    column3 = buttons[2 * len(buttons) // 3:]

    for btn1, btn2, btn3 in zip(column1, column2, column3):
        keyboard.add(btn1, btn2, btn3)

    save_button = InlineKeyboardButton(text='Сохранить', callback_data='5rec_save')
    keyboard.add(save_button)

    return keyboard


async def recommendation_edit_keyboard_6(user_data):
    keyboard = InlineKeyboardMarkup(row_width=3)
    recommendations = await get_recommendations('Кислотность и желчеотток')

    on = '✅ '
    off = '❌ '

    buttons = []
    for option in recommendations['Кислотность и желчеотток']:
        button_text = f"{on if str(option['id']) in user_data else off}{option['id']}"
        button = InlineKeyboardButton(button_text, callback_data=f'edit_rec_6_{option["id"]}')
        keyboard.add(button)

    column1 = buttons[:len(buttons) // 3]
    column2 = buttons[len(buttons) // 3: 2 * len(buttons) // 3]
    column3 = buttons[2 * len(buttons) // 3:]

    for btn1, btn2, btn3 in zip(column1, column2, column3):
        keyboard.add(btn1, btn2, btn3)

    save_button = InlineKeyboardButton(text='Сохранить', callback_data='rec6_save')
    keyboard.add(save_button)

    return keyboard


async def edit_recommendation_keyboard_6(user_data):
    keyboard = InlineKeyboardMarkup(row_width=3)
    recommendations = await get_recommendations('Кислотность и желчеотток')

    on = '✅ '
    off = '❌ '

    buttons = []
    for option in recommendations['Кислотность и желчеотток']:
        button_text = f"{on if str(option['id']) in user_data else off}{option['id']}"
        button = InlineKeyboardButton(button_text, callback_data=f'rec_6_edit_{option["id"]}')
        keyboard.add(button)

    column1 = buttons[:len(buttons) // 3]
    column2 = buttons[len(buttons) // 3: 2 * len(buttons) // 3]
    column3 = buttons[2 * len(buttons) // 3:]

    for btn1, btn2, btn3 in zip(column1, column2, column3):
        keyboard.add(btn1, btn2, btn3)

    save_button = InlineKeyboardButton(text='Сохранить', callback_data='6rec_save')
    keyboard.add(save_button)

    return keyboard
