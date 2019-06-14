from app import *
from helpers.helpers import *
from helpers.classes import User
import hashlib
from bleach import clean
from flask_mail import Mail, Message
from passlib.hash import sha256_crypt
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature



@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', first=4, second=0,third=4), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('error.html', first=5, second=0,third=0), 500





app.config.from_pyfile('config.cfg')
mail = Mail(app)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])


@app.route('/forgot')
def forgot():
    return render_template('forgot.html', send=True)

@app.route('/forgot/reset', methods=['GET', 'POST'])
def reset():
    POST_USERNAME = clean(request.form['username'])
    query = "SELECT * FROM dbo.customer_basic WHERE email = ?"
    tup = (POST_USERNAME,)
    data, cursor = execute(query, True, tup)

    data = data.fetchone()

    if data != None:
        token = s.dumps(POST_USERNAME, salt="password-reset")
        msg = Message('Reset Password', sender='no-reply@marketr.life', recipients=[POST_USERNAME])
        link = url_for('forgot_password', token=token, _external=True)

        msg.body = f"Your password reset link is: {link}"
        mail.send(msg)
        message_sent = "Your password reset link has been sent. If there is an account associated with that email, you should see it any moment."
    else:
        message_sent = "Your password reset link has been sent! If there is an account associated with that email, you should see it any moment."

    return render_template('forgot.html', send=True, message_sent=message_sent)


@app.route('/forgot_password/<token>')
def forgot_password(token):
    email = s.loads(token, salt='password-reset', max_age=3600)
    return render_template("forgot.html", token=token, send=False, conf=False, reset=False)


@app.route('/forgot_password/update_password', methods=['POST', 'GET'])
def update_password():

    token = request.args.get('token')
    email = s.loads(token, salt='password-reset', max_age=3600)
    POST_password = clean(request.form['password'])
    password = sha256_crypt.encrypt(POST_password)

    tup = (password, email)
    query = "UPDATE dbo.customer_basic SET password = ? WHERE email = ?;commit;"
    print(query)
    execute(query, False, tup)

    return render_template('login.html', reset=True)





@app.route('/confirm_email/<token>')
def confirm_email(token):
    email = s.loads(token, salt='email-confirm', max_age=3600)

    tup = (email,)
    query = "UPDATE dbo.customer_basic SET email_confirmed = 1 WHERE email = ?;commit;"
    execute(query, False, tup)
    # return query
    return render_template("login.html", conf=True)


@app.route('/create_user', methods=['POST'])
def create_user():
    POST_USERNAME = clean(request.form['username'])
    POST_PASSWORD = clean(request.form['password'])
    password = sha256_crypt.encrypt(str(POST_PASSWORD))

    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    first_tup = (POST_USERNAME,)
    first_query = "SELECT * FROM dbo.customer_basic WHERE email = ?"
    data, cursor = execute(first_query, True, first_tup)
    data = cursor.fetchone()
    if data == None:

        token = s.dumps(POST_USERNAME, salt="email-confirm")
        msg = Message('Confirm Email', sender='no-reply@marketr.life', recipients=[POST_USERNAME])
        link = url_for('confirm_email', token=token, _external=True)

        msg.body = f"Your link is: {link}"

        mail.send(msg)

        tup = (POST_USERNAME, password, str(st), str(st))
        query = """INSERT INTO dbo.customer_basic (
                                        email,
                                        password,
                                        account_created,
                                        last_modified,
                                        email_confirmed)
                    VALUES (?,
                            ?,
                            ?,
                            ?,
                            0); commit;"""

        execute(query, False, tup)
        return redirect(url_for("splash", next_step="begin"))
    else:
        error = "Account already exists with email. Please try again."
        print(error)
        return render_template('create.html', error=error)

        
@app.route('/login_page', methods=['GET'])
def login_page():
    if not session.get('logged_in'):
        return render_template('login.html')

    else:
        return redirect(url_for('index'))

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first!")
            return redirect(url_for('login_page'))

    return wrap

@app.route('/login', methods=['POST'])
def customer_login():
    POST_USERNAME = clean(request.form['username'])
    POST_PASSWORD = clean(request.form['password'])
    
    try:   
        tup = (POST_USERNAME,)
        query = "SELECT email, password, ID, email_confirmed FROM dbo.customer_basic WHERE email = ?"
        data, cursor = execute(query, True, tup)
        data = cursor.fetchall()
        cursor.close()
        pw = data[0][1]
        uid = data[0][2]
        email_confirmed = data[0][3]

        if sha256_crypt.verify(POST_PASSWORD, pw):
            if email_confirmed == 1:
                session['logged_in'] = True
                session['user'] = int(uid)
                session.permanent = True
                session.remember = True

                first_query = sql_to_df("SELECT first_name FROM dbo.customer_basic WHERE ID = '" + str(session['user']) + "'")

                if first_query['first_name'][0] == None:
                    me = User(session['user'])
                    return redirect(url_for('begin'))

                else:
                    me = User(session['user'])
                    step = load_last_page(session['user'])
                    if step == "product":
                        return redirect(url_for("product", redirect=True))
                    else:
                        return redirect(url_for(step))
            else:
                tup = ("begin",)
                query = "SELECT heading, paragraph FROM dbo.splash WHERE after_page = ?"
                data, cursor = execute(query, True, tup)
                heading, paragraph = cursor.fetchone()
                heading = heading.replace("`", "'")
                paragraph = paragraph.replace("`", "'")
                return render_template('intake/splash.html', next_step='begin', heading=heading, paragraph=paragraph)

        else:
            error = "Invalid credentials. Try again."
            return render_template("login.html", error = error)  

    except Exception as e:
    # except AssertionError:
        error = "Invalid credentials. Try again!"
        return render_template("login.html", error = error)  
        



@app.route("/logout")
@login_required
def logout():
    session['logged_in'] = False
    session.clear()
    return redirect(url_for('index'))


@app.route('/new')
def new():
    if not session.get('logged_in'):
        return render_template('create.html')
    else:
        return begin()


@app.route('/begin')
@login_required
def begin():
    return render_template('intake/init_setup.html')



@app.route('/availability', methods=['GET'])
def availability():
    result = sql_to_df('select email from dbo.customer_basic')
    result = result.to_json(orient='records')

    return result



########admin###########


def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'admin_logged_in' in session:
            return f(*args, **kwargs)
        else:
            return render_template('admin_view/login.html')

    return wrap


@app.route('/admin')
@admin_required
def admin():
    results = sql_to_df("SELECT customer_basic.id, customer_basic.company_name, customer_basic.account_created, customer_basic.perc_complete, customer_basic.last_modified, admins.first_name FROM customer_basic, admins WHERE admins.ID = '" + str(session['admin']) + "' ORDER BY company_name ASC")
    return render_template('admin_view/admin_index.html', results=results)


@app.route('/admin/branch', methods=['GET', 'POST'])
@admin_required
def branch():

    if request.method == 'POST':
        branch_trigger = str(request.form['branch_trigger'])
        branch_trigger_val = str(request.form['branch_trigger_val'])
        branch_action = str(request.form['branch_action'])
        affected_page = str(request.form['affected_page'])
        mask_val = str(request.form['mask_val'])
        default_mask = str(request.form['default_mask'])
        hide_val = request.form['hide_val']
        ind = request.form['ind']

        cursor = db.cursor()
        if branch_action == "hide":
            tup = (branch_trigger, branch_action, affected_page, hide_val, ind, branch_trigger_val)
            query = """INSERT INTO dbo.branches
                        (branch_trigger, branch_action, affected_page, hide_val, ind, branch_trigger_val)
                        VALUES (?,?,?,?,?,?);commit;"""
            execute(query, False, tup)

        elif branch_action == "mask":
            tup = (branch_trigger, branch_action, affected_page, mask_val, default_mask, ind, branch_trigger_val)
            query = """INSERT INTO dbo.branches
                        (branch_trigger, branch_action, affected_page, mask_val, default_mask, ind, branch_trigger_val)
                        VALUES (?,?,?,?,?,?,?);commit;"""
            execute(query, False, tup)
        else:
            return False

    branch_tup = ('affected_page',)
    branches = "SELECT ind, ?, branch_action, branch_trigger_val FROM dbo.branches ORDER BY affected_page ASC"
    branches, cursor = execute(branches, True, branch_tup)
    branches = cursor.fetchall()

    cursor.close()

    return render_template('admin_view/branch.html', branches=branches)

@app.route('/admin/<customer_id>')
@admin_required
def company_view(customer_id):


    page = request.args.get('page')
    basics_df = an.sql_to_df("""SELECT * FROM dbo.customer_basic WHERE ID = """ + customer_id)
    company_name = basics_df['company_name'][0]


    if page == "profile":
        load_company = basics_df
        load_company.insert(loc=0, column='is profile', value=True)
    elif page == "audience":
        load_company = an.sql_to_df(f"""SELECT * FROM dbo.audience WHERE customer_id = {customer_id}""")
        load_company = load_company.drop(columns=['customer_id', 'age_group_1', 'age_group_2', 'age_group_3', 'age_group_4', 'age_group_5', 'age_group_6', 'age_group_7', 'age_group_8', 'before_1', 'before_2', 'before_3', 'before_4', 'before_5', 'before_6', 'before_7', 'before_8', 'before_9', 'before_10', 'before_freeform', 'after_1', 'after_2', 'after_3', 'after_4', 'after_5', 'after_6', 'after_7', 'after_8', 'after_9', 'after_10', 'after_freeform'])
        audiences_dict = clean_audience(customer_id)
        columns = list(load_company.columns)
        return render_template('admin_view/company_view.html',columns=columns,audiences=audiences_dict, customer_id=customer_id, company=company_name, page=page, data=load_company)
    elif page == "product":
        load_company = an.sql_to_df(f"""SELECT gen_description, quantity, link FROM dbo.product WHERE customer_id = {customer_id}""")
        product_dict = clean_product(customer_id)

        product_list = an.sql_to_df(f"""SELECT * FROM dbo.product_list WHERE customer_id = {customer_id}""")
        product_list = product_list.drop(columns=['customer_id'])
        product_list = clean_for_display(product_list)

        return render_template('admin_view/company_view.html',product_list=product_list,product_dict=product_dict, customer_id=customer_id, company=company_name, page=page, data=load_company)
    elif page == "notes":
        load_company = an.sql_to_df(f"""SELECT * from dbo.notes WHERE customer_id = {customer_id} ORDER BY added DESC""")
    elif page == "salescycle":
        awareness = an.sql_to_df(f"""SELECT tactic FROM dbo.awareness WHERE customer_id = {customer_id}""")
        evaluation = an.sql_to_df(f"""SELECT tactic FROM dbo.evaluation WHERE customer_id = {customer_id}""")
        conversion = an.sql_to_df(f"""SELECT tactic FROM dbo.conversion WHERE customer_id = {customer_id}""")
        retention = an.sql_to_df(f"""SELECT tactic FROM dbo.retention WHERE customer_id = {customer_id}""")
        referral = an.sql_to_df(f"""SELECT tactic FROM dbo.referral WHERE customer_id = {customer_id}""")

        return render_template('admin_view/company_view.html', customer_id=customer_id, company=company_name, page=page, data='hi', awareness=awareness, evaluation=evaluation, conversion=conversion, retention=retention, referral=referral)
    else:
        load_company = an.sql_to_df(""" SELECT * FROM dbo.""" + page + """ WHERE customer_id = """ + str(customer_id))
        load_company.insert(loc=0, column='is_profile', value=False)
    
    load_company = clean_for_display(load_company)

    return render_template('admin_view/company_view.html', customer_id=customer_id, company=company_name, page=page, data=load_company)


@app.route('/admin/<customer_id>/note', methods=['POST'])
@admin_required
def add_note(customer_id):
    if request.method == 'POST':
        POST_note = clean(request.form['note'])
        # ' = `
        # " = ~
        POST_note = POST_note.replace("'","`")
        POST_note = POST_note.replace('"',"~")
        tup = (customer_id, session['admin_first'], session['admin_last'], POST_note)
        query = "INSERT INTO dbo.notes (customer_id, author, author_last, content) VALUES(?,?,?,?);commit;"
        execute(query, False, tup)

    return redirect(url_for('company_view', customer_id=customer_id, page="notes"))


@app.route('/admin_login', methods=['POST'])
def admin_login():

 
    POST_USERNAME = clean(request.form['username'])
    POST_PASSWORD = clean(request.form['password'])
 
    
    # try:    
    tup = (POST_USERNAME,)
    query = "SELECT email, password, ID, first_name, last_name FROM dbo.admins WHERE email = ?"
    data, cursor = execute(query, True, tup)
    data = cursor.fetchall()
    pw = data[0][1]
    uid = data[0][2]
    admin_first = data[0][3]
    admin_last = data[0][4]
    cursor.close()


    if sha256_crypt.verify(POST_PASSWORD, pw):
        session['logged_in'] = True
        session['admin'] = int(uid)
        session['admin_first'] = admin_first
        session['admin_last'] = admin_last
        session['admin_logged_in'] = True
        session.permanent = True
        session.remember = True
        return redirect(url_for('admin'))
    else:
        flash('incorrect email or password')
        return redirect(url_for('logout'))


    # except:
    #     flash('incorrect email or password')
    #     return redirect(url_for('logout'))


@app.route('/load_admin')
@admin_required
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
@admin_required
def add_admin():
    POST_first_name = clean(request.form['first_name'])
    POST_last_name = clean(request.form['last_name'])
    POST_USERNAME = clean(request.form['email'])
    POST_PASSWORD = clean(request.form['password'])
    password = sha256_crypt.encrypt(str(POST_PASSWORD))

    cursor = db.cursor()
    tup = (POST_first_name, POST_last_name, POST_USERNAME, password)
    query = """INSERT INTO dbo.admins (
                                    first_name,
                                    last_name,
                                    email,
                                    password)
                VALUES (?,
                        ?,
                        ?,
                        ?); commit;"""

    execute(query, False, tup)

    return redirect(url_for('admin'))








@app.route('/delete_asset', methods=['GET'])
@login_required
def delete_asset():
    if request.method == 'GET':
        file_path = request.args.get('file_path')
        tup = (file_path, session['user'])
        query = "DELETE FROM dbo.assets WHERE file_path = ? AND customer_id = ?;commit;"
        execute(query, False, tup)
        if os.path.exists(file_path):
            # name = server_path.rsplit('/', 1)[-1]
            print(file_path)
            os.remove(file_path)
        else:
            name = 'does not exist'
            print(file_path)
            print(name)
        return redirect(url_for('creative'))





