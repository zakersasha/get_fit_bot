from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from db import get_food_titles, get_recommendations, get_clients_data


def get_clients_keyboard():
    """Notification settings keyboard creation."""
    keyboard = InlineKeyboardMarkup(row_width=1)
    btn_add_client = InlineKeyboardButton('Добавить нового клиента', callback_data='add_client')
    btn_find_client = InlineKeyboardButton('Найти клиента', callback_data='find_client')

    keyboard.add(btn_add_client, btn_find_client)

    return keyboard


def get_start_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    btn_clients = InlineKeyboardButton('Список клиентов', callback_data='clients')
    btn_menu = InlineKeyboardButton('Сформировать меню', callback_data='menu')
    btn_recommendations = InlineKeyboardButton('Сформировать рекомендации', callback_data='recommendations')

    keyboard.add(btn_clients, btn_menu, btn_recommendations)

    return keyboard


def get_food_protocols_keyboard():
    keyboard = InlineKeyboardMarkup()
    protocols = get_food_titles()
    for protocol_id, protocol_title in protocols.items():
        keyboard.add(InlineKeyboardButton(protocol_title, callback_data=f'protocol_{protocol_id}'))
    return keyboard


def recommendations_keyboard_1(user_data):
    keyboard = InlineKeyboardMarkup(row_width=3)
    recommendations = get_recommendations('Работа со стрессом')

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


def recommendations_keyboard_2(user_data):
    keyboard = InlineKeyboardMarkup(row_width=3)
    recommendations = get_recommendations('Витамины')

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


def recommendations_keyboard_3(user_data):
    keyboard = InlineKeyboardMarkup(row_width=3)
    recommendations = get_recommendations('Режим дня и сон')

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


def recommendations_keyboard_4(user_data):
    keyboard = InlineKeyboardMarkup(row_width=3)
    recommendations = get_recommendations('Активность')

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


def recommendations_keyboard_5(user_data):
    keyboard = InlineKeyboardMarkup(row_width=3)
    recommendations = get_recommendations('Слизистые')

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


def recommendations_keyboard_6(user_data):
    keyboard = InlineKeyboardMarkup(row_width=3)
    recommendations = get_recommendations('Кислотность и желчеотток')

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


def get_clients_list_keyboard():
    keyboard = InlineKeyboardMarkup()
    clients = get_clients_data()
    for client in clients:
        keyboard.add(InlineKeyboardButton(client['full_name'], callback_data=f'client_{str(client["id"])}'))
    return keyboard


def get_clients_settings_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    btn_edit = InlineKeyboardButton('Редактировать данные клиента', callback_data='edit_client')
    btn_delete = InlineKeyboardButton('Удалить клиента', callback_data='remove_client')

    keyboard.add(btn_edit, btn_delete)

    return keyboard


def get_remove_question_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    btn_edit = InlineKeyboardButton('Да', callback_data='removal_yes')
    btn_delete = InlineKeyboardButton('Нет', callback_data='removal_no')

    keyboard.add(btn_edit, btn_delete)

    return keyboard
