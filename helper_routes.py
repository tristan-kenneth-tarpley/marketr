from app import *
from core_routes import *
from intake_routes import *
from helpers import *
from classes import *
from data.cities import cities

@app.route('/cities', methods=['GET'])
def cities():
	if request.method == "GET":
		return cities

