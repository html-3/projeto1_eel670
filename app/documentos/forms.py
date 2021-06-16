from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_wtf.file import FileField, FileAllowed 
from wtforms.validators import DataRequired, Length, URL, Optional, ValidationError
from .models import Documento

class AdicionarDocumento(FlaskForm):
    titulo = StringField('Título', validators=[
                        DataRequired(message="Insira um titulo."), 
                        Length(min=3, max=150, message="Insira um titulo menor.")])
    autor = StringField('Autor', validators=[
                        Length(min=3, max=120, message="Insira um nome de autor menor."), Optional()])
    
    tipo = StringField('Tipo', validators=[
                        DataRequired(message="Insira um titulo."), 
                        Length(min=5, max=6, message="Insira um tipo válido.")])

    formato = StringField('Formato', validators=[
                        DataRequired(message="Insira um titulo."), 
                        Length(min=3, max=3, message="Insira um formato válido (ex.: txt, pdf).")])

    arquivo = FileField('Adicionar arquivo', validators=[FileAllowed(['pdf']),
                                                        DataRequired(message="Favor inserir um documento válido.")])
    submeter = SubmitField('Adicionar')

    def validate_doc(self, titulo):
        existe = Documento.query.filter_by(titulo=titulo.data).first()
        if existe:
            raise ValidationError("Este documento já existe!")

class AdicionarComDocumento(FlaskForm):
    conteudo = StringField('Comentário', validators=[
                        Length(min=1, max=280, message="Escreva até 280 caractéres.")])
    
    submeter = SubmitField('Adicionar')
