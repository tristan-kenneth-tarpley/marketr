from app import app, session, FlaskForm
from flask import request, render_template, redirect, url_for, flash
import services.helpers as helpers
from flask import jsonify
from bleach import clean
import json
import data.db as db
from urllib.parse import quote, urlencode
import requests


fb_access_token = access_token = 'EAAB18Dy3CA8BAJRAjpZCvRfltVZBvTFZAKolXjlYFdUW9djFyRc5nJ7ASPoEq0nIgmoUvoWaOrUZBG3q8klYMVuidl8HK207qcNYdJbZAg25OfcpXSZCpdVj72aZBlGLargokVKsimxZAMkOKg9SksECR2djNrlZAKeaNuQ0sKb616Bb4ntAhfOiXOStsKgHDemrUpKzJzbyJpwXdY7yB2zZCM'
marketr_bizm_id = '243210706157899'
arc_inc_bizm_id = '2066184430264474'

@app.route('/auth/facebook_business_manager', methods=['GET', 'POST'])
def facebook_bm():
    
    relationship_edge_url = f"https://graph.facebook.com/v4.0/{marketr_bizm_id}/managed_businesses?existing_client_business_id={marketr_bizm_id}&access_token={marketr_bizm_id}"
    user_access_token = f"https://graph.facebook.com/v4.0/<MERCHANTS_BM_ID>/access_token?scope=ads_management,manage_pages&app_id=<APP_ID>&access_token=<USER_ACCESS_TOKEN|PARTNER_BM_ADMIN_SYSTEM_USER_ACCESSS_TOKEN>&system_user_name=<optional SU name>"

    return relationship_edge_url


linkedin_secret = 'OAozBy1Xy217oHeY'
linkedin_client_id = '781vh6v82vnuy3'
state = '781vh6v82vnuy3'
linkedin_callback_url = "https://marketr.life/auth/linkedin/callback"


@app.route('/auth/linkedin', methods=['GET', 'POST'])
def linkedin():
    endpoint = 'https://www.linkedin.com/oauth/v2/authorization'
    params = {
        'response_type': 'code',
        'client_id': linkedin_client_id,
        'redirect_uri': linkedin_callback_url,
        'state': state,
        'scope': 'r_emailaddress r_ads rw_ads r_ads_reporting'
    }
    url = f"{endpoint}?{urlencode(params)}"

    return redirect(url)

  
@app.route('/auth/linkedin/callback', methods=['GET', 'POST'])
def linkedin_callback():
    _state = request.args.get('state')
    if state == _state:
        code = request.args.get('code')
        endpoint = '/oauth/v2/accessToken'
        host = 'https://www.linkedin.com'
        
        payload = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': linkedin_callback_url,
            'client_id': linkedin_client_id,
            'client_secret': linkedin_secret
        }

        r = requests.post(
            host+endpoint,
            data=payload,
            headers={
                "Content-Type": "application/x-www-form-urlencoded"
            }
        )
        res = r.json()
        access_token = json.dumps(res)
        return json.dumps(payload) + "\n" + access_token

    else:
        return "state error"

        
