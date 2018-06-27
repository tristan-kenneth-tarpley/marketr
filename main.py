#import analysis as an
from flask import Flask, render_template, flash, request, url_for, redirect
import numpy as np
#import pandas as pd
import requests
import pyodbc
import json
import colors

import analysis as an

from urllib.error import HTTPError
from time import time, sleep
from watson_developer_cloud import ToneAnalyzerV3
from itertools import product



app = Flask(__name__)





@app.route('/')
def index():
	return app.send_static_file('index.html')


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
# 	return app.send_static_file('dashboard.html')



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
	return app.send_static_file('recommendations.html')

@app.route('/campaigns')
def campaigns():
	return app.send_static_file('campaigns.html')

@app.route('/integrations')
def integrations():
	return app.send_static_file('integrations.html')

@app.route('/settings')
def settings():
	return app.send_static_file('settings.html')


if __name__ == '__main__':
	app.run(debug=True)