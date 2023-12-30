"""Service configuration."""
import os

from dotenv import load_dotenv

load_dotenv()


class Config(object):
    """Project main config"""
    TOKEN = os.environ.get('TOKEN')

    DB_NAME = os.environ.get('DB_NAME')
    DB_USERNAME = os.environ.get('DB_USERNAME')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_HOST = os.environ.get('DB_HOST')
    DB_PORT = os.environ.get('DB_PORT')

    NO_ANSWER = ['no', 'net', 'нет', 'NO', 'No', 'Нет', 'Отсутствуют', 'Отсутствует', 'отсутствуют', 'отсутствует', '-']

    CATALOG_ID = os.environ.get('CATALOG_ID')
    API_KEY_ID = os.environ.get('API_KEY_ID')
    API_SECRET = os.environ.get('API_SECRET')
