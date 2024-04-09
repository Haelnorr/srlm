"""Configuration parameters of the flask app"""
import os
import configparser
from api.srlm.definitions import ROOT_DIR


config = configparser.ConfigParser()
config.read(os.path.join(ROOT_DIR, 'config', 'mail.config'))
mailing_list = config['MAIL']['MailingList'].split(', ')

#league_manager_db_uri = os.getenv('DATABASE_URL', '').replace('"', '') + os.getenv('LEAGUE_MANAGER_DB', '')
#api_access_db_uri = os.getenv('DATABASE_URL', '').replace('"', '') + os.getenv('API_ACCESS_DB', '')
mysql_user = os.getenv('MYSQL_USER')
mysql_pass = os.getenv('MYSQL_PASS')
mysql_host = os.getenv('MYSQL_HOST')
mysql_port = int(os.getenv('MYSQL_PORT'))

base_db_url = f"mysql+pymysql://{mysql_user}:{mysql_pass}@{mysql_host}:{mysql_port}/"
league_manager_db_uri = base_db_url + 'league_manager'
api_access_db_uri = base_db_url + 'api_access'

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
        "broker_url": os.getenv('CELERY_BROKER', "redis://127.0.0.1:6379/0"),
        "result_backend": os.getenv('CELERY_BACKEND')
    }
    APIFAIRY_TITLE = 'Slapshot: Rebound - League Manager API'
    APIFAIRY_VERSION = '0.7 - dev'

