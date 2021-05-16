from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user


def check_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.confirmado is False:
            flash('Favor confirmar a sua conta!', 'warning')
            return redirect(url_for('n_confirmado'))
        return func(*args, **kwargs)

    return decorated_function