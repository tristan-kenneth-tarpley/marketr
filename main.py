from flask import Flask, render_template, flash, request, url_for, flash, redirect, session, abort
import numpy as np
import pandas as pd
import urllib
import os
import pyodbc
import json

import analysis as an


app = Flask(__name__)


#########################
#########################
#########################
#####INTAKE ROUTES#######
#########################
#########################
#########################

@app.route('/begin')
def begin():
    return render_template('intake/init_setup.html')

@app.route('/begin/')
def red_begin():
    return redirect("/begin", code=302)

@app.route('/competitors', methods=['POST'])
def competitors():
    POST_first_name = str(request.form['first_name'])
    POST_last_name = str(request.form['last_name'])
    POST_company_name = str(request.form['company_name'])
    POST_revenue = str(request.form['revenue'])
    POST_city = str(request.form['city'])
    POST_state = str(request.form['state'])

    print(POST_first_name + " " + POST_last_name + " " + POST_company_name + " " + POST_revenue + " " + POST_city + " " + POST_state)

    return render_template('intake/company.html')

@app.route('/competitors/')
def red_competitors():
    return redirect("/competitors", code=302)

@app.route('/competitors/company')
def company():
    return render_template('intake/competitors.html')

@app.route('/competitors/company/')
def red_company():
    return redirect('/competitors/company', code=302)

@app.route('/competitors/company/audience')
def audience():
    return render_template('intake/audience.html')

@app.route('/competitors/company/audience/')
def red_audience():
    return redirect('/competitors/company/audience', code=302)


@app.route('/nice')
def nice():
    return render_template('intake/nice.html')

@app.route('/nice/')
def red_nice():
    return redirect('/nice', code=302)






@app.route('/goals')
def goals():
    return render_template('intake/2/goals.html')

@app.route('/goals/')
def red_goals():
    return redirect('/goals', code=302)




#########################


@app.route('/')
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('index.html')


@app.route('/login', methods=['POST'])
def do_admin_login():
 
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
 
    result = an.sql_to_df("SELECT * from dbo.customers WHERE email = '" + POST_USERNAME + "' AND password = '" + POST_PASSWORD + "'")
    try:    
        if result['id'][0] != None:
            session['logged_in'] = True
            session.permanent = True
            return index()

    except IndexError:
        flash('wrong password!')
        return index()



@app.route("/logout")
def logout():
    session['logged_in'] = False
    return index()


@app.route('/new')
def new():
    if not session.get('logged_in'):
        return render_template('create.html')
    else:
        return render_template('index.html')


@app.route('/create_user')
def create_user():
    session['logged_in'] = True 
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])


    query = """INSERT INTO dbo.customers (
                                email,
                                password)
            VALUES ('""" + str(POST_USERNAME) + """',
                    '""" + str(POST_PASSWORD) + """'; commit;"""

    cursor = an.cursor

    cursor.execute(query)

    return index()






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
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SECRET_KEY'] = os.urandom(12)
    app.run(debug=True)





