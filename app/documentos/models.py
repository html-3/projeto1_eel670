from sqlalchemy.orm import defaultload
from app import db
from datetime import datetime

class Documento(db.Model):
    # id principal do documento
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    # titulo do documento
    titulo = db.Column(db.String(150), nullable=False)
    # matéria (db.List código)
    # escritor ou autor do documento
    autor = db.Column(db.String(120))
    # lista, prova, livro, etc.
    tipo = db.Column(db.String(6), nullable=False)
    # PDF, PNG, DOC, MD, TXT, etc.
    formato = db.Column(db.String(3), nullable=False)
    # link do documento no drive
    file_link = db.Column(db.String(30), default='')

    # comentarios associados a um documento
    comentarios = db.relationship('ComentarioDocumento', cascade="all,delete", backref='docu', lazy=True)
    # docente que requer esse livro
    dono_id = db.Column(db.Integer, db.ForeignKey('docente.id'))

    def __repr__(self):
        return f"{self.id} - {self.titulo}.{self.formato} ({self.autor}))"

class ComentarioDocumento(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    doc_id = db.Column(db.Integer, db.ForeignKey('documento.id'))
    
    # nome do usuario do comentador
    nome_usuario = db.Column(db.String(120), nullable=False)
    # mensagem ou comentario na pratica
    conteudo = db.Column(db.String(280), nullable=False)
    # dia da postagem
    data = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.id} - {self.nome_usuario}: {self.conteudo}"

