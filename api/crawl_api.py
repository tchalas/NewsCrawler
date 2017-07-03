import json
from flask import Blueprint, request, session, abort, jsonify
from api.CrawlerClient import CrawlerClient

crawl_api = Blueprint('crawl_api', __name__, url_prefix='/crawl_api')
client = CrawlerClient()

@crawl_api.route("/top10points/<post_type>", methods=['GET'])
def top10points(post_type):
    return jsonify(client.get_top_posts_by_poins(post_type))

@crawl_api.route("/top10commented/<post_type>", methods=['GET'])
def top10commented(post_type):
    return jsonify(client.get_top_posts_by_comments(post_type))

@crawl_api.route("/topsubmitter", methods=['GET'])
def topsubmitter():
    return jsonify(client.get_top_submitter())

@crawl_api.route("/topcommenter", methods=['GET'])
def topcommenter():
    return jsonify(client.get_top_commenter())

@crawl_api.route("/mostactive", methods=['GET'])
def mostactive():
    return jsonify(client.get_most_active_user())
