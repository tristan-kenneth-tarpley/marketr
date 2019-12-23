from app import app, session, FlaskForm
from flask import request, render_template, redirect, url_for, flash
import services.helpers as helpers
import hashlib
import json
from bleach import clean
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
from services.UserService import UserService
from services.NotificationsService import EmailService, GoogleChatService, NotificationsService
from services.CompetitorService import CompetitorService
from services.LoginHandlers import login_required, admin_required, owner_required, manager_required, account_rep_required, onboarding_required
from services.AdminService import AdminService, AdminActions, MessagingService, AdminUserService
from services.SharedService import MessagingService, TaskService, ScoreService, NotificationsService, CoreService, GoogleChatService
from services.PaymentsService import PaymentsService
from services.ChatService import ChatService
from services.AdSpend import GetRec, SpendAllocation
from services.tools.campaign_creator import AdGrouper, MarketResearch, CopyWriter
from services.gamify import Achievements, Credits, Rewards
from services.BigQuery import GoogleORM
from ViewModels.ViewModels import ViewFuncs, AdminViewModel, CustomerDataViewModel, SettingsViewModel, TacticViewModel, CompetitorViewModel, TacticOfTheDay
import hashlib
import data.db as db
from bleach import clean
from flask_mail import Mail, Message
from passlib.hash import sha256_crypt
import services.forms as forms
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
import time
import datetime


@app.route('/sitemap', methods=['GET'])
def sitemap():
    return render_template('sitemap.xml')

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

    data, cursor = db.execute(query, True, tup)

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
		home=True,
        quantity = request.args.get('quantity') if request.args.get('quantity') else 1
	)

@app.route('/inspect')
def inspect():
    service = PaymentsService(None, customer_id='cus_Fg7dwInveMv4wX')
    customer = service.get_plan_meta(plan_id='sub_FhE3gUPeN4xjE4') 
    return json.dumps(customer)


@app.route('/checkout/single_campaign', methods=['GET', 'POST'])
@login_required
def single_campaign():
    obj = PaymentsService(session['email'], customer_id = session['stripe_id'])
    quantity = request.args.get('quantity') if request.args.get('quantity') else 1
    obj.single_campaign(quantity=quantity)

    if request.args.get('session_id'):
        return render_template('core/checkout.html', plan="ab")
    else:
        return redirect(url_for('single_campaign', session_id=obj.id, quantity=quantity))



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

@app.route('/checkout/paid_ads_premium', methods=['GET', 'POST'])
@login_required
def paid_ads_premium_checkout():
    obj = PaymentsService(session['email'], customer_id = session['stripe_id'])
    obj.paid_ads_premium()
    if request.args.get('session_id'):
        return render_template('core/checkout.html', plan="ads_premium")
    else:
        return redirect(url_for('paid_ads_premium_checkout', session_id=obj.id))

# anchor
@app.route('/Xr8FcPcNQsvTEJ3kuznY')
def success():
    # get plan id
    email = session['email'] if session['logged_in'] else request.args.get('email')
    customer_id = session['stripe_id'] if session['logged_in'] else request.args.get('stripe_id')
    payments = PaymentsService(session['email'], customer_id = session['stripe_id'])
    gchat = GoogleChatService()
    plans = payments.get_plan()
    for plan in plans:
        gchat.new_customer(email=session['email'], customer_type=plan)
        # update db with plan id
        UserService.update_plan(session['user'], plan)

    UserService.init_profile_after_purchase(UserService.now(), session['user'])

    # redirect to home
    return redirect(url_for('home', view='campaigns'))

@app.route('/cancel')
def cancel():
    return 'cancelled'

@app.route('/schedule')
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
    # data = GoogleORM('musicmaker')
    # campaign.google_meta()
    view_model = CustomerDataViewModel(customer_id=session['user'], init=True)
    chat = ChatService('User', session['email'], session['user'])
    chat.run()
    return render_template(
        'layouts/home_layout.html',
        page=view_model,
        chat=chat
    )

# @app.route('/home_test', methods=['GET', 'POST'])
# @login_required
# @onboarding_required
# def home_test():
#     view_model = CustomerDataViewModel(customer_id=session['user'], init=True)
#     return render_template(
#         'layouts/home_layout_2.html',
#         page=view_model
#     )

@app.route('/home/achievements', methods=['GET', 'POST'])
@login_required
@onboarding_required
def achievements():
    view_model = CustomerDataViewModel(customer_id=session['user'], init=True)
    return render_template(
        'layouts/gamification_layout.html',
        page=view_model
    )


@app.route('/home/settings', methods=['GET', 'POST'])
@login_required
def settings():
    page = SettingsViewModel(session['email'], customer_id=session['user'], stripe_id=session['stripe_id'])
    return render_template(
        'core/settings.html', page=page,
        root=True
    )

@app.route('/home/settings/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    pw_form = forms.ChangePassword()
    if request.method == 'POST' and pw_form.validate_on_submit():
        result = UserService.update_password(pw_form.current_password.data, pw_form.password.data, session['user'])
        if result == True:
            return redirect(url_for('change_password', success=True))
        else:
            return render_template(
                'core/change_password.html',
                success=False if not request.args.get('success') else True,
                root=False, pw_form=pw_form, message=result
            )

    return render_template(
        'core/change_password.html',
        success=False if not request.args.get('success') else True,
        root=False, pw_form=pw_form
    )




@app.route('/home/settings/<plan_id>', methods=['GET', 'POST'])
@login_required
def plan_view(plan_id):
    page = SettingsViewModel(
        session['email'],
        customer_id=session['user'],
        stripe_id=session['stripe_id'],
        root=False,
        sub_id = plan_id
    )

    if request.method == 'POST':
        if request.form['cancel_sub']:
            payments = PaymentsService(session['email'], customer_id=session['stripe_id'])
            payments.delete_subscriptions(
                sub_id = plan_id,
                customer_id = session['stripe_id']
            )
            return redirect(url_for('settings'))
    
        # if request.form['send_invoice']:
        #     payments = PaymentsService(session['email'], customer_id=session['stripe_id'])
        #     payments.send_invoice(invoice_id=request.form['invoice_id'])
        #     return redirect(url_for('plan_view', plan_id=request.form['plan_id']))

    return render_template('core/settings.html', page=page, root=False, plan_id=plan_id)


@app.route('/tactic/<tactic_id>', methods=['GET'])
@login_required
@onboarding_required
def tactic(tactic_id):

    vm = TacticViewModel(tactic_id)
    vm.compile()
    return render_template(
        'core/tactics.html',
        page=vm
    )

@app.route('/audit/<url>', methods=['GET'])
def audit(url):
    query = """SELECT
                audit_string,
                (select audit_string from audit_results WHERE url = ar.comp_1) as comp_1,
                (select audit_string from audit_results WHERE url = ar.comp_2) as comp_2,
                (select audit_string from audit_results WHERE url = ar.comp_3) as comp_3,
                (select top 3 title, description from join_tactics where tag_val like '%any%' ORDER BY NEWID() for json path, root('tactics'))
                as tactics

                FROM audit_results as ar WHERE url = ?
            """
    results, cursor = db.execute(query, True, (url,))
    results = cursor.fetchone()
    page = eval(results[0])
    if results[1]:
        competitors = [eval(results[1]), eval(results[2]), eval(results[3])]
    else:
        competitors = None
    tactics = eval(results[4])
    return render_template(
        'branding/audit.html',
        page=page,
        competitors=competitors if competitors else None,
        tactics=tactics
    )





@app.route('/audit_request', methods=['POST'])
def audit_request():
    google = GoogleChatService()
    post_url = request.form.get('url')
    post_email = request.form.get('email')
    url = clean('https://' + request.form.get('url').replace('https://', '')) if post_url else 'error'
    email = clean(request.form.get('email')) if post_email else 'error'
    google.audit_request(url, email)
    return 'success'




@app.route('/error', methods=['POST'])
@login_required
def error_log():
    google = GoogleChatService()
    google.error(request.form['type'], session['user'])
    return 'success'



@app.route('/google_test', methods=['GET'])
def google():
    
    return 'success'


