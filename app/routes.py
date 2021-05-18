from app.decoradores import check_confirmed
from app import app, db, bcrypt
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, current_user, logout_user, login_required
from app.token import gerar_token, confirmar_token
from app.email import enviar_email
from app.decoradores import check_confirmed
from app.forms.cadastro import CadastroDiscente
from app.forms.docs import AdicionarDoc
from app.forms.login import Login
from app.models.db import Usuario, Dados, Doc
from app.models.docente import Docente


@app.route("/", methods = ["GET"])
@app.route("/home")
def home():
    return render_template('main/home.html', title='Home')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = Login()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(nome_usuario=form.nome_usuario.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form.senha.data):
            login_user(usuario, remember=form.lembrar.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Acesso mal sucedido. Por favor reveja usuario e senha', 'danger')
    return render_template('usuario/login.html', title='Login', form=form)

@app.route("/cadastro", methods = ["GET","POST"])
def cadastro():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = CadastroDiscente()
    if form.validate_on_submit():
        hashed_senha = bcrypt.generate_password_hash(form.senha.data).decode('utf-8')
        usuario = Usuario(
                        nome_usuario=form.nome_usuario.data, 
                        senha=hashed_senha, 
                        email=form.email.data)
        
        db.session.add(usuario)
        db.session.commit()

        token = gerar_token(usuario.email)
        confirmar_url = url_for('confirmar_email', token=token, _external=True)
        html = render_template('usuario/email.html', confirmar_url=confirmar_url)
        subject = 'Por favor, confirme seu email.'
        enviar_email(usuario.email, subject, html)

        login_user(usuario)

        dados = Dados(
                        dre=form.dre.data, 
                        nome=form.nome.data, 
                        curso=form.curso.data,
                        periodo=form.periodo.data)
        db.session.add(dados)
        db.session.commit()

        flash('Um link de confirmação foi enviado via email.', 'warning')
        return redirect(url_for('n_confirmado'))
    return render_template('usuario/cadastro.html', title='Cadastro', form=form)   

@app.route('/confirmar/<token>')
@login_required
def confirmar_email(token):
    try:
        email = confirmar_token(token)
    except:
        flash('O link de confirmação não é válido ou expirou.', 'danger')
    user =  Usuario.query.filter_by(email=email).first_or_404()
    if user.confirmado:
        flash('Conta já foi confirmada. Favor efetuar login.', 'success')
    else:
        user.confirmado = True
        user.registrado_data = datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('Sua conta foi confirmada com sucesso.', 'success')
    return redirect(url_for('home'))

@app.route('/n_confirmado')
def n_confirmado():
    if current_user.confirmado:
        return redirect('home')
    flash('Favor confirmar a sua conta!', 'warning')
    return render_template('usuario/n_confirmado.html')

@app.route('/reenviar')
@login_required
def reenviar_confirmacao():
    token = gerar_token(current_user.email)
    confirmar_url = url_for('confirmar_email', token=token, _external=True)
    html = render_template('usuario/email.html', confirmar_url=confirmar_url)
    subject = 'Por favor, confirme o seu email'
    enviar_email(current_user.email, subject, html)

    flash('Um novo link de confirmação foi enviado via email.', 'success')

    return redirect(url_for('n_confirmado'))

@app.route('/documento', methods=['GET','POST'])
@login_required
@check_confirmed
def documento():
    # quantidade de documentos a ser mostrado no site
    # incluir forma de iterar sobre os diferentes blocos
    # descobrir como fzr slicing da database
    quantidade = 10
    docs = Doc.query.limit(quantidade).all()

    form = AdicionarDoc()
    if form.validate_on_submit():
        doc = Doc(
                        titulo=form.titulo.data, 
                        autor=form.autor.data,
                        tipo=form.tipo.data, 
                        formato=form.formato.data,  
                        link=form.link.data)
        db.session.add(doc)
        db.session.commit()

        flash('Documento cadastrado com sucesso!', 'success')
        return redirect(url_for('documento'))
    return render_template('main/documento.html', title='Documentos', docs=docs, form=form)

@app.route('/documento/<int:documento_id>', methods=['GET','POST'])
@login_required
@check_confirmed
def documento_esp(documento_id):
    doc = Doc.query.get_or_404(documento_id)
    return render_template('main/documento_esp.html', title="Documento", doc=doc)

@app.route('/documento/<int:documento_id>/editar', methods=['GET','POST'])
@login_required
@check_confirmed
def editar_documento(documento_id):
    doc = Doc.query.get_or_404(documento_id)

    if not current_user.admin:
        redirect(url_for('documento'))

    form = AdicionarDoc()
    if form.validate_on_submit():
        doc.titulo = form.titulo.data
        doc.autor = form.autor.data
        doc.tipo = form.tipo.data
        doc.formato = form.formato.data
        doc.link = form.link.data
        db.session.commit()
        flash('Documento atualizado!', 'success')
        return redirect(url_for('documento', post_id=doc.id))

    elif request.method == 'GET':
        form.titulo.data = doc.titulo
        form.autor.data = doc.autor
        form.tipo.data = doc.tipo
        form.formato.data = doc.formato
        form.link.data = doc.link
    return render_template('main/editar_documento.html', title="Documento", form=form)

@app.route('/editar_documento/<int:documento_id>/deletar', methods=['GET','POST'])
@login_required
@check_confirmed
def deletar_documento(documento_id):
    doc = Doc.query.get_or_404(documento_id)

    if not current_user.admin:
        redirect(url_for('documento'))

    db.session.delete(doc)
    db.session.commit()
    flash('Documento deletado!', 'success')
    return redirect(url_for('documento'))
    
# fácil de fazer, mas sem tempo irmao
""" @app.route('/conta/<str:nome_usuario>')
@login_required
@check_confirmed
def conta(nome_usuario):
    usuario = Doc.query.get_or_404(nome_usuario)

    if not current_user.admin:
        redirect(url_for('documento'))

    form = AdicionarDoc()
    if form.validate_on_submit():
        doc.titulo = form.titulo.data
        doc.autor = form.autor.data
        doc.tipo = form.tipo.data
        doc.formato = form.formato.data
        doc.link = form.link.data
        db.session.commit()
        flash('Documento atualizado!', 'success')
        return redirect(url_for('documento', post_id=doc.id))

    elif request.method == 'GET':
        form.titulo.data = doc.titulo
        form.autor.data = doc.autor
        form.tipo.data = doc.tipo
        form.formato.data = doc.formato
        form.link.data = doc.link
    return render_template('main/editar_documento.html', title="Documento", form=form) """
# <a class="nav-item nav-link" href="{{ url_for('conta') }}">Conta</a> 
# ao parecer comentários dentro do html causam problemas quando contem código do python
# isto pertence ao layout na parte {% if user_is_authenticated %}
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))