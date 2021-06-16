from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from flask_wtf.file import FileField, FileAllowed 
from wtforms.validators import DataRequired, Length, Optional, ValidationError, Required#, URL
from .models import Documento
from app import db
from app.docentes.models import Docente

lista_tipos = ["Escolha um tipo...","Lista","Prova","Livro"]

# isto eh ilegivel mas evita que uma lista sqlalchemy.util._collections.result seja criada :)
lista_donos_crua = db.session.query(Docente.nome).all()
lista_donos = [i for lista_nome in [list(nome) for nome in lista_donos_crua] for i in lista_nome]

class AdicionarDocumento(FlaskForm):
    titulo = StringField('Título', validators=[
                        DataRequired(message="Insira um titulo."), 
                        Length(min=3, max=150, message="Insira um titulo menor.")])
    autor = StringField('Autor', validators=[
                        Length(min=3, max=120, message="Insira um nome de autor menor."), Optional()])

    tipo = SelectField('Tipo', choices=lista_tipos, validators=[
                        Required(message="Insira um tipo."),
                        Length(min=1, max=5, message="Escolha um tipo!")])

    formato = StringField('Formato', validators=[
                        DataRequired(message="Insira um formato."), 
                        Length(min=3, max=3, message="Insira um formato válido (ex.: txt, pdf).")])

    dono = SelectField('Dono (Docente)', choices=lista_donos, validators=[
                        DataRequired(message="Favor inserir um dono válido.")])

    arquivo = FileField('Adicionar arquivo', validators=[FileAllowed(['pdf'])])
    submeter = SubmitField('Adicionar')

    def validate_doc(self, titulo):
        existe = Documento.query.filter_by(titulo=titulo.data).first()
        if existe:
            raise ValidationError("Este documento já existe!")

class AdicionarComDocumento(FlaskForm):
    conteudo = StringField('Comentário', validators=[
                        Length(min=1, max=280, message="Escreva até 280 caractéres.")])
    
    submeter = SubmitField('Adicionar')
