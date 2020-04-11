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
        'scope': 'r_emailaddress r_ads w_organization_social rw_ads r_basicprofile r_liteprofile r_ads_reporting r_organization_social rw_organization_admin w_member_social r_1st_connections_size'
    }
    url = f"{endpoint}?{urlencode(params)}"

    return redirect(url)

  
@app.route('/auth/linkedin/callback', methods=['GET', 'POST'])
def linkedin_callback():
    _state = request.args.get('state')
    if state == _state:
        code = request.args.get('code')
        endpoint = '/oauth/v2/accessToken'
        host = 'www.linkedin.com'
        
        payload = {
            "Content-Type": "application/x-www-form-urlencoded",
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': linkedin_callback_url,
            'client_id': linkedin_client_id,
            'client_secret': linkedin_secret
        }

        r = requests.post(
            host+endpoint,
            data=json.dumps(payload),
            headers={}
        )

        res = r.json()
        access_token = res.get('access_token')
        return access_token



        
