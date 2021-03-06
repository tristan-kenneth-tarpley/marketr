from functools import wraps
from flask import session, redirect, url_for
from app import app
from services.UserService import load_last_page

def account_rep_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'account_rep' in session and session['account_rep'] == True or 'customer' in session and session['customer'] == True:
            return f(*args, **kwargs)
        else:
            return "YOU CAN'T GO HERE"
    
    return wrap

def onboarding_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session.get('onboarding_complete') == True:
            return f(*args, **kwargs)
        elif session.get('onboarding_complete') == False:
            page = load_last_page(session['user'])
            return redirect(url_for(page, splash=True))
        else:
            return redirect('/logout')

    return wrap
    
def owner_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'owner_logged_in' in session and session['owner_logged_in'] == True:
            return f(*args, **kwargs)
        else:
            return redirect('/logout?admin=True')

    return wrap

def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'admin_logged_in' in session and session['admin_logged_in'] == True:
            return f(*args, **kwargs)
        else:
            return redirect('/logout?admin=True')

    return wrap

def manager_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'manager_logged_in' in session and session['manager_logged_in'] == True:
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