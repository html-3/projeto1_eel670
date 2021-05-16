from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Optional

class Login(FlaskForm):
    nome_usuario = StringField('Nome de usuário', validators=[DataRequired(message="Insira seu nome de usuário!"), 
                                         Length(min=5, max=120, message="Nome muito longo/curto!")])
    
    senha = PasswordField('Senha', validators=[DataRequired(message="Insira sua senha!")])
    
    lembrar = BooleanField('Lembrar de mim!',  validators=[Optional()])
    
