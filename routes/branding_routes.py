from app import app
from flask import render_template, session, redirect
from services.Blog import Blog

@app.route('/')
def index():
	return "api is running"

@app.route('/privacy')
def privacy():
	return render_template('branding/privacy.html')

@app.route('/terms_of_service')
def terms():
	return render_template('branding/terms_of_service.html')

@app.route('/terms_and_conditions')
def terms_and_conditions():
	return render_template('branding/termsandconditions.html')