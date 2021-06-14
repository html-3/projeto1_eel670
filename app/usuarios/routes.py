from flask import render_template, flash, redirect, url_for, request, Blueprint
from app import db, bcrypt
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required, login_manager
from .utilidades import gerar_token, confirmar_token, enviar_email, check_confirmed, save_picture, upload_files
from .models import Usuario, Dados
from .forms import Login, Cadastro, UpdateAccountForm, ConfirmarEmail

usuarios = Blueprint('usuarios', __name__)
# pagina de login para usuarios
# pagina de cadastro para usuarios
# pagina para confirmar email
# pagina de redirecionamento de emails nao confirmados
# pagina para reenviar confirmacao
# pagina de logout quando email nao esta confirmado
# pagina de lista de usuarios (apenas admin)
# pagina de redirecionamento logout
# pagina de usuario em especifico

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
    subject = 'Email de confirmação - PoliDoc'
    enviar_email(current_user.email, subject, html)

    flash('Um novo link de confirmação foi enviado via email.', 'success')

    return redirect(url_for('usuarios.n_confirmado'))

@usuarios.route('/reenviar_conf',  methods = ["GET","POST"])
def reenviar_confirmacao_logout():
    form = ConfirmarEmail()
    if form.validate_on_submit():
        token = gerar_token(form.email.data)
        confirmar_url = url_for('usuarios.confirmar_email', token=token, _external=True)
        html = render_template('usuario/email.html', confirmar_url=confirmar_url)
        subject = 'Email de confirmação - PoliDoc'
        enviar_email(form.email.data, subject, html)
        flash('Um novo link de confirmação foi enviado via email.', 'success')

    return render_template('usuario/reenviar_email.html', title ='Reenvio de confirmação', form=form)

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

@usuarios.route("/minha_conta", methods = ['GET','POST']) #Página da conta do Usuario
@login_required
@check_confirmed
def minha_conta():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            picture_path = "app/static/profile_pics/"+picture_file
            current_user.image_file = picture_file
            send = Thread(target=upload_files, args=(picture_path,), daemon=True)
            send.start()
        Usuario.query.filter_by(id=current_user.id).update(dict(nome_usuario = form.nome_usuario.data, email = form.email.data))
        Dados.query.filter_by(usuario_id=current_user.id).update(dict(dre = form.dre.data, periodo = form.periodo.data, curso = form.curso.data, nome = form.nome.data.lower().title()))
        db.session.commit()
        flash('Sua conta foi atualizada','sucess')
        return redirect(url_for('usuarios.minha_conta'))
    elif request.method == 'GET':
        form.nome_usuario.data = current_user.nome_usuario
        form.email.data = current_user.email
        form.dre.data = current_user.dados.dre
        form.periodo.data = current_user.dados.periodo
        form.curso.data = current_user.dados.curso
        form.nome.data = current_user.dados.nome
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file) #atualiza a imagem de perfil do usuario
    return render_template('usuario/minha_conta.html', title='Minha Conta', 
                            image_file=image_file, form = form) #chama o template da conta

@usuarios.route('/minha_conta/deletar', methods=['GET','POST'])
@login_required
@check_confirmed
def excluir_conta():
    usuario = Dados.query.filter_by(usuario_id=current_user.dados.usuario_id).first()
    db.session.delete(usuario)
    usuario = Usuario.query.filter_by(id=current_user.id).first()
    db.session.delete(usuario)
    db.session.commit()
    flash('Seu usuário foi excluído com sucesso! Esperamos ter ajudado, a porta da frente estará sempre aberta.', 'warning')
    return redirect(url_for('main.home'))