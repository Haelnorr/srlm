"""Configuration parameters of the flask app"""
import os
import configparser
from api.srlm.definitions import ROOT_DIR


config = configparser.ConfigParser()
config.read(os.path.join(ROOT_DIR, 'config', 'mail.config'))
mailing_list = config['MAIL']['MailingList'].split(', ')

postgres_user = os.getenv('POSTGRES_USER')
postgres_pass = os.getenv('POSTGRES_PASS')
postgres_host = os.getenv('POSTGRES_HOST')
postgres_port = os.getenv('POSTGRES_PORT')
postgres_ssl_mode = os.getenv('POSTGRES_SSL_MODE')
postgres_endpoint_id = os.getenv('POSTGRES_ENDPOINT')

if postgres_port:
    postgres_host = f'{postgres_host}:{postgres_port}'

base_db_url = f"postgresql://{postgres_user}:{postgres_pass}@{postgres_host}/(database)?sslmode={postgres_ssl_mode}"
if postgres_endpoint_id:
    base_db_url = base_db_url + f'&options=endpoint%3D{postgres_endpoint_id}'
league_manager_db_uri = base_db_url.replace('(database)', 'league_manager_api')

redis_host = os.getenv('REDIS_HOST')
redis_port = int(os.getenv('REDIS_PORT'))

celery_broker = f"redis://{redis_host}:{redis_port}/0"
celery_backend = "db+" + base_db_url.replace('(database)', "celery")

cache_backend = f"redis://{redis_host}:{redis_port}/1"
limiter_backend = f"redis://{redis_host}:{redis_port}/2"


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = league_manager_db_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 0,
        'pool_pre_ping': True
    }
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
    APIFAIRY_VERSION = '0.8.16 - dev'
    CACHE_TYPE = 'RedisCache'
    CACHE_DEFAULT_TIMEOUT = os.getenv('API_CACHE_TIMEOUT') or 300
    CACHE_REDIS_URL = cache_backend
    CACHE_SOURCE_CHECK = True
    RATELIMIT_APPLICATION = '200 per minute'
    RATELIMIT_STORAGE_URI = limiter_backend
    RATELIMIT_STRATEGY = 'fixed-window'
    RATELIMIT_HEADERS_ENABLED = True
