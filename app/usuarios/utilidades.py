from app import db
from datetime import datetime
from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from app.token import gerar_token, confirmar_token
from app.email import enviar_email
from .models import Usuario
from .routes import usuarios


