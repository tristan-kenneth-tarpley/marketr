
from flask import Flask, render_template, flash, request, url_for, flash, redirect, session, abort, send_from_directory, Blueprint
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_wtf import FlaskForm 
import numpy as np
import pandas as pd
import urllib
import os
import json
from functools import wraps

app = Flask(__name__, static_folder='static/public')

# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


# from helpers.UserService import *
# from helpers.ViewModels import *
# from helpers.LoginHandlers import *
import services.forms as forms
# from routes.branding_routes import *
# from routes.intake_routes import *
# from routes.admin_routes import *
from routes.oauth_routes import *
# from routes.core_routes import *
from routes.api_routes import *
from services.filters import *



if __name__ == '__main__':
	app.config.from_pyfile('config.cfg')
	app.run(use_reloader=True, debug=True)


