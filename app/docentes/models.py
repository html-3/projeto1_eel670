from app import db
from datetime import datetime

class Docente(db.Model):
    # id principal do docente
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    # nome do docente
    nome = db.Column(db.String(100), nullable=False)
    # Matrícula SIAPE não é obrigatória
    siape = db.Column(db.Integer, default=1000000)
    # email do docente
    # Email instucional, preferência por @poli.ufrj.br?
    email = db.Column(db.String(50), unique=True, nullable=False)
    # departamento do docente
    dep = db.Column(db.String(100), nullable=False)
    # link do docente, é obrigatório
    link_ufrj = db.Column(db.String(100))

    # comentarios associados a pagina do docente
    comentarios = db.relationship('ComentarioDocente', backref=db.backref('docen', lazy=True))
    # documentos requeridos ou usados pelo docente
    documentos = db.relationship('Documento', backref=db.backref('dono', lazy=True))

    def __repr__(self):
        if self.siape == self.siape.default:
            return f"{self.id} - {self.nome}, Email: {self.email}; Depart.: {self.dep}"
        return f"{self.siape} - {self.nome}, Email: {self.email}; Depart.: {self.dep}"

class ComentarioDocente(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    doce_id = db.Column(db.Integer, db.ForeignKey('docente.id'), nullable=False)
    
     # nome do usuario do comentador
    nome_usuario = db.Column(db.String(120), nullable=False)
    # mensagem ou comentario na pratica
    conteudo = db.Column(db.String(280), nullable=False)
    # dia da postagem
    data = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.id} - {self.nome_usuario}: {self.conteudo}"
