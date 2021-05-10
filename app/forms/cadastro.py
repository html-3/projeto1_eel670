from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class CadastroDiscente(FlaskForm):
    dre = StringField('DRE', validators=[DataRequired(), Length(min=9, max=9, message="Insira apenas 9 digitos!")])

    nome = StringField('Nome', validators=[DataRequired(), Length(min=5, max=100, message="Nome muito longo/curto!")])
    
    nome_usuario = StringField('Nome de usuário', validators=[DataRequired(), Length(min=5, max=120, message="Nome muito longo/curto!")])

    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=5, max=50, message="Email muito longo/curto!")])
    
    curso = StringField('Curso', validators=[DataRequired(), Length(min=5, max=50, message="Nome de curso muito longo/curto!")])

    senha = PasswordField('Senha', validators=[DataRequired()])
    
    confirmar_senha = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('senha')])

    submit = SubmitField('Confirmar!')