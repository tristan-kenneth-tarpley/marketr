from app import app
from flask import render_template, session, url_for, redirect
import stripe

class PaymentsService:
    def __init__(self):
        app.config.from_pyfile('config.cfg')
        self.sk = app.config['STRIPE_TEST_SK']
        self.pk = app.config['STRIPE_TEST_PK']
        self.success_url = 'http://127.0.0.1:5000/home'
        self.cancel_url = 'http://127.0.0.1:5000/logout'

    def almost_free(self):
        stripe.api_key = self.sk
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            subscription_data={
                'items': [{
                'plan': 'plan_FeZoBcEgfD35he',
                }],
            },
            success_url = self.success_url,
            cancel_url = self.cancel_url
        )
        self.id = session['id']
        

    def ab_plan(self):
        stripe.api_key = self.sk
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            subscription_data={
                'items': [{
                'plan': 'plan_Fed1YzQtnto2mT',
                }],
            },
            success_url = self.success_url,
            cancel_url = self.cancel_url
        )
        self.id = session['id']
    
    def paid_ads(self):
        stripe.api_key = self.sk
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            subscription_data={
                'items': [{
                'plan': 'plan_FecAlOmYSmeDK3',
                }],
            },
            success_url = self.success_url,
            cancel_url = self.cancel_url
        )
        self.id = session['id']