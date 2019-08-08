from app import app
from flask import render_template

@app.route('/')
def index():
    return render_template('branding/index.html')

@app.route('/privacy')
def privacy():
	return render_template('branding/privacy.html')

@app.route('/terms_of_service')
def terms():
	return render_template('branding/terms_of_service.html')