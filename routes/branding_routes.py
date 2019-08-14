from app import app
from flask import render_template, session

@app.route('/')
def index():
    return render_template(
		'branding/index.html',
		logged_in = True if session.get('logged_in') == True else False,
		home=True
	)

@app.route('/pricing')
def pricing():
	return render_template(
		'branding/pricing.html',
		logged_in = True if session.get('logged_in') == True else False
	)

@app.route('/privacy')
def privacy():
	return render_template('branding/privacy.html')

@app.route('/terms_of_service')
def terms():
	return render_template('branding/terms_of_service.html')