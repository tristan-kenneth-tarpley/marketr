from app import app
from flask import render_template, session, url_for, redirect
import stripe
import time

class PaymentsService:
    def __init__(self, email, customer_id=None):
        app.config.from_pyfile('config.cfg')
        self.sk = app.config['STRIPE_SK']
        self.pk = app.config['STRIPE_PK']
        self.success_url = 'https://marketr.life/success'
        self.cancel_url = 'https://marketr.life/logout'
        self.email = email
        self.customer_id = customer_id

    def modify(self, company_name=None):
        stripe.api_key = self.sk
        stripe.Customer.modify(
            self.customer_id,
            name=company_name
        )

    def delete_subscriptions(self, sub_id=None):
        stripe.api_key = self.sk
        stripe.Subscription.delete(sub_id)

    def send_invoice(self, invoice_id=None):
        stripe.api_key = self.sk
        stripe.Invoice.send_invoice(invoice_id)
        
    def get_customer(self):
        stripe.api_key = self.sk
        return stripe.Customer.retrieve(self.customer_id)
    # just returns id of active plans
    def get_plan(self):
        stripe.api_key = self.sk
        customer = stripe.Customer.retrieve(self.customer_id)
        plans = []
        for plan_parent in customer['subscriptions']['data']:
            plans.append(plan_parent['items']['data'][0]['plan']['id'])

        return plans

    def get_plan_meta(self, plan_id=None):
        stripe.api_key = self.sk
        return stripe.Subscription.retrieve(plan_id)

    # use this if you need more metadata about plans
    def fetch_plans(self):
        stripe.api_key = self.sk
        customer = stripe.Customer.retrieve(self.customer_id)
        plans = {}
        for i in range(len(customer['subscriptions']['data'])):
            plans[i] = {
                'nickname': customer['subscriptions']['data'][i]['plan']['nickname'],
                'plan_id': customer['subscriptions']['data'][i]['id'],
                'amount': (customer['subscriptions']['data'][i]['plan']['amount']/100)
            }
        return plans

    def invoices(self, sub_num=None):
        stripe.api_key = self.sk
        if not sub_num:
            return stripe.Invoice.list(customer=self.customer_id)
        else:
            return stripe.Invoice.list(customer=self.customer_id, subscription=sub_num)

    def upcoming_invoices(self):
        stripe.api_key = self.sk
        return stripe.Invoice.retrieve("upcoming", customer=self.customer_id).lines.list(limit=1)
        


    def create_customer(self, name=""):
        stripe.api_key = self.sk
        customer = stripe.Customer.create(
            description=f"Customer for {self.email}",
            email=self.email
        )
        return customer.id

    def poll(self):
        stripe.api_key = self.sk
        events = stripe.Event.list(type = 'checkout.session.completed', created = {
        # Check for events created in the last 24 hours.
            'gte': int(time.time() - 24 * 60 * 60),
        })

        for event in events.auto_paging_iter():
            session = event['data']['object']
            print(session)
        return session
            # Fulfill the purchase...

    def almost_free(self):
        stripe.api_key = self.sk
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            customer=self.customer_id,
            subscription_data={
                'items': [{
                'plan': 'plan_FfIAIrHBJ78YpY'
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
            customer=self.customer_id,
            subscription_data={
                'items': [{
                'plan': 'plan_FfI9OI02wob7Wl'
                }],
            },
            success_url = self.success_url,
            cancel_url = self.cancel_url
        )
        self.id = session['id']
        self.session = session
    
    def paid_ads(self):
        stripe.api_key = self.sk
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            customer=self.customer_id,
            subscription_data={
                'items': [{
                'plan': 'plan_FfI9ZGhlsAkGii'
                }],
            },
            success_url = self.success_url,
            cancel_url = self.cancel_url
        )
        self.id = session['id']