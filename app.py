from flask import Flask, render_template, flash, request, url_for, flash, redirect, session, abort
from flask_uploads import UploadSet, configure_uploads, IMAGES
import numpy as np
import pandas as pd
import urllib
import os
import json
from functools import wraps

app = Flask(__name__)

from db import db, sql_to_df, execute
from core_routes import *
from intake_routes import *
from helpers import *
import analysis as an


if __name__ == '__main__':
	app.config.from_pyfile('config.cfg')
	app.config.update(SECRET_KEY=os.urandom(12))
	app.run(debug=True)