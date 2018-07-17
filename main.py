# import os
#import analysis as an
from flask import Flask, render_template, flash, request, url_for, redirect
import numpy as np
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.sql import text
# from sqlalchemy import create_engine
import urllib
# import requests
import pyodbc
import json
# import colors

import analysis as an
# from werkzeug import secure_filename
# from urllib.error import HTTPError
# from time import time, sleep
# from watson_developer_cloud import ToneAnalyzerV3
# from itertools import product
#pyodbc==4.0.23



app = Flask(__name__)


# server = 'darbly.database.windows.net'
# database = 'blendo'
# username = 'tarpley'
# password = 'Password123!'
# driver= '{ODBC Driver 13 for SQL Server}'

# connStr = 'DRIVER='+driver+';SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password
# db = pyodbc.connect(connStr)
# cursor = db.cursor()

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://{}:{}@{}/{}?driver={}'.format(username,password,server,database,driver)
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)


# class Example(db.Model):
#     __tablename__ = 'customers'
#     id = db.Column('id', db.Integer, primary_key=True)
#     first_name = db.Column('first_name',db.Unicode)
#     middle_initial = db.Column('middle_initial',db.Unicode)
#     last_name = db.Column('last_name',db.Unicode)
#     business_type = db.Column('business_type',db.Unicode)
#     industry = db.Column('industry',db.Unicode)
#     region = db.Column('region',db.Unicode)
#     business_model = db.Column('business_model',db.Unicode)
#     revenue = db.Column('revenue',db.Integer)
#     target_demographic = db.Column('target_demographic',db.Unicode)
#     facebook_ad_id = db.Column('facebook_ad_id',db.Integer)
#     business_name = db.Column('business_name',db.Unicode)

# examples = Example.query.all()
# for x in examples:
#     print(x.first_name)


@app.route('/begin')
def begin():
    return render_template('audit.html')

@app.route('/begin/create')
def create_account():
    return render_template('create_account.html')

@app.route('/begin/create/competitors')
def competitors():
    return render_template('competitors.html')

@app.route('/begin/create/competitors/type')
def type():
    return render_template('type.html')




@app.route('/begin/create/competitors/type/nice')
def nice():
    return render_template('nice.html')

    


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/onload')
def onload():
	a = an.get_customers()
	name = a['first_name'][0]
	last = a['last_name'][0]
	full_name = name + " " + last

	# cpas = an.get_top_cpas()
	# one = cpas[0]

	return full_name #, cpas

@app.route('/data-pop')
def onload_2():
	cpas = an.get_top_cpas()
	cpas = np.round(cpas, 2)
	#cpas = cpas.astype(str)
	cpas = cpas.tolist()
	cpas = json.dumps(cpas)

	return cpas


# @app.route('/dashboard')
# def dashboard():
# 	return render_template('dashboard.html')


# @app.route('/login/', methods=['POST', 'GET'])
# def login_page():
# 	error = ''

# 	if request.method == "POST":

# 		attempted_username = request.form['username']
# 		attempted_password = request.form['password']

# 		x = an.test()

# 		#flash(attempted_username)
# 		#flash(attempted_password)

# 		if attempted_username == "admin" and attempted_password == "password":
# 		    return redirect(url_for('dashboard'))

# 		else:
# 		    error = "Invalid credentials. Try Again."


# 	return redirect(url_for('dashboard'))
# 	#return render_template("login.html", error = error)


@app.route('/recommendations')
def recommendations():
    return render_template('recommendations.html')

@app.route('/recommendations/')
def red_rec():
    return redirect("/recommendations", code=302)
@app.route('/getrecs')
def get_rec():
    print('hi from the client')
    a = an.petri_dish()
    petri = a.head(5)
    petjson = petri.to_json(orient='split')

    return petjson





@app.route('/campaigns')
def campaigns():
    return render_template('campaigns.html')


@app.route('/campaigns/')
def red_campaigns():
    return redirect("/campaigns", code=302)


@app.route('/integrations')
def integrations():
    return render_template('integrations.html')


@app.route('/integrations/')
def red_integrations():
    return redirect("/integrations", code=302)


@app.route('/settings')
def settings():
    return render_template('settings.html')


@app.route('/settings/')
def red_settings():
    return redirect("/settings", code=302)


@app.route('/campaigns/newcampaign')
def create_campaign():
    return render_template('newcampaign.html')


@app.route('/campaigns/newcampaign')
def red_newcampaigns():
    return redirect("/campaigns/newcampaign", code=302)


#UPLOAD_FOLDER = '../marketr/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/create_campaign', methods=['POST'])
def exe_campaign():
    campaign_name = request.form['campaign_name']

    file = request.files['files[]']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    dog = request.form['dog']
    beer = request.form['beer']

    print(campaign_name + " " + filename + " " + beer)

    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(debug=True)
