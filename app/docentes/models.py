from app import db

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

    def __repr__(self):
        if self.siape == self.siape.default:
            return f"{self.id} - {self.nome}, Email: {self.email}; Depart.: {self.dep}"
        return f"{self.siape} - {self.nome}, Email: {self.email}; Depart.: {self.dep}"
