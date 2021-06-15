from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Optional, Email, EqualTo, ValidationError
from .models import Usuario, Dados
from flask_wtf.file import FileField, FileAllowed    
from flask_login import current_user
from re import sub

class Cadastro(FlaskForm):
    # nome
    # nome de usuario
    # email
    # dre
    # curso
    # periodo
    # senha
    # foto de perfil
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
    dre = StringField('DRE', validators=[
                        DataRequired(message="Insira seu DRE!"), 
                        Length(min=9, max=9, message="Insira apenas 9 digitos!")])
                    
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
    def validate_nome_usuario(self,nome_usuario):
       existe = Usuario.query.filter_by(nome_usuario=nome_usuario.data).first()
       if existe:
           raise ValidationError("Escolha outro nome de usuario!")
    
    def validate_dre(self,dre):
        dre = int(sub("\D", "", dre.data))
        existe = Dados.query.filter_by(dre=dre).first()
        if existe:
           raise ValidationError("Já existe uma conta com esse DRE.")

    def validate_email(self,email):
       existe = Usuario.query.filter_by(email=email.data).first()
       if existe:
          raise ValidationError("Já existe uma conta com esse email.")

class Login(FlaskForm):
    nome_usuario = StringField('Nome de usuário', validators=[DataRequired(message="Insira seu nome de usuário!"), 
                                         Length(min=5, max=120, message="Nome muito longo/curto!")])
    
    senha = PasswordField('Senha', validators=[DataRequired(message="Insira sua senha!")])
    
    lembrar = BooleanField('Lembrar de mim!',  validators=[Optional()])

    submeter = SubmitField('Entrar')

class UpdateAccountForm(FlaskForm):
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
    

    dre = StringField('DRE', validators=[
                        DataRequired(message="Insira seu DRE!"), 
                        Length(min=9, max=9, message="Insira apenas 9 digitos!")])

    curso = StringField('Curso', validators=[
                        DataRequired(message="Insira seu curso!"), 
                        Length(min=5, max=50, message="Nome de curso muito longo/curto!")])

    periodo = IntegerField('Período', validators=[
                        DataRequired(message="Insira seu período!")])

    picture = FileField('Atualizar Foto de Perfil*', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Atualizar')
    
    def validate_nome_usuario(self,nome_usuario):
        if nome_usuario.data != current_user.nome_usuario:
            existe = Usuario.query.filter_by(nome_usuario=nome_usuario.data).first()
            if existe:
                raise ValidationError("Já existe uma conta com esse nome de usuario")
        
    def validate_email(self,email):
        if email.data != current_user.email:
            existe = Usuario.query.filter_by(email=email.data).first()
            if existe:
                raise ValidationError("Já existe uma conta com esse email.")
    
    def validate_dre(self,dre):
        dre = int(sub("\D", "", dre.data))
        if dre != current_user.dados.dre:
            existe = Dados.query.filter_by(dre=dre).first()
            if existe:
                raise ValidationError("Já existe uma conta com esse DRE.")

class ConfirmarEmail(FlaskForm):

    email = StringField('Email', validators=[
                        DataRequired(message="Insira seu email"), 
                        Email(message="Insira um email válido!"), 
                        Length(min=5, max=50, message="Email muito longo/curto!")])

    def validate_email(self,email):
        existe = Usuario.query.filter_by(email=email.data).first()
        if not existe:
            raise ValidationError("Não existe conta registrada com esse email.")