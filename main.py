from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
  return app.send_static_file('index.html')

@app.route('/icons')
def 

if __name__ == '__main__':
  app.run()