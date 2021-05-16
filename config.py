from datetime import MAXYEAR
import os 

basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig(object):
    # Configuração principal
    SECRET_KEY = os.environ.get('SECRET_KEY')  or 'escolher uma chave'
    SECURITY_PASSWORD_SALT = 'bomsabadopvctbm'
    WTF_CSRF_SECRET_KEY = 'pq'
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuração email
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # Autenticação Gmail
    MAIL_USERNAME = 'projetoprovas@gmail.com'
    MAIL_PASSWORD = 'lingprog'
    
    # Conta email
    MAIL_DEFAULT_SENDER = 'projetoprovas@gmail.com' # Mudar pelo nome do email


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///'+os.path.join(basedir,"site.db")
    