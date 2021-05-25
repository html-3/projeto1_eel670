from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Optional, Email, EqualTo, ValidationError
from .models import Usuario, Dados
    
    
class Cadastro(FlaskForm):
    dre = StringField('DRE', validators=[
                        DataRequired(message="Insira seu DRE!"), 
                        Length(min=9, max=9, message="Insira apenas 9 digitos!")])

    nome = StringField('Nome', validators=[
                        DataRequired(message="Insira seu nome!"), 
                        Length(min=5, max=100, message="Nome muito longo/curto!")])
    
    nome_usuario = StringField('Nome de usuário', validators=[
                        DataRequired(message="Insira seu nome de usuário!"), 
                        Length(min=5, max=120, message="Nome muito longo/curto!")])

    email = StringField('Email', validators=[
                        DataRequired(message="Insira seu email"), 
                        Email(message="Insira um email válido!"), 
                        Length(min=5, max=50, message="Email muito longo/curto!")])
    
    curso = StringField('Curso', validators=[
                        DataRequired(message="Insira seu curso!"), 
                        Length(min=5, max=50, message="Nome de curso muito longo/curto!")])

    periodo = IntegerField('Período', validators=[
                        DataRequired(message="Insira seu período!")])

    senha = PasswordField('Senha', validators=[
                        DataRequired(message="Insira sua senha!")])
    
    confirmar_senha = PasswordField('Confirmar Senha', validators=[
                        DataRequired(message="Insira sua senha denovo!"), 
                        EqualTo('senha', message="Suas senhas nao sao iguais!")])
    
    submeter = SubmitField('Cadastrar')


    # confirma se já existe na db ou nao
    def validar_nome_usuario(self,nome_usuario):
       existe = Usuario.query.filter_by(nome_usuario=nome_usuario.data).first()
       if existe:
           raise ValidationError("Escolha outro nome de usuario!")
    
    def validar_dre(self,dre):
       existe = Dados.query.filter_by(dre=dre.data).first()
       if existe:
           raise ValidationError("Já existe uma conta com esse DRE.")

    def validar_email(self,email):
       existe = Usuario.query.filter_by(email=email.data).first()
       if existe:
          raise ValidationError("Já existe uma conta com esse email.")

class Login(FlaskForm):
    nome_usuario = StringField('Nome de usuário', validators=[DataRequired(message="Insira seu nome de usuário!"), 
                                         Length(min=5, max=120, message="Nome muito longo/curto!")])
    
    senha = PasswordField('Senha', validators=[DataRequired(message="Insira sua senha!")])
    
    lembrar = BooleanField('Lembrar de mim!',  validators=[Optional()])

    submeter = SubmitField('Entrar')