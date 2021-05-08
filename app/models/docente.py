from app import db

class Docente(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    # sabemos que o siape tem 7 digitos, mas nao sabemos o siape de todos os profs
    siape = db.Column(db.Integer, default=1000000)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    dep = db.Column(db.String(100), nullable=False)
    # do perfil da ufrj do docente, pode nao ser incluido
    link = db.Column(db.String(100))

    def __repr__(self):
        return f"Docente('{self.id}','{self.nome}','{self.email}','{self.dep}')"