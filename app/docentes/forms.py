from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, URL, Optional, ValidationError, Email
from .models import Docente

class AdicionarDocente(FlaskForm):
    nome = StringField('Nome', validators=[
                        DataRequired(message="Insira um nome."), 
                        Length(min=3, max=100, message="Insira um nome menor.")])

    siape = StringField('SIAPE', validators=[
                        Length(min=7, max=7, message="Insira os sete digitos do SIAPE."),
                        Optional()])
    
    email = StringField('Email', validators=[
                        DataRequired(message="Insira seu email"), 
                        Email(message="Insira um email válido!"), 
                        Length(min=5, max=50, message="Email muito longo/curto!")])

    dep = StringField('Departamento', validators=[
                        DataRequired(message="Insira Departamento."), 
                        Length(min=3, max=50, message="Sintetise o nome do departamento.")])

    link = StringField('Link', validators=[
                        DataRequired(message="Insira um link do perfil."), 
                        URL(message="Insira um link válido.")])

    submeter = SubmitField('Adicionar')

    def validate_doc(self, nome):
        existe = Docente.query.filter_by(nome=nome.data).first()
        if existe:
            raise ValidationError("Este documento já existe!")

class AdicionarComDocente(FlaskForm):
    conteudo = StringField('Comentário', validators=[
                        Length(min=1, max=280, message="Escreva até 280 caractéres.")])
    
    submeter = SubmitField('Adicionar')
    