from app import db


class Usuario(db.Model):

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    nome_usuario = db.Column(db.String(120), unique=True, default= 'dados.nome', nullable=False)
    senha = db.Column(db.String(50), nullable=False)
    # Confirmação de email @poli.ufrj.br
    email = db.Column(db.String(50), unique=True, nullable=False)
    confirmado =  db.Column(db.Boolean, nullable=False, default=False)
    data_registro = db.Column(db.DateTime, nullable=False)
    admin =  db.Column(db.Boolean, nullable=False, default=False)
    dados = db.relationship('Dados', backref='usuario', uselist=False, lazy=True)

    def __init__(self, nome_usuario, senha, email, admin=False):
        self.nome_usuario = nome_usuario
        self.senha = senha
        self.email = email
        self.admin = admin

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return f"{self.id} - '{self.nome_usuario}. Email: {self.email}'"

class Dados(db.Model):
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    dre = db.Column(db.Integer, primary_key=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    curso = db.Column(db.String(50), nullable=False)
    periodo = db.Column(db.Integer)
    
    def __init__(self, usuario_id, dre, nome, curso, periodo):
        self.usuario_id = usuario_id
        self.dre = dre
        self.nome = nome
        self.curso = curso
        self.peiodo =periodo
    
    def __repr__(self):
        return f" {self.dre} - {self.nome}:\n\tCurso/Período: {self.curso}-{self.periodo}º"