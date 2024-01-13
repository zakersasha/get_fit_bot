"""Service configuration."""
import os
import sys

from dotenv import load_dotenv

load_dotenv()


class Config(object):
    """Project main config"""
    TOKEN = os.environ.get('TOKEN')
    RUNNER_PATH = getattr(sys.modules['__main__'], '__file__')
    ROOT_PATH = os.path.abspath(os.path.dirname(RUNNER_PATH))

    IMAGES_PATH = os.path.join(ROOT_PATH, 'images')
    ZIP_PATH = os.path.join(ROOT_PATH, 'images.zip')

    DB_NAME = os.environ.get('DB_NAME')
    DB_USERNAME = os.environ.get('DB_USERNAME')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_HOST = os.environ.get('DB_HOST')
    DB_PORT = os.environ.get('DB_PORT')

    NO_ANSWER = ['no', 'net', 'нет', 'NO', 'No', 'Нет', 'Отсутствуют', 'Отсутствует', 'отсутствуют', 'отсутствует', '-',
                 '0', 'none', 'nope', 'None', 'Nope', 'not']

    CATALOG_ID = os.environ.get('CATALOG_ID')
    API_KEY_ID = os.environ.get('API_KEY_ID')
    API_SECRET = os.environ.get('API_SECRET')

    FUSION_KEY = os.environ.get('FUSION_KEY')
    FUSION_SECRET = os.environ.get('FUSION_SECRET')
