from flask import render_template, flash, redirect, url_for, request, Blueprint
from app import db, bcrypt
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required
from .utilidades import gerar_token, confirmar_token, enviar_email, check_confirmed, save_picture 
from .models import Usuario, Dados
from .forms import Login, Cadastro, UpdateAcountForm 

usuarios = Blueprint('usuarios', __name__)

@usuarios.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = Login()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(nome_usuario=form.nome_usuario.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form.senha.data) and usuario.confirmado:
            login_user(usuario, remember=form.lembrar.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        elif usuario and bcrypt.check_password_hash(usuario.senha, form.senha.data) and not usuario.confirmado:
            flash('Favor confirmar o seu email antes de fazer o login.', 'warning')
        else:
            flash('Acesso mal sucedido. Por favor reveja usuario e senha', 'danger')
    return render_template('usuario/login.html', title='Login', form=form)

@usuarios.route("/cadastro", methods = ["GET","POST"])
def cadastro():
    form = Cadastro()
    if form.validate_on_submit():
        hashed_senha = bcrypt.generate_password_hash(form.senha.data).decode('utf-8')
        usuario = Usuario(
                        nome_usuario=form.nome_usuario.data, 
                        senha=hashed_senha, 
                        email=form.email.data)
        
        db.session.add(usuario)
        db.session.commit()

        token = gerar_token(usuario.email)
        confirmar_url = url_for('usuarios.confirmar_email', token=token, _external=True)
        html = render_template('usuario/email.html', confirmar_url=confirmar_url)
        subject = 'Por favor, confirme seu email.'
        enviar_email(usuario.email, subject, html)

        login_user(usuario)

        dados = Dados(
                    dre=form.dre.data, 
                    nome=form.nome.data.lower().title(), 
                    curso=form.curso.data.lower().title(),
                    periodo=form.periodo.data,
                    discente=usuario)
        db.session.add(dados)
        db.session.commit()

        flash('Um link de confirmação foi enviado via email.', 'warning')
        return redirect(url_for('usuarios.n_confirmado'))
    return render_template('usuario/cadastro.html', title='Cadastro', form=form)   

@usuarios.route('/confirmar/<token>')
@login_required
def confirmar_email(token):
    try:
        email = confirmar_token(token)
    except:
        flash('O link de confirmação não é válido ou expirou.', 'danger')
    usuario =  Usuario.query.filter_by(email=email).first()
    if usuario.confirmado:
        flash('Conta já foi confirmada. Favor efetuar login.', 'success')
    else:
        usuario.confirmado = True
        usuario.registrado_data = datetime.now()
        db.session.add(usuario)
        db.session.commit()
        flash('Sua conta foi confirmada com sucesso.', 'success')
    return redirect(url_for('main.home'))

@usuarios.route('/n_confirmado')
def n_confirmado():
    if current_user.confirmado:
        return redirect('home')
    flash('Favor confirmar a sua conta!', 'warning')
    return render_template('usuario/n_confirmado.html')

@usuarios.route('/reenviar')
@login_required
def reenviar_confirmacao():
    token = gerar_token(current_user.email)
    confirmar_url = url_for('usuarios.confirmar_email', token=token, _external=True)
    html = render_template('usuario/email.html', confirmar_url=confirmar_url)
    subject = 'Por favor, confirme o seu email'
    enviar_email(current_user.email, subject, html)

    flash('Um novo link de confirmação foi enviado via email.', 'success')

    return redirect(url_for('usuarios.n_confirmado'))

@usuarios.route('/lista_usuarios', methods=['GET'])
@login_required
@check_confirmed
def lista_usuarios():
    page = request.args.get('page', 1, type=int)
    usuarios = Usuario.query.order_by(Usuario.id).paginate(page=page, per_page=10)
    quantidade = Usuario.query.count()

    return render_template('usuario/lista_usuarios.html',title='Usuarios', usuarios=usuarios, quantidade=quantidade)

@usuarios.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

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

@usuarios.route("/account", methods = ['GET','POST'])#Página da conta do Usuario
def account():
    form = UpdateAcountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.nome_usuario = form.nome_usuario.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Sua conta foi atualizada','sucess')
        return redirect(url_for('usuarios.account'))
    elif request.method == 'GET':
        form.nome_usuario.data = current_user.nome_usuario
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file) #atualiza a imagem de perfil do usuario
    return render_template('usuario/account.html', title='Account', 
                            image_file=image_file, form = form) #chama o template da conta