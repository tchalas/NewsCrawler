import json
from flask import Blueprint, request, session, abort, jsonify

crawl_api = Blueprint('crawl_api', __name__, url_prefix='/crawl_api')

@crawl_api.route("")
def init():
    return "yo"
