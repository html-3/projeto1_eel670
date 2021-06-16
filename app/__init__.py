from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
from flask_mail import Mail
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import DevelopmentConfig
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# instanciacao do aplicativo web
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db = SQLAlchemy(app)
# migrate = Migrate(app, db)
mail = Mail(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
bcrypt = Bcrypt(app)

# para evitar problemas na criacao da database com as rotas, isto foi colocado aqui
from app.dummy_data import create_dd
create_dd()

# API com google drive
# autorizacao do google
gauth = GoogleAuth()
# https://stackoverflow.com/questions/24419188/automating-pydrive-verification-process/24542604#24542604
# tenta carregar as credenciais do google
"""gauth.LoadCredentialsFile("gauth_credenciais.txt")
if gauth.credentials is None:
    # autentificar caso nao exista
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    # refresh se elas expiraram
    gauth.Refresh()
else:
    # inicializar caso existam
    gauth.Authorize()
# salvar as crecencias do diretorio
gauth.SaveCredentialsFile("gauth_credenciais.txt")"""
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

# importar os Blueprints de cada parte do codigo
from .main.routes import main
from .usuarios.routes import usuarios
from .documentos.routes import documentos
from .docentes.routes import docentes

# registrar os Blueprints
app.register_blueprint(main)
app.register_blueprint(usuarios)
app.register_blueprint(documentos)
app.register_blueprint(docentes)