from flask import Flask, render_template, flash, request, url_for, flash, redirect, session, abort
import numpy as np
import pandas as pd
import urllib
import os
import json

app = Flask(__name__)


from db import db, sql_to_df
from routes import *
from helpers import *
import analysis as an


if __name__ == '__main__':
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SECRET_KEY'] = os.urandom(12)
    app.run(debug=True)