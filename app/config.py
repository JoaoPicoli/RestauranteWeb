import os
from datetime import timedelta


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'troque_esta_chave')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REMEMBER_COOKIE_DURATION = timedelta(days=7)
    MAX_OPEN_COMANDAS_PER_CLIENT = int(os.environ.get('MAX_OPEN_COMANDAS_PER_CLIENT', 3))