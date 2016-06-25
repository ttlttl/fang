# -*- coding=UTF-8 -*-
from functools import wraps
from flask_login import current_user
from flask import abort


def admin_required(func):
    @wraps(func)
    def decorated_func(*args, **kwargs):
        if not current_user.is_administrator():
            abort(404)
        return func(*args, **kwargs)
    return decorated_func