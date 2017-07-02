import json
import unittest
import crawler.crawler_tasks as crawler_tasks
import configparser
import psycopg2
import datetime

html_strings = "tests/html_collection"

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
        print("setup")
        print(dbname)
        self.conn = psycopg2.connect(dbname=dbname, user=dbuser, host=dbhost, password=dbpassword)
        self.cur = self.conn.cursor()

    def test_craw_post_task(self):
        a = 1;
        with open(html_strings) as f:
            content = f.readlines()
            content = [x.strip() for x in content]
            rst = crawler_tasks.craw_post(str(content))
            res = self.cur.execute('select * FROM "reddit-post";')
            res = self.cur.fetchone()
        t = ('thing_t3_6ka9lv', 'pinkysooperfly', 'self.Python', 1, 1, 'Help With Programming Around APFS', '/r/Python/comments/6ka9lv/help_with_programming_around_apfs/', datetime.datetime(2017, 6, 29, 18, 24))
        self.assertEqual(t,res);

    def tearDown(self):
        self.conn.close()
