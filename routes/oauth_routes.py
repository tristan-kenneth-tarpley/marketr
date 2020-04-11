from app import app, session, FlaskForm
from flask import request, render_template, redirect, url_for, flash
import services.helpers as helpers
from flask import jsonify
from bleach import clean
import json
import data.db as db
from urllib.parse import quote, urlencode
import requests

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

        
