
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

from routes.core_routes import *
from helpers.UserService import *
from helpers.ViewModels import ViewFuncs, IntakeViewModel, Admin_View
from helpers.LoginHandlers import *
import helpers.forms as forms
from routes.intake_routes import *
from routes.admin_routes import *
from helpers.helpers import *
import helpers.analysis as an
from routes.branding_routes import *
from helpers.filters import *
from passlib.hash import sha256_crypt


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', first=4, second=0,third=4), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('error.html', first=5, second=0,third=0), 500

if __name__ == '__main__':
	app.config.from_pyfile('config.cfg')
	app.run(debug=True)


