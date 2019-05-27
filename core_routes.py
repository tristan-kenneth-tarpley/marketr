from app import *
import hashlib
from passlib.hash import sha256_crypt

@app.route('/')
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('index.html')
        

@app.route('/login', methods=['POST'])
def customer_login():
 
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
 
    
    try:    
        cursor = db.cursor()
        data = cursor.execute("SELECT email, password, ID FROM dbo.customer_basic WHERE email = '" + str(POST_USERNAME) + "'")
        data = cursor.fetchall()
        pw = data[0][1]
        uid = data[0][2]
        cursor.close()


        if sha256_crypt.verify(POST_PASSWORD, pw):
            session['logged_in'] = True
            session['user'] = int(uid)
            session.permanent = True
            session.remember = True

            first_query = sql_to_df("SELECT first_name FROM dbo.customer_basic WHERE ID = '" + str(session['user']) + "'")
            steps = {'competitors': 'competitors',
                     'company_info': 'company',
                     'audience': 'audience',
                     'product_gen': 'product',
                     'product_list': 'product_2',
                     'awareness': 'salescycle',
                     'goals': 'goals',
                     'history': 'history',
                     'platforms': 'platforms',
                     'past': 'past',
                     'the end': 'index'}

            if first_query['first_name'][0] == None:
                return begin()

            else:
                def call_it(name):
                    print('made it here')
                    return steps[name]

                i = 0
                for step in steps:
                    if step != 'the end' and step != 'the end':
                        def_query = sql_to_df("SELECT customer_id FROM " + step + " WHERE customer_id = '" + str(session['user']) + "'")
                        print(step)
                        i+=1
                        print(i)
                        if def_query.empty == True:
                            perc_complete = str(i*10)
                            print(perc_complete)
                            cursor = db.cursor()
                            cursor.execute("""UPDATE dbo.customer_basic SET perc_complete = '""" + str(perc_complete) + """' WHERE id = """ + str(session['user']) + """;commit;""")
                            return redirect(url_for(call_it(step)))
                    else:
                        i+=1
                        return redirect(url_for(call_it(step)))

    except IndexError:
        flash('incorrect email or password')
        return logout()



@app.route("/logout")
def logout():
    session['logged_in'] = False
    return index()


@app.route('/new')
def new():
    if not session.get('logged_in'):
        return render_template('create.html')
    else:
        return begin()


@app.route('/begin')
def begin():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('intake/init_setup.html')


@app.route('/create_user', methods=['POST'])
def create_user():
    session['logged_in'] = True 
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
    password = sha256_crypt.encrypt(str(POST_PASSWORD))

    print(POST_USERNAME + " " + password)

    cursor = db.cursor()
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    query = """INSERT INTO dbo.customer_basic (
                                    email,
                                    password,
                                    account_created,
                                    last_modified)
                VALUES ('""" + POST_USERNAME + """',
                        '""" + password + """',
                        '""" + str(st) + """',
                        '""" + str(st) + """'); commit;"""

    cursor.execute(query)

    data = cursor.execute(""" SELECT ID FROM dbo.customer_basic WHERE email = '""" + POST_USERNAME + """'""")
    data = cursor.fetchone()[0]

    cursor.close()
    
    session['logged_in'] = True
    session.permanent = True
    uid = data
    session['user'] = int(uid)
    return begin()


@app.route('/availability', methods=['GET'])
def availability():
    result = sql_to_df('select email from dbo.customer_basic')
    result = result.to_json(orient='records')

    return result



########admin###########



@app.route('/admin')
def admin():

    if not session.get('logged_in'):
        return render_template('admin_view/login.html')
    else:
        results = sql_to_df("SELECT customer_basic.id, customer_basic.company_name, customer_basic.account_created, customer_basic.perc_complete, customer_basic.last_modified, admins.first_name FROM customer_basic, admins WHERE admins.ID = '" + str(session['admin']) + "' ORDER BY company_name ASC")

        print(results.head())

        return render_template('admin_view/admin_index.html', results=results)

@app.route('/admin/<customer_id>')
def company_view(customer_id):

    if not session.get('logged_in'):
        return render_template('admin_view/login.html')
    else:
        page = request.args.get('page')

        basics_df = an.sql_to_df("""SELECT * FROM dbo.customer_basic WHERE ID = """ + customer_id)
        company_name = basics_df['company_name'][0]


        if page == "profile":
            load_company = basics_df
            load_company.insert(loc=0, column='is profile', value=True)
        else:
            load_company = an.sql_to_df(""" SELECT * FROM dbo.""" + page + """ WHERE customer_id = '""" + customer_id + """'""")
            load_company.insert(loc=0, column='is_profile', value=False)
        
        load_company = clean_for_display(load_company)

        return render_template('admin_view/company_view.html', company=company_name, page=page, data=load_company)





@app.route('/admin_login', methods=['POST'])
def admin_login():

 
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
 
    
    try:    
        cursor = db.cursor()
        data = cursor.execute("SELECT email, password, ID FROM dbo.admins WHERE email = '" + str(POST_USERNAME) + "'")
        data = cursor.fetchall()
        pw = data[0][1]
        uid = data[0][2]
        cursor.close()


        if sha256_crypt.verify(POST_PASSWORD, pw):
            session['logged_in'] = True
            session['admin'] = int(uid)
            session.permanent = True
            session.remember = True
            return redirect(url_for('admin'))


    except IndexError:
        flash('incorrect email or password')
        return redirect(url_for('admin'))


@app.route('/load_admin')
def load_admin():
    results = sql_to_df('SELECT customer_basic.id, customer_basic.company_name, admins.first_name FROM customer_basic, admins WHERE admins.ID = ' + str(session['admin']))

    results = results.to_json(orient='records')

    return results


@app.route('/admin_availability', methods=['GET'])
def admin_availability():
    result = sql_to_df('select email from dbo.admins')
    result = result.to_json(orient='records')

    return result


@app.route('/new_admin')
def new_admin():
    return render_template('admin_view/new.html')


@app.route('/add_admin', methods=['POST'])
def add_admin():
    POST_first_name = str(request.form['first_name'])
    POST_last_name = str(request.form['last_name'])
    POST_USERNAME = str(request.form['email'])
    POST_PASSWORD = str(request.form['password'])
    password = sha256_crypt.encrypt(str(POST_PASSWORD))

    cursor = db.cursor()

    query = """INSERT INTO dbo.admins (
                                    first_name,
                                    last_name,
                                    email,
                                    password)
                VALUES ('""" + POST_first_name + """',
                        '""" + POST_last_name + """',
                        '""" + POST_USERNAME + """',
                        '""" + password + """'); commit;"""

    cursor.execute(query)

    cursor.close()

    return admin()


photos = UploadSet('photos', IMAGES)
filepath = 'uploads/img'

app.config['UPLOADED_PHOTOS_DEST'] = filepath
configure_uploads(app, photos)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = filepath + "/" + filename

        return path
    return render_template('upload.html')



















