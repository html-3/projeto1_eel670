from app import db

class Discente(db.Model):
    dre = db.Column(db.Integer, primary_key=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    nome_usuario = db.Column(db.String(120), unique=True, default=nome, nullable=False)
    # ver de dá p confirmar se pertence à @poli.ufrj
    email = db.Column(db.String(50), unique=True, nullable=False)
    curso = db.Column(db.String(50), nullable=False)
    senha = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Discente('{self.dre}','{self.nome_usuario}','{self.nome}','{self.email}','{self.curso}')"