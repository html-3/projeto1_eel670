from app import db

class Doc(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    titulo = db.Column(db.String(150), nullable=False)
    # matéria (db.List código)
    autor = db.Column(db.String(120))
    tipo = db.Column(db.String(6), nullable=False)
    formato = db.Column(db.String(3), nullable=False)
    link = db.Column(db.String(150), nullable=False)

    comentarios = db.relationship('ComentarioDoc', backref='doc', lazy=True)

    def _repr_(self):
        return f"{self.id} - {self.título}.{self.formato} ({self.autor}):\n\tLink:{self.link})"

class ComentarioDoc(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    doc_id = db.Column(db.Integer, db.ForeignKey('doc.id'), nullable=False)
