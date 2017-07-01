import json
from flask import Blueprint, request, session, abort, jsonify
from api.CrawlerClient import CrawlerClient

crawl_api = Blueprint('crawl_api', __name__, url_prefix='/crawl_api')
client = CrawlerClient()

@crawl_api.route("")
def init():
    return jsonify(client.get_top_posts())
