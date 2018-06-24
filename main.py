from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
	return app.send_static_file('index.html')

@app.route('/icons')
def icons():
	return app.send_static_file('icons.html')

if __name__ == '__main__':
	app.run()