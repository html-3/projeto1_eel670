from app import db

class Documento(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    # nome (título do documento)
    # matéria (db.List código)
    # autor (prof ou autos msm)
    # tipo (db.Sting(5) prova, lista, livro)
    # formato (db.String png, pdf, doc, xls)
    # link (db.String -> google drive)

    def __repr__(self):
        return f"Documento('{self.}','{self.}','{self.}','{self.}')"