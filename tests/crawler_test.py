import time
import json
import unittest
import crawler.crawler_tasks as crawler_tasks
import configparser
import psycopg2
import datetime
import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0"}

html_strings = "tests/html_collection"
comments_html = "tests/comments_html"


## read config
CONFIG = configparser.RawConfigParser()
CONFIG.read('./config.cfg')

# get values from config file
db_section = "db"
env = CONFIG.get('default', 'env')

if env == "test":
    db_section = "testdb"

# get values from config file
dbname = CONFIG.get(db_section, 'dbname')
dbuser = CONFIG.get(db_section, 'dbuser')
dbpassword = CONFIG.get(db_section, 'dbpassword')
dbhost = CONFIG.get(db_section, 'dbhost')

# Mock the html response and test the soup production
class CrawlerTests(unittest.TestCase):

    conn = None
    cur = None

    def setUp(self):
        self.conn = psycopg2.connect(dbname=dbname, user=dbuser, host=dbhost, password=dbpassword)
        self.cur = self.conn.cursor()

    def test_01(self):
        #conn = psycopg2.connect(dbname=dbname, user=dbuser, host=dbhost, password=dbpassword)
        with open(html_strings) as f:
            content = f.readlines()
            content = [x.strip() for x in content]
            rst = crawler_tasks.craw_post(str(content))
            res = self.cur.execute('select * FROM "reddit-post";')
            res = self.cur.fetchone()
        t = ('thing_t3_6ka9lv', 'pinkysooperfly', 'self.Python', 1, 1, 'Help With Programming Around APFS', '/r/Python/comments/6ka9lv/help_with_programming_around_apfs/', datetime.datetime(2017, 6, 29, 18, 24))
        self.assertEqual(t,res);

    def test_02(self):
        r  = requests.get("https://www.reddit.com/r/Python/comments/6ka9lv/help_with_programming_around_apfs", headers=HEADERS)
        s = r.text
        t = ('thing_t1_djkmdyz', 3, 'mrvkino', 'thing_t3_6ka9lv')
        comments_soup = BeautifulSoup(s, "html.parser")
        rst = crawler_tasks.craw_comments(comments_soup.decode(),"thing_t3_6ka9lv", "https://www.reddit.com/r/Python/comments/6ka9lv/help_with_programming_around_apfs")
        res = self.cur.execute('select * FROM "reddit-comment";')
        res = self.cur.fetchone()
        self.assertEqual(t,res);

    def tearDown(self):
        self.cur.close()
        self.conn.close()
