from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
from flask_mail import Mail
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import DevelopmentConfig

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