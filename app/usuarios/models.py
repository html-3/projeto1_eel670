from app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(id):
    return Usuario.query.get(int(id))


class Usuario(db.Model, UserMixin):
    # id do usuario ou discente
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    # nome de perfil personalizado para o usuario
    nome_usuario = db.Column(db.String(120), unique=True, default= 'dados.nome', nullable=False)
    # senha hash
    senha = db.Column(db.String(50), nullable=False)
    # Confirmação de email @poli.ufrj.br
    email = db.Column(db.String(50), unique=True, nullable=False)
    # check de confirmacao do email
    confirmado =  db.Column(db.Boolean, nullable=False, default=False)
    # confere se e um admin
    admin =  db.Column(db.Boolean, default=False)
    # imagem de perfil
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    # data de registro do usuario
    registrado_data = db.Column(db.String(30))

    # dados pessoais do usuario
    dados = db.relationship('Dados', cascade="all,delete", backref='discente', uselist=False, lazy=True)

    def __repr__(self):
        return f"{self.id} - @{self.nome_usuario} - {self.email}'"


class Dados(db.Model):
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))

    # dre do discente, obrigratorio
    dre = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    # nome pessoal do usuario
    nome = db.Column(db.String(100), nullable=False)
    # nome do curso
    curso = db.Column(db.String(50), nullable=False)
    # periodo atual do discente
    periodo = db.Column(db.Integer)
    
    def __repr__(self):
        return f" {self.dre} - {self.nome}: {self.curso} - {self.periodo}º"
