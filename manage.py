#Outside manager of the App
import subprocess
import sys
import os, shutil
from flask_script import Manager
import db.setup as db
import api.app as crawlApi
import crawler
import crawler.crawler_manager as crawler_manager
import configparser
import tests
import os

## read config
CONFIG = configparser.RawConfigParser()
CONFIG.read('./config.cfg')

def createdb(drop_first=True):
    """Creates the database."""
    print("db")
    if drop_first:
        db.drop_db()
    db.create_db()

def crawl(pages):
    """ Starts crawling """
    crawler_manager.crawl(pages)

def serve():
    """ Start the Api """
    crawlApi.serve()


def test():
    createdb(drop_first=True)
    """Runs unit tests"""
    tests.run()
    CONFIG.set('default', 'env', 'dev')
    with open('config.cfg', 'w') as configfile:
        CONFIG.write(configfile)

if __name__ == "__main__":

    action = sys.argv[1]
    print(action)
    if action == "createdb":
        print(action)
        createdb()
    if action == "serve":
        serve()
    if action == "crawl":
        pages = sys.argv[2]
        crawl(pages)
    if action == "test":
        test()
