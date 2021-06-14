from functools import wraps
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from flask import flash, redirect, url_for, abort
from flask_login import current_user
from app import app, mail, drive
from .models import Usuario
import os, secrets

def upload_files(upload_file):
    
    gfile = drive.CreateFile({'parents': [{'id': '1rXtdkLm3jsrTqpv4Km_mzGmYOWoBjoph'}]})
    gfile.SetContentFile(upload_file)
    gfile.Upload()

"""def verify_file_list(file_name):
    file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format('1cIMiqUDUNldxO6Nl-KVuS9SV-cWi9WLi')}).GetList()
    for file in file_list:
        if file['title'] == file_name:
            Usuario.query.filter_by().first"""

def gerar_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])

def confirmar_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email

def enviar_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)

def check_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.confirmado is False:
            flash('Favor confirmar a sua conta!', 'warning')
            return redirect(url_for('usuarios.n_confirmado'))
        return func(*args, **kwargs)

    return decorated_function

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    form_picture.save(picture_path)
    
    return picture_fn
