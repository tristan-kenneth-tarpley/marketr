from flask import Flask, render_template, flash, request, url_for, redirect
import json
import analysis as an
app = Flask(__name__)



@app.route('/onload')
def onload():
	a = an.get_customers()
	name = a['first_name'][0]
	last = a['last_name'][0]
	full_name = name + " " + last
	return full_name


@app.route('/')
def index():
	return app.send_static_file('index.html')


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
	app.run()