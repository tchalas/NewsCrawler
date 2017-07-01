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
import os

## read config
CONFIG = configparser.RawConfigParser()
CONFIG.read('./config.cfg')

def createdb(drop_first=True):
    """Creates the database."""
    if drop_first:
        db.drop_db()
    db.create_db()

def crawl(pages):
    """ Starts crawling """
    crawler_manager.crawl()

def serve():
    """ Start the Api """
    crawlApi.serve()


def test():
    #createdb(drop_first=True)
    """Runs unit tests"""
    tests = subprocess.call(['python', '-c', 'import tests; tests.run()'])
    sys.exit(tests)

if __name__ == "__main__":
   action = sys.argv[1]
   if action == "createdb":
       createdb()
   if action == "serve":
       serve()
   if action == "crawl":
       pages = sys.argv[2]
       crawl(pages)
   if action == "test":
       test()
