from functools import wraps
from flask import abort, session, redirect, url_for
from flask_login import current_user
from .models import Permission
from functools import wraps


# 检查用户是否具有某权限
def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return decorated_function

    return decorator


def admin_reqiured(f):
    return permission_required(Permission.ADMINISTER)


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('employee_id'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))

    return wrapper
