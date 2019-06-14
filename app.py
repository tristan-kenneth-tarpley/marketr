from flask import Flask, render_template, flash, request, url_for, flash, redirect, session, abort
from flask_uploads import UploadSet, configure_uploads, IMAGES
import numpy as np
import pandas as pd
import urllib
import os
import json
from functools import wraps

app = Flask(__name__)

from data.db import db, sql_to_df, execute
from routes.core_routes import *
from routes.intake_routes import *
from helpers.helpers import *
import helpers.analysis as an
from routes.branding_routes import *


if __name__ == '__main__':
	app.config.from_pyfile('config.cfg')
	app.run(debug=True)