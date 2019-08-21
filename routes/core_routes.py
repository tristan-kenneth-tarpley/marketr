from app import app, session, FlaskForm
from flask import request, render_template, redirect, url_for, flash
import services.helpers as helpers
import hashlib
import json
from bleach import clean
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
from services.UserService import UserService, EmailService
from services.CompetitorService import CompetitorService
from services.LoginHandlers import login_required, admin_required, owner_required, manager_required, account_rep_required, onboarding_required
from services.AdminService import AdminService, AdminActions, MessagingService, AdminUserService
from services.SharedService import MessagingService, TaskService, ScoreService, NotificationsService, CoreService
from services.PaymentsService import PaymentsService
from ViewModels.ViewModels import ViewFuncs, AdminViewModel, CustomerDataViewModel
import hashlib
from data.db import execute, sql_to_df
from bleach import clean
from flask_mail import Mail, Message
from passlib.hash import sha256_crypt
import services.forms as forms
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
import time
import datetime


@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    form = forms.ForgotPassword()

    if ViewFuncs.ValidSubmission(form=form, method=request.method):
        email = EmailService()
        email.send_email_reset(form.email.data)
        message_sent = "Your password reset link has been sent! If there is an account associated with that email, you should see it any moment."
        return render_template('forgot.html', form=form, send=True, message_sent=message_sent)

    elif request.method == 'GET':
        session['logged_in'] = False

    return render_template('forgot.html', form=form, send=True)



@app.route('/forgot_password/<token>', methods=['GET', 'POST'])
def update_password(token):
    form = forms.UpdatePassword()

    if ViewFuncs.ValidSubmission(form=form, method=request.method):
        email = EmailService()
        email.update_password(form.password.data, token=token)
        return redirect(url_for('customer_login', conf=True))
    try:
        return render_template("change_pass.html", pass_step=True, form=form, token=token, send=False, conf=False, reset=False)
    except:
        return redirect(url_for('customer_login', expired=True))


    

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
    UserService.confirm_customer(email, token)
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


# payments

@app.route('/pricing')
def pricing():
    return render_template(
		'branding/pricing.html',
		logged_in = True if session.get('logged_in') == True else False,
		home=True
	)

@app.route('/inspect')
def inspect():
    service = PaymentsService(None, customer_id='cus_FfIDeTFMXFCZWG')
    customer = service.get_customer() 
    return json.dumps(customer)

@app.route('/checkout/ab_testing', methods=['GET', 'POST'])
@login_required
def ab_checkout():
    obj = PaymentsService(session['email'], customer_id = session['stripe_id'])
    obj.ab_plan()
    if request.args.get('session_id'):
        return render_template('core/checkout.html', plan="ab")
    else:
        return redirect(url_for('ab_checkout', session_id=obj.id))

@app.route('/checkout/almost_free', methods=['GET', 'POST'])
@login_required
def free_checkout():
    obj = PaymentsService(session['email'], customer_id = session['stripe_id'])
    obj.almost_free()
    if request.args.get('session_id'):
        return render_template('core/checkout.html', plan="free")
    else:
        return redirect(url_for('free_checkout', session_id=obj.id))

@app.route('/checkout/paid_ads', methods=['GET', 'POST'])
@login_required
def ads_checkout():
    obj = PaymentsService(session['email'], customer_id = session['stripe_id'])
    obj.paid_ads()
    if request.args.get('session_id'):
        return render_template('core/checkout.html', plan="ads")
    else:
        return redirect(url_for('ads_checkout', session_id=obj.id))


@app.route('/success')
def success():
    # get plan id
    email = session['email'] if session['logged_in'] else request.args.get('email')
    customer_id = session['stripe_id'] if session['logged_in'] else request.args.get('stripe_id')
    payments = PaymentsService(session['email'], customer_id = session['stripe_id'])
    plan_id = payments.get_plan()
    # update db with plan id
    UserService.update_plan(session['user'], plan_id)
    # redirect to home
    # return plan_id
    return redirect(url_for('home', view='campaigns'))

@app.route('/cancel')
def cancel():
    return 'cancelled'

@app.route('/schedule')
@login_required
def schedule():
    return render_template('core/schedule.html')

# home actions
@app.route('/expectations')
@login_required
@onboarding_required
def expectations():
    return render_template('core/expectations.html')


@app.route('/customer_core', methods=['GET'])
def customer_core():
    service = CustomerDataViewModel(customer_id=request.args.get('customer_id'))
    return_data = service.compile_core()
    return json.dumps(return_data)


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
        request.args.get('task')
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

@app.route('/api/marketr_score', methods=['GET'])
@login_required
def marketr_score():
    user = session['user'] if session['customer'] == True else request.args.get('customer_id')
    score = ScoreService(user)
    return score.get()

@app.route('/api/notifications', methods=['GET'])
@login_required
def notifications():
    user = session['user'] if session['customer'] == True else request.args.get('customer_id')
    notifications = NotificationsService(user)
    return json.dumps(notifications.get())
