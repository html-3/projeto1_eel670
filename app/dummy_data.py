from app import db, bcrypt
from .usuarios.models import Usuario, Dados
from .documentos.models import Doc, ComentarioDoc


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
            confirmado=True)

        db.session.add(tomas)
        db.session.add(Dados(
            usuario_id=1,
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
            admin=True)

        db.session.add(admin)
        db.session.add(Dados(
            dre=999999999,
            nome="Administracao",
            curso="Administracao",
            periodo="0",
            discente=admin))

    if not Doc.query.filter_by(titulo="Prova 1 Circuitos Lógicos").first():
        db.session.add(Doc(
            titulo="Prova 1 Circuitos Lógicos",
            autor="Diego Dutra",
            tipo="Prova",
            formato="pdf",
            link="https://www.compasso.ufrj.br/disciplinas/eel280"))
        db.session.add(Doc(
            titulo="Prova 1 Cálculo II",
            autor="Departamento de Matemática",
            tipo="Prova",
            formato="pdf",
            link="https://arquimedes.nce.ufrj.br/calculo2/"))
    
    db.session.commit()