"""Configuration parameters of the flask app"""
import os
import configparser
from api.srlm.definitions import ROOT_DIR


config = configparser.ConfigParser()
config.read(os.path.join(ROOT_DIR, 'config', 'mail.config'))
mailing_list = config['MAIL']['MailingList'].split(', ')

mysql_user = os.getenv('MYSQL_USER')
mysql_pass = os.getenv('MYSQL_PASS')
mysql_host = os.getenv('MYSQL_HOST')
mysql_port = int(os.getenv('MYSQL_PORT'))

base_db_url = f"mysql+pymysql://{mysql_user}:{mysql_pass}@{mysql_host}:{mysql_port}/"
league_manager_db_uri = base_db_url + 'league_manager'
api_access_db_uri = base_db_url + 'api_access'

redis_host = os.getenv('REDIS_HOST')
redis_port = int(os.getenv('REDIS_PORT'))

celery_broker = f"redis://{redis_host}:{redis_port}/0"
celery_backend = "db+" + base_db_url + "celery"

cache_backend = f"redis://{redis_host}:{redis_port}/1"
limiter_backend = f"redis://{redis_host}:{redis_port}/2"


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = league_manager_db_uri
    SQLALCHEMY_BINDS = {
        'api_access': api_access_db_uri
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'localhost')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 25))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    DOMAIN = os.getenv('DOMAIN')
    ADMINS = mailing_list
    CELERY = {
        'broker_url': celery_broker,
        'result_backend': celery_backend
    }
    APIFAIRY_TITLE = 'Slapshot: Rebound - League Manager API'
    APIFAIRY_VERSION = '0.8.4 - dev'
    CACHE_TYPE = 'RedisCache'
    CACHE_DEFAULT_TIMEOUT = 10  # TODO set to 300 for prod
    CACHE_REDIS_URL = cache_backend
    CACHE_SOURCE_CHECK = True
    RATELIMIT_APPLICATION = '200 per minute'  # TODO 50
    RATELIMIT_STORAGE_URI = limiter_backend
    RATELIMIT_STRATEGY = 'fixed-window'
    RATELIMIT_HEADERS_ENABLED = True


