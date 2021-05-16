from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, URL, ValidationError
from app.models.documento import Doc

class CadastroDocs(FlaskForm):
    titulo = StringField('Título', validators=[
                        DataRequired(message="Insira um titulo."), 
                        Length(min=3, max=150, message="Insira um titulo menor.")])
    autor = StringField('Autor', validators=[
                        Length(min=3, max=120, message="Insira um nome de autor menor.")])
    
    tipo = StringField('Tipo', validators=[
                        DataRequired(message="Insira um titulo."), 
                        Length(min=5, max=6, message="Insira um tipo válido.")])

    formato = StringField('Formato', validators=[
                        DataRequired(message="Insira um titulo."), 
                        Length(min=3, max=3, message="Insira um formato válido (ex.: txt, pdf).")])

    link = StringField('Link', validators=[
                        DataRequired(message="Insira um link."), 
                        URL(message="Insira um link válido.")])


    submit = SubmitField('Confirmar!')

    #def validate_doc(self, link):
    #    existe = Doc.query.filter_by(link=link.data).first()
    #    if existe:
    #        raise ValidationError("Este documento já existe.")