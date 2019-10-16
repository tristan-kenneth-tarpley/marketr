
from flask import Flask, render_template, flash, request, url_for, flash, redirect, session, abort
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_wtf import FlaskForm 
import numpy as np
import pandas as pd
import urllib
import os
import json
from functools import wraps

app = Flask(__name__)

# from helpers.UserService import *
# from helpers.ViewModels import *
# from helpers.LoginHandlers import *
import services.forms as forms
from routes.branding_routes import *
from routes.intake_routes import *
from routes.admin_routes import *
from routes.core_routes import *
from services.filters import *

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', first=4, second=0,third=4), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', first=5, second=0,third=0), 500

if __name__ == '__main__':
	app.config.from_pyfile('config.cfg')
	app.run(debug=False)


