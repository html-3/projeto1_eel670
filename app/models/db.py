from enum import unique
from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(id):
    return Usuario.query.get(int(id))


class Usuario(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    nome_usuario = db.Column(db.String(120), unique=True, default= 'dados.nome', nullable=False)
    senha = db.Column(db.String(50), nullable=False)
    # Confirmação de email @poli.ufrj.br
    email = db.Column(db.String(50), unique=True, nullable=False)
    confirmado =  db.Column(db.Boolean, nullable=False, default=False)
    admin =  db.Column(db.Boolean, default=False)
    dados = db.relationship('Dados', backref='usuario', uselist=False, lazy=True)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def repr(self):
        return f"{self.id} - '{self.nome_usuario}. Email: {self.email}'"

class Dados(db.Model):
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    dre = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    curso = db.Column(db.String(50), nullable=False)
    periodo = db.Column(db.Integer)

    def init(self, usuario_id, dre, nome, curso, periodo):
        self.usuario_id = usuario_id
        self.dre = dre
        self.nome = nome
        self.curso = curso
        self.periodo = periodo

    def repr(self):
        return f" {self.dre} - {self.nome}:\n\tCurso/Período: {self.curso}-{self.periodo}º"

class Doc(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    titulo = db.Column(db.String(150), nullable=False)
    # matéria (db.List código)
    autor = db.Column(db.String(120))
    tipo = db.Column(db.String(6), nullable=False)
    formato = db.Column(db.String(3), nullable=False)
    link = db.Column(db.String(150), nullable=False)

    def _repr_(self):
        return f"{self.id} - {self.título}.{self.formato} ({self.autor}):\n\tLink:{self.link})"


db.create_all()
db.session.commit()