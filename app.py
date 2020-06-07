import io

from flask import Flask

from controller.Search import searchApp
from controller.Tile import tileApp
from controller.S3Tile import s3tileApp

app = Flask(__name__)

app.register_blueprint(searchApp)
app.register_blueprint(tileApp)
app.register_blueprint(s3tileApp)

@app.after_request
def cors(environ):
    environ.headers['Access-Control-Allow-Origin'] = '*'
    environ.headers['Access-Control-Allow-Method'] = '*'
    environ.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    environ.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    environ.headers["Pragma"] = "no-cache"
    environ.headers["Expires"] = "0"
    return environ


@app.route('/')
def hello_world():
    return 'Hello, World!'
