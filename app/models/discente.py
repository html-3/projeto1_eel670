from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    nome_usuario = db.Column(db.String(120), unique=True, default= 'dados.nome', nullable=False)
    senha = db.Column(db.String(50), nullable=False)
    dados = db.relationship('Dados', backref='usuario', uselist=False, lazy=True)

    def __init__(self, nome_usuario, senha):
        self.nome_usuario = nome_usuario
        self.senha = senha

    def __repr__(self):
        return f"{self.id} - '{self.nome_usuario}'"

class Dados(db.Model):
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    dre = db.Column(db.Integer, primary_key=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    curso = db.Column(db.String(50), nullable=False)
    periodo = db.Column(db.Integer)
    # Confirmação de email @poli.ufrj.br
    email = db.Column(db.String(50), unique=True, nullable=False)
    
    
    def __repr__(self):
        return f" {self.dre} - {self.nome}:\n\tCurso/Período: {self.curso}-{self.periodo}º\n\tEmail: {self.email}"