import configparser
import time
from api.crawl_api import crawl_api
from flask import Flask, request, abort, Response, jsonify, g
from flask_restful import Api
import flask_profiler

## READ CONFIG
CONFIG = configparser.RawConfigParser()
CONFIG.read('./config.cfg')

HOST = CONFIG.get('flask', 'host')
PORT = int(CONFIG.get('flask', 'port'))

APP = Flask(__name__)
# flask-profiler config as follows:
APP.config["flask_profiler"] = {
        "enabled": True,
        "storage": {
            "engine": "sqlite"
        },
        "basicAuth":{
            "enabled": True,
            "username": "admin",
            "password": "admin"
        },
        "ignore": [
    	    "^/static/.*"
    	]
}
flask_profiler.init_app(APP)

API = Api(app=APP, default_mediatype="application/json")
APP.register_blueprint(crawl_api)

def serve():
    APP.run(host=HOST, port=PORT)
