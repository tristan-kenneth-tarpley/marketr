from functools import wraps
from flask import session, redirect, url_for
from app import *


def owner_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'owner_logged_in' in session and session['owner_logged_in']:
            return f(*args, **kwargs)
        else:
            return redirect('/logout?admin=True')

    return wrap

def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'admin_logged_in' in session and session['admin_logged_in']:
            return f(*args, **kwargs)
        else:
            return redirect('/logout?admin=True')

    return wrap

def manager_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'manager_logged_in' in session and session['manager_logged_in']:
            return f(*args, **kwargs)
        else:
            return redirect('/logout?admin=True')

    return wrap

def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			return redirect('/login')

	return wrap