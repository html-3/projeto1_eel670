from functools import wraps
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from flask import flash, redirect, url_for, abort
from flask_login import current_user
from app import app, mail, drive
from time import sleep
import os, secrets

def upload_files(file_path, folder_id):
    gfile = drive.CreateFile({'parents': [{'id':f'{folder_id}'}]})
    gfile.SetContentFile(file_path)
    gfile.Upload()

def verify_file_list(file_path, folder_id):
    file_list = drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()
    for file in file_list:
        if file['title'] == file_path:
            os.remove(file_path)
            return str(file['id'])

def change_file(file_path, folder_id):
        upload_files(file_path, folder_id)
        sleep(10)
        link = verify_file_list(file_path, folder_id)
        return link
        
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

def save_file(form_file):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_file.filename)
    file_fn = random_hex + f_ext
    file_path = os.path.join(app.root_path, 'static/file_storage', file_fn)
    form_file.save(file_path)
    return file_fn