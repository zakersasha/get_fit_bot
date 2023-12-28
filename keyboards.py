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


def get_recommendations_keyboard(user_data):
    keyboard = InlineKeyboardMarkup(row_width=1)
    recommendations = get_recommendations()

    on = '✅ '
    off = '❌ '

    for option_id, option_name in recommendations.items():
        button_text = f"{on if str(option_id) in user_data else off}{option_name}"
        button = InlineKeyboardButton(button_text, callback_data=f'recommendation_{option_id}')
        keyboard.add(button)

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
