from app import app, session, FlaskForm
from flask import request, render_template, redirect, url_for, flash
import services.helpers as helpers
import hashlib
from bleach import clean
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
from services.UserService import UserService
from services.LoginHandlers import login_required, admin_required, owner_required, manager_required, account_rep_required, onboarding_required
from services.AdminService import AdminService, AdminActions, MessagingService, AdminUserService
from services.SharedService import MessagingService, TaskService
from ViewModels.ViewModels import ViewFuncs, AdminViewModel, CustomerDataViewModel
import hashlib
from data.db import execute, sql_to_df
from bleach import clean
from flask_mail import Mail, Message
from passlib.hash import sha256_crypt
import services.forms as forms
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature

@app.route('/forgot')
def forgot():
    return render_template('forgot.html', send=True)


app.config.from_pyfile('config.cfg')
mail = Mail(app)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])


@app.route('/forgot/reset', methods=['GET', 'POST'])
def reset():
    POST_USERNAME = clean(request.form['username'])
    query = "SELECT * FROM dbo.customer_basic WHERE email = ?"
    tup = (POST_USERNAME,)
    data, cursor = execute(query, True, tup)

    data = data.fetchone()
    cursor.close()

    if data != None and request.method=='POST':
        token = s.dumps(POST_USERNAME, salt="password-reset")
        msg = Message('Reset Password', sender='no-reply@marketr.life', recipients=[POST_USERNAME])
        link = url_for('forgot_password', token=token, _external=True)
        msg.body = "Your password reset link is: %s" % (link,)
        mail.send(msg)
        message_sent = "Your password reset link has been sent. If there is an account associated with that email, you should see it any moment."
    else:
        message_sent = "Your password reset link has been sent! If there is an account associated with that email, you should see it any moment."

    return render_template('forgot.html', send=True, message_sent=message_sent)


@app.route('/forgot_password/<token>')
def forgot_password(token):
    # email = s.loads(token, salt='password-reset', max_age=3600)
    return render_template("forgot.html", token=token, send=False, conf=False, reset=False)


@app.route('/forgot_password/update_password', methods=['POST', 'GET'])
def update_password():

    token = request.args.get('token')
    email = s.loads(token, salt='password-reset', max_age=3600)
    POST_password = clean(request.form['password'])
    password = sha256_crypt.encrypt(POST_password)

    tup = (password, email)
    query = "UPDATE dbo.customer_basic SET password = ? WHERE email = ?;commit;"

    execute(query, False, tup)

    return render_template('login.html', reset=True)



    

@app.route('/login', methods=['GET', 'POST'])
def customer_login():

    form = forms.CustomerLogin()

    if ViewFuncs.ValidSubmission(form=form, method=request.method):
        loginResult, action = UserService.customer_login(form.email.data, form.password.data)
        return UserService.routeLogin(loginResult, action, form=form)

    elif request.method == 'GET':
        session['logged_in'] = False

    return render_template('login.html', form=form)



@app.route("/logout")
@login_required
def logout():

    session['logged_in'] = False
    session.clear()

    if request.args.get('admin') != None:
        if request.args.get('admin'):
            return redirect(url_for('admin_login'))
    else:
        return redirect(url_for('index'))


@app.route('/new', methods=['POST', 'GET'])
def new():
    form = forms.CreateCustomer()

    if ViewFuncs.ValidSubmission(form=form, method=request.method):
        result = UserService.CreateCustomer(form.email.data, form.password.data, form=form, app=app)
        if result:
            return redirect(url_for("splash", next_step="begin"))
        else:
            error = "something went wrong."
            return render_template('new.html', form=form, error=error)

    elif request.method == 'GET':
        session['logged_in'] = False
        
    return render_template('new.html', form=form)



@app.route('/confirm_email/<token>')
def confirm_email(token):
    s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    email = s.loads(token, salt='email-confirm', max_age=3600)
    tup = (email,)
    query = "UPDATE dbo.customer_basic SET email_confirmed = 1 WHERE email = ?"
    execute(query, False, tup, commit=True)
    form = forms.CustomerLogin()
    return render_template("login.html", conf=True, form=form)



@app.route('/availability', methods=['GET'])
def availability():
    email = request.args.get('email')
    tup = (email,)
    query = """ SELECT email FROM customer_basic WHERE email = ? """

    data, cursor = execute(query, True, tup)

    data = cursor.fetchall()
    cursor.close()

    if data == []:
        return 'True'
    else:
        return 'False'



########home page###########





# @app.route('/delete_asset', methods=['GET'])
# @login_required
# def delete_asset():
#     if request.method == 'GET':
#         file_path = request.args.get('file_path')
#         tup = (file_path, session['user'])
#         query = "DELETE FROM dbo.assets WHERE file_path = ? AND customer_id = ?;commit;"
#         execute(query, False, tup)
#         if os.path.exists(file_path):
#             # name = server_path.rsplit('/', 1)[-1]
#             print(file_path)
#             os.remove(file_path)
#         else:
#             name = 'does not exist'
#             print(file_path)
#             print(name)
#         return redirect(url_for('creative'))




@app.route('/home', methods=['GET', 'POST'])
@login_required
@onboarding_required
def home():
    view_model = CustomerDataViewModel(customer_id=session['user'], init=True)
    return render_template(
        'layouts/home_layout.html',
        page=view_model
    )




# core actions
@app.route('/api/remove_product', methods=['POST'])
@admin_required
@account_rep_required
def remove_product():
    print(request.form['product_name'])
    UserService.remove_product(request.form.get('product_name'))
    return 'added'


@app.route('/api/add_task', methods=['POST'])
@admin_required
@account_rep_required
def add_task():
    tasks = TaskService(
        request.form.get('customer_id'),
        admin_id = session.get('admin'),
        user = 'customer' if session['customer'] == True else 'admin'
    )
    tasks.post_task(
        request.form.get('task')
    )
    return 'added'

@app.route('/api/send_message', methods=['POST'])
@account_rep_required
def messages():
    customer_id = request.form.get('customer_id') if not session['customer'] else session['user']
    messaging = MessagingService(
        customer_id,
        admin_id = session.get('admin'),
        user = 'customer' if session['customer'] == True else 'admin'
    )
    messaging.post_message(request.form.get('msg'))

    return 'sent'

@app.route('/api/complete_task', methods=['POST'])
@admin_required
@account_rep_required
def complete_task():
    tasks = TaskService(
        request.form.get('customer_id'),
        admin_id = session.get('admin'),
        user = 'customer' if session['customer'] == True else 'admin'
    )
    tasks.complete_task(
        request.form.get('task')
    )
    return 'completed'

@app.route('/api/remove_task', methods=['POST'])
@admin_required
@account_rep_required
def remove_task():
    tasks = TaskService(
        request.form.get('customer_id'),
        admin_id = session.get('admin'),
        user = 'customer' if session['customer'] == True else 'admin'
    )
    tasks.remove_task(
        request.form.get('task')
    )
    return 'completed'
