from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, URL, Optional, ValidationError
from .models import Doc

class AdicionarDoc(FlaskForm):
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

    link = StringField('Link', validators=[
                        DataRequired(message="Insira um link."), 
                        URL(message="Insira um link válido.")])

    submeter = SubmitField('Adicionar')

    def validate_doc(self, titulo):
        existe = Doc.query.filter_by(titulo=titulo.data).first()
        if existe:
            raise ValidationError("Este documento já existe!")

