from functools import wraps
from flask import session, redirect, url_for


def owner_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session['owner_logged_in']:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('logout', admin=True))

    return wrap

def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session['admin_logged_in']:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('logout', admin=True))

    return wrap

def manager_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session['manager_logged_in'] == True:
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
			return redirect(url_for('login_page'))

	return wrap