from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email

class Login(FlaskForm):
    dre = StringField('DRE', validators=[DataRequired(), Length(min=9, max=9, message="Insira apenas 9 digitos!")])
    
    senha = PasswordField('Senha', validators=[DataRequired()])
    
    lembrar = BooleanField('Lembrar de mim!')
    
    submit = SubmitField('Entrar!')