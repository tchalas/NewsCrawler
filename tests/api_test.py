import time
import json
import unittest
import crawler.crawler_tasks as crawler_tasks
import configparser
import psycopg2
import datetime
import requests
from bs4 import BeautifulSoup

# Mock the html response and test the soup production
class CrawlerTests(unittest.TestCase):

    conn = None
    cur = None

    def setUp(self):
        self.conn = psycopg2.connect(dbname=dbname, user=dbuser, host=dbhost, password=dbpassword)
        self.cur = self.conn.cursor()

    #add stuff to the testdb and test output
    def test_01(self):
