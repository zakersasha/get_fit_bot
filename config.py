"""Service configuration."""
import os

from dotenv import load_dotenv

load_dotenv()


class Config(object):
    """Project main config"""
    TOKEN = os.environ.get('TOKEN')
    NEW_CLIENT = {}
    RECOMMENDATIONS_CHOICES = []
    CLIENT_ID_TO_DELETE = ''

    DB_NAME = os.environ.get('DB_NAME')
    DB_USERNAME = os.environ.get('DB_USERNAME')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_HOST = os.environ.get('DB_HOST')
    DB_PORT = os.environ.get('DB_PORT')
