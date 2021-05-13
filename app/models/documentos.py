from app import db

class Documento(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    título = db.Column(db.String(150), nullable=False)
    # matéria (db.List código)
    autor = db.Column(db.String(120))
    tipo = db.Column(db.String(5), nullable=False)
    formato = db.Column(db.String(3), nullable=False)
    link = db.Column(db.String(120))

    def _repr_(self):
        return f"{self.id} - {self.título}.{self.formato} ({self.autor}):\n\tLink:{self.link})"