from app import db
from datetime import datetime

class Doc(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    titulo = db.Column(db.String(150), nullable=False)
    # matéria (db.List código)
    autor = db.Column(db.String(120))
    tipo = db.Column(db.String(6), nullable=False)
    formato = db.Column(db.String(3), nullable=False)
    link = db.Column(db.String(150), nullable=False)

    comentarios = db.relationship('ComentarioDoc', backref=db.backref('docu', lazy=True))

    def __repr__(self):
        return f"{self.id} - {self.titulo}.{self.formato} ({self.autor}): {self.link})"

class ComentarioDoc(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    doc_id = db.Column(db.Integer, db.ForeignKey('doc.id'), nullable=False)
    
    nome_usuario = db.Column(db.String(120), nullable=False)
    conteudo = db.Column(db.String(280), nullable=False)
    data = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.id} - {self.nome_usuario}: {self.conteudo}"

