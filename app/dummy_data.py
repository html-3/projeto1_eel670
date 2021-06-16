from app import db, bcrypt
from datetime import datetime
from .usuarios.models import Usuario, Dados
from .documentos.models import Documento, ComentarioDocumento
from .docentes.models import Docente, ComentarioDocente

def create_dd():
    db.create_all()
    # assegura q a base de dados seja criada com sucesso
    db.session.commit()
    # data temporária
    # tirar bcrypt dps
    # manter db.session.commit()
    if not Usuario.query.filter_by(nome_usuario="admin").first():
        
        tomas = Usuario(
            nome_usuario="tomas2",
            senha= bcrypt.generate_password_hash("123").decode('utf-8'),
            email="tomas@poli.ufrj.br",
            confirmado=True,
            registrado_data= datetime.now())

        db.session.add(tomas)
        db.session.add(Dados(
            dre=120011111,
            nome="Tomas Tutor",
            curso="Engenharia",
            periodo="4",
            discente=tomas))
        
        admin = Usuario(
            nome_usuario="admin",
            senha= bcrypt.generate_password_hash("123").decode('utf-8'),
            email="admin@poli.ufrj.br",
            confirmado=True,
            admin=True,
            registrado_data= datetime.now())

        db.session.add(admin)
        db.session.add(Dados(
            dre=999999999,
            nome="Administracao",
            curso="Administracao",
            periodo="0",
            discente=admin))
    if not Docente.query.filter_by(nome="Claudio Miceli").first():
        claudio = Docente(
                        nome="Claudio Miceli", 
                        email="cmicelifarias@cos.ufrj.br",
                        dep="Sistemas e Computação", 
                        link_ufrj="https://www.cos.ufrj.br/index.php/pt-BR/telefones-do-pesc/details/3/2783")
        monica = Docente(
                        nome="Monika Merkele", 
                        email="monica@im.ufrj.br",
                        dep="Matemática", 
                        link_ufrj="http://www.im.ufrj.br/index.php/pt/pessoal/docentes/docentes/125-monica-moulin-ribeiro-merkle")
        diego = Docente(
                        nome="Diego Dutra", 
                        email="diegodutra@poli.ufrj.br",
                        dep="Eletrônica e de Computação", 
                        link_ufrj="https://www.del.ufrj.br/equipe/docentes/diego-dutra")

        db.session.add(claudio)
        db.session.add(monica)
        db.session.add(diego)
        if not Documento.query.filter_by(titulo="Prova 1 Circuitos Lógicos 2020.2").first():
            db.session.add(Documento(
                titulo="Prova 1 Circuitos Lógicos 2020.2",
                autor="Diego Dutra",
                tipo="Prova",
                formato="PDF",
                file_link="1fq9z9JCfWbET0nPIqTX5zJkvEOOVEr-b",
                dono=diego))
            db.session.add(Documento(
                titulo="Prova 2 Circuitos Lógicos 2020.2",
                autor="Diego Dutra",
                tipo="Prova",
                formato="PDF",
                file_link="1G5nGExWy_eQzpxsCi1CabjX6aByZGbTW",
                dono=diego))
            db.session.add(Documento(
                titulo="Lista 1 Cálculo II 2020.2",
                autor="Departamento de Matemática",
                tipo="Lista",
                formato="PDF",
                file_link="1mrnkQG59SzJanBe9tGCbmGvobO1meMw2",
                dono=monica))

    db.session.commit()