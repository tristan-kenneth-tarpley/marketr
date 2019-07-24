from functools import wraps
from flask import session, redirect, url_for


def owner_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'owner_logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('logout', admin=True))

    return wrap

def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'admin_logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('logout', admin=True))

    return wrap

def manager_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'manager_logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('logout', admin=True))

    return wrap

def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			return redirect(url_for('login'))

	return wrap