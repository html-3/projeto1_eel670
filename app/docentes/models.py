from app import db
from datetime import datetime

class Docente(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    # Matrícula SIAPE não é obrigatória
    siape = db.Column(db.Integer, default=1000000)
    nome = db.Column(db.String(100), nullable=False)
    # Email instucional, preferência por @poli.ufrj.br
    email = db.Column(db.String(50), unique=True, nullable=False)
    dep = db.Column(db.String(100), nullable=False)
    # Link do perfil UFRJ, também não é obrigatório
    link_ufrj = db.Column(db.String(100))

    comentarios = db.relationship('ComentarioDocente', backref=db.backref('docen', lazy=True))

    def __repr__(self):
        if self.siape == self.siape.default:
            return f"{self.id} - {self.nome}, Email: {self.email}; Depart.: {self.dep}"
        return f"{self.siape} - {self.nome}, Email: {self.email}; Depart.: {self.dep}"

class ComentarioDocente(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    doce_id = db.Column(db.Integer, db.ForeignKey('docente.id'), nullable=False)
    
    nome_usuario = db.Column(db.String(120), nullable=False)
    conteudo = db.Column(db.String(280), nullable=False)
    data = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.id} - {self.nome_usuario}: {self.conteudo}"
