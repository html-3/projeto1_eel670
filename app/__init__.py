from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
from flask_mail import Mail
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

db = SQLAlchemy(app)
# migrate = Migrate(app, db)
mail = Mail(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
bcrypt = Bcrypt(app)

from .main.routes import main
from .usuarios.routes import usuarios
from .documentos.routes import documentos
from .docentes.routes import docentes

app.register_blueprint(main)
app.register_blueprint(usuarios)
app.register_blueprint(documentos)
app.register_blueprint(docentes)