"""Configuration parameters of the flask app"""
import os
import configparser
from api.srlm.definitions import ROOT_DIR


config = configparser.ConfigParser()
config.read(os.path.join(ROOT_DIR, 'config', 'mail.config'))
mailing_list = config['MAIL']['MailingList'].split(', ')

db_type = os.getenv('DATABASE_TYPE')
league_manager_db_uri = api_access_db_uri = ''

if db_type == 'postgres':
    postgres_user = os.getenv('POSTGRES_USER')
    postgres_pass = os.getenv('POSTGRES_PASS')
    postgres_host = os.getenv('POSTGRES_HOST')
    postgres_port = os.getenv('POSTGRES_PORT')
    postgres_ssl_mode = os.getenv('POSTGRES_SSL_MODE')
    if postgres_port:
        postgres_host = f'{postgres_host}:{postgres_port}'
    base_db_url = f"postgresql://{postgres_user}:{postgres_pass}@{postgres_host}/(database)?sslmode={postgres_ssl_mode}"
    league_manager_db_uri = base_db_url.replace('(database)', 'league_manager')
    api_access_db_uri = base_db_url.replace('(database)', 'api_access')
    celery_backend = "db+" + base_db_url.replace('(database)', "celery")

elif db_type == 'mysql':
    mysql_user = os.getenv('MYSQL_USER')
    mysql_pass = os.getenv('MYSQL_PASS')
    mysql_host = os.getenv('MYSQL_HOST')
    mysql_port = int(os.getenv('MYSQL_PORT'))
    base_db_url = f"mysql+pymysql://{mysql_user}:{mysql_pass}@{mysql_host}:{mysql_port}/"
    league_manager_db_uri = base_db_url + 'league_manager'
    api_access_db_uri = base_db_url + 'api_access'
    celery_backend = "db+" + base_db_url + "celery"

redis_host = os.getenv('REDIS_HOST')
redis_port = int(os.getenv('REDIS_PORT'))

celery_broker = f"redis://{redis_host}:{redis_port}/0"

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
    APIFAIRY_VERSION = '0.8.14 - dev'
    CACHE_TYPE = 'RedisCache'
    CACHE_DEFAULT_TIMEOUT = os.getenv('SRLM_CACHE_TIMEOUT') or 300
    CACHE_REDIS_URL = cache_backend
    CACHE_SOURCE_CHECK = True
    RATELIMIT_APPLICATION = '200 per minute'
    RATELIMIT_STORAGE_URI = limiter_backend
    RATELIMIT_STRATEGY = 'fixed-window'
    RATELIMIT_HEADERS_ENABLED = True
    SERVER_NAME = os.getenv('SRLM_SERVER_NAME') or None
