from app import app, session, FlaskForm
from flask import request, render_template, redirect, url_for, flash
import services.helpers as helpers
import hashlib
import json
import pandas as pd
import asyncio
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
from services.Portfolio import Portfolio
from services.tools.campaign_creator import AdGrouper, MarketResearch, CopyWriter
from services.gamify import Achievements, Credits, Rewards
from services.BigQuery import GoogleORM
from services.RecService import RecommendationService, Recommendation
from services.WebListener import Listener
from services.CampaignManager import CampaignMetaManager
from services.WalletService import Wallet
from services.DashboardCompiler import compile_data_view
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

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

## market(r) index imports
from services.MarketrIndex import MarketrIndex, AdIndex, AdGroupIndex, CampaignIndex, BucketIndex, PortfolioIndex, compile_master
from services.OpportunitiesService import compile_topics

@app.route('/api/products', methods=['GET'])
def get_personas():
    customer_id = request.args.get('customer_id')
    query = "select name, p_id from product_list where customer_id = ? and name is not null"
    data, cursor = db.execute(query, True, (customer_id,))
    data = cursor.fetchall()

    returned = [{'product_name': row[0], 'p_id': row[1]} for row in data]
    return json.dumps(returned)

@app.route('/api/personas', methods=['GET'])
def get_products():
    customer_id = request.args.get('customer_id')
    #test
    query = "SELECT persona_name, audience_id from audience WHERE persona_name is not null and customer_id = ?"
    data, cursor = db.execute(query, True, (customer_id,))
    data = cursor.fetchall()
    returned = [{'persona_name': row[0], 'audience_id': row[1]} for row in data]
    return json.dumps(returned)

@app.route('/api/remove_product', methods=['POST'])
@admin_required
@account_rep_required
def remove_product():

    UserService.remove_product(request.form.get('product_name'))
    return 'added'


@app.route('/api/add_task', methods=['POST'])
def add_task():
    tasks = TaskService(
        request.form.get('customer_id') if request.form.get('customer_id') else session.get('user'),
        admin_id = session.get('admin'),
        user = 'customer' if session['customer'] == True else 'admin'
    )
    tasks.post_task(
        request.form.get('task'),
        tactic_id = request.form.get('tactic_id')
    )
    return 'added'

@app.route('/api/add_balance', methods=['POST'])
@login_required
def add_balance():
    amount = request.form['amount'].replace(',', '')
    payments = PaymentsService(session['email'], customer_id=session['stripe_id'])
    payments.add_balance(amount)
    UserService.add_balance(session['user'], amount)
    return redirect(url_for('settings'))

@app.route('/api/spend_rate', methods=['POST'])
@login_required
def spend_rate():
    spend_rate = request.form['spend_rate'].replace(',', '')
    UserService.set_spend_rate(session['user'], spend_rate)
    return redirect(url_for('settings'))

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
def complete_task():
    tasks = TaskService(
        request.form.get('customer_id') if request.form.get('customer_id') else session['user'],
        admin_id = session.get('admin'),
        user = 'customer' if session['customer'] == True else 'admin'
    )

    tasks.complete_task(
        request.form.get('task')
    )
    return 'completed'

@app.route('/api/incomplete_task', methods=['POST'])
def incomplete_task():
    tasks = TaskService(
        request.form.get('customer_id') if request.form.get('customer_id') else session['user'],
        admin_id = session.get('admin'),
        user = 'customer' if session['customer'] == True else 'admin'
    )

    tasks.incomplete_task(
        request.form.get('task')
    )
    return 'incomplete'

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
    notifications_list = json.dumps(notifications.get())
    if notifications_list:
        return notifications_list
    else:
        return None

@app.route('/api/backfall_ppc', methods=['GET'])
def backfall_ppc():
    comp = CompetitorService()
    return str(comp.backfall(request.args.get('url')))


@app.route('/api/poll_for_state', methods=['GET'])
@login_required
def poll_for_state():
    ach = Achievements(customer_id=session['user'])
    return json.dumps(ach.state())



@app.route('/api/drop', methods=['POST'])
def drop():
    req = request.get_json()
    reward_service = Rewards(customer_id=session['user'], email=session['email'])
    reward = reward_service.drop(req.get('type'))

    return json.dumps(reward)

@app.route('/api/claim', methods=['POST'])
@login_required
def claim():
    req = request.get_json()

    ach = Achievements(customer_id=session['user'])
    ach.acknowledge(achievement_id = req.get('achievement_id'))

    credits_system = Credits(customer_id=session['user'])
    amount = credits_system.update(req.get('amount'))
    returned = {
        'amount': amount
    }

    return json.dumps(returned)

@app.route('/api/rewards', methods=['GET'])
@login_required
def rewards():
    query = "select reward_title, cast(added as date) as added from rewards_log where customer_id = ? order by added desc"
    data, cursor = db.execute(query, True, (session['user'],))
    data = cursor.fetchall()
    returned = []
    for row in data:
        returned.append({
            'achievement': row[0],
            'date': str(row[1])
        })
    return json.dumps(returned)


@app.route('/api/spend_allocation', methods=['POST'])
def spend_allocation():
    req = request.get_json()
    revenue = req.get('revenue') if req.get('revenue') and req.get('revenue') > 100000 else 100000
    rec = GetRec(revenue, req.get('stage'), req.get('type'), 'saas', req.get('growth_needs'))
    budget = rec.get()

    viewed_budget = req.get('viewed_budget')
    if viewed_budget and viewed_budget != 'None':
        input_budget = float(str(viewed_budget).replace(",", ""))
    else:
        input_budget = budget

    user = req.get('customer_id')
    
    spend = SpendAllocation(
        user, revenue, input_budget,
        req.get('brand_strength'), req.get('growth_needs'), req.get('competitiveness'), 
        req.get('selling_to'), req.get('biz_model')
    )

    allocation = json.loads(spend.campaign_allocation())
    print(allocation)
    returned = {
        'budget': input_budget,
        'allocation': allocation,
        'recommended_budget': budget
    }
    return json.dumps(returned)

# @app.route('/api/portfolio_metrics', methods=['POST'])
# def portfolio_metrics():
#     req = request.get_json()
#     orm = GoogleORM(req.get('company_name'))
#     df = orm.agg()

#     portfolio = Portfolio(agg=df)
#     returned = portfolio.group()

#     return returned

@app.route('/api/portfolio/trend_line', methods=['POST'])
def portfolio_trends():
    req = request.get_json()
    orm = GoogleORM(req.get('company_name'))
    df = orm.agg()

    portfolio = Portfolio(agg=df)
    returned = portfolio.trendline()

    return returned


@app.route('/api/unclaimed_achievements', methods=['GET'])
@login_required
def get_achievements():
    ach = Achievements(customer_id=session['user'])
    return json.dumps(ach.count_unclaimed())

@app.route('/api/recommendations', methods=['POST'])
def new_recommendation():

    req = request.get_json()

    service = RecommendationService(customer_id=req.get('customer_id'), admin_id=req.get('admin_id'))

    title = req.get('title')
    body = req.get('body')

    if title is not None and body is not None:
        service.new(title=title, body=body)

    if req.get('outstanding') and req.get('outstanding') == True:
        return service.get_all_outstanding()
    else:
        return service.get_all()

    
@app.route('/api/outstanding_recs', methods=['POST'])
def outstanding_recs():
    req = request.get_json()
    service = RecommendationService(customer_id=req.get('customer_id'))

    return service.get_all_outstanding()

@app.route('/api/recommendation/delete', methods=['POST'])
def delete_rec():
    req = request.get_json()
    rec = Recommendation(customer_id=req.get('customer_id'), rec_id=req.get('rec_id'), admin_id=req.get('admin_id'))
    if rec.rec_id and rec.admin_id:
        rec.delete()

    return rec.get_all_outstanding()

@app.route('/api/recommendation/approve', methods=['POST'])
def approve_rec():
    try: 
        req = request.get_json()
        rec = Recommendation(customer_id=req.get('customer_id'), rec_id=req.get('rec_id'))
        rec.accept()
        result = 'success'

        google = GoogleChatService()
        google.rec_accepted(rec_id=req.get('rec_id'), user=req.get('customer_id'), company=session['company_name'], email=session['email'])
    except Exception as e:
        print(e)
        result = 'failure'

    return json.dumps({'result': result})

@app.route('/api/recommendation/dismiss', methods=['POST'])
def dismiss_rec():
    try:
        req = request.get_json()
        rec = Recommendation(customer_id=req.get('customer_id'), rec_id=req.get('rec_id'))
        rec.dismiss()
        result = 'success'

        google = GoogleChatService()
        google.rec_dismissed(rec_id=req.get('rec_id'), user=req.get('customer_id'), company=session['company_name'], email=session['email'])
    except Exception as e:
        print(e)
        result = 'error'

    return json.dumps({'result': result})


# intel
@app.route('/api/intel/listener', methods=['POST'])
def web_listen():
    req = request.get_json()
    listener = Listener(req.get('customer_id'), req.get('keywords'))

    due, result = listener.is_due()
    res = listener.listen() if due else result

    return res



#views


@app.route('/api/tactic_of_day', methods=['GET'])
@login_required
def tactic_of_day():
    service = TacticOfTheDay(session['user'])
    tactic = service.get()
    tasksservice = TaskService(session['user'], user='customer')
    tasks = tasksservice.get_tasks()
    return render_template('macros/components/tactics.html', base=tactic, tasks=tasks)


@app.route('/api/competitive_intel', methods=['POST'])
def get_competitors():
    req = request.get_json()
    comp = CompetitorService(req.get("customer_id"))

    return json.dumps(comp.competitor_card())

@app.route('/api/insights', methods=['POST'])
def insights():
    req = request.get_json()
    tup = (req.get('customer_id'),)
    query = "SELECT body, FORMAT(time, 'MM-dd-yyyy') as time, (select top 1 name from map_am(admin_id)) as name FROM insights WHERE customer_id = ? order by time desc"
    insights, cursor = db.execute(query, True, tup)
    insights = cursor.fetchall()
    returned = [{'body': row[0],'time': str(row[1]), 'admin': str(row[2])} for row in insights]
    return json.dumps(returned)

@app.route('/api/ranged_insights', methods=['POST'])
@login_required
def range_insights():
    req = request.get_json()
    tup = (req.get('customer_id'), req.get('start_date'), req.get('end_date'))
    query = "SELECT * FROM ranged_insights (?, ?, ?)"
    insights, cursor = db.execute(query, True, tup)
    insights = cursor.fetchall()
    returned = [{'body': row[0],'time': str(row[1])} for row in insights]
    return json.dumps(returned)
 


#tools 
@app.route('/api/create_campaign', methods=['POST'])
def create_campaign():
    req = request.get_json()
    keywords = req.get('keywords')
    market = MarketResearch()

    grouper = AdGrouper(market, keywords)
    groups = grouper.full_groups()

    for group in enumerate(groups):  
        try:
            ad_history = market.ad_history(group[1]['group'])

            if len(ad_history) > 0:
                ad_history = ad_history[ad_history.position < 10]
                ad_obj = CopyWriter()
                ads = ad_obj.Google(ad_history)
                if ads:
                    group[1].update(ads = [ad for ad in list(ads)])

        except Exception as e:
            print(e)
            continue

    return json.dumps(groups)


### spend queries ###
@app.route('/api/spend/last_7', methods=['POST'])
def last_7_spend():
    req = request.get_json()
    orm = GoogleORM(req.get('company_name'))
    spend = orm.cost_past_7()
    if spend is not None:
        spend = spend.cost.sum()
    else:
        spend = 0

    return json.dumps({
        'spend': spend
    })
    
    


### Market(r) index ### 
@app.route('/api/index/detailed', methods=['POST'])
def compile_master_index():
    req = request.get_json()
    demo = True if req.get('customer_id') == '181' else False
    date_range = req.get('date_range')
    ltv = float(req.get('ltv').replace(",", ""))
    company_name = req.get('company_name')
    run_social = req.get('facebook')
    run_search = req.get('google')

    dfs = compile_data_view(
        run_social=run_social,
        run_search=run_search,
        company_name=company_name,
        date_range=date_range,
        demo=demo,
        ltv=ltv
    )

    search_df = dfs.get('search_df')
    social_df = dfs.get('social_df')
    opps = dfs.get('topic_opps')

    compiled = compile_master(ltv=ltv, search_df=search_df, social_df=social_df)
    index = MarketrIndex(ltv)
    lcr = index.lcr(compiled.get('total_conversions'), compiled.get('total_clicks'))

    if opps is not None:
        topics = compile_topics(opps, index, lcr, ltv)
    else:
        topics = None

    returned = json.dumps({
        'topics': topics,
        'index': compiled
    })

    return returned

@app.route('/api/index/trendline', methods=['POST'])
def index_trendline():
    req = request.get_json()

    query = """
        select _index, convert(varchar(10), submitted, 120) as date from index_log where customer_id = ?
    """

    data, cursor = db.execute(query, True, (req.get('customer_id'),))
    data = cursor.fetchall()
    
    returned = list()
    if data:
        for row in data:
            returned.append({
                'index': row[0],
                'date': row[1]
            })

    return json.dumps(returned)


# @app.route('/api/index/trendline/view', methods=['POST'])
# def portfolio_view_func():
#     pass

@app.route('/api/campaigns', methods=['POST'])
def get_campaigns():
    req = request.get_json()
    company_name = req.get('company_name')
    orm = GoogleORM(company_name)
    campaigns = list()
    if req.get('google'):
        campaigns.append(orm.search_campaigns())
    if req.get('facebook'):
        campaigns.append(orm.social_campaigns())

    manager = CampaignMetaManager(req.get('customer_id'))
    
    return manager.group(campaigns)

@app.route('/api/claim_campaign', methods=['POST'])
def claim_campaign():
    req = request.get_json()
    manager = CampaignMetaManager(req.get('customer_id'))
    manager.claim(req.get('campaign_name'), req.get('customer_id'), req.get('campaign_id'), req.get('type'))

    return 'success'










### wallet

@app.route('/api/wallet/meta', methods=['POST'])
def wallet_meta():
    req = request.get_json()
    wallet = Wallet(req.get('customer_id'))

    return wallet.meta()

@app.route('/api/wallet/update', methods=['POST'])
def update_wallet():
    req = request.get_json()
    wallet = Wallet(req.get('customer_id'))
    try:
        wallet.update_balance(req.get('amount'))
        return json.dumps({'result': 200})
    except Exception as e:
        print(e)
        return json.dumps({'result': 500})