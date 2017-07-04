import time
import json
import unittest
import crawler.crawler_tasks as crawler_tasks
import configparser
import psycopg2
import datetime
import requests
from api.crawler_client import CrawlerClient
from bs4 import BeautifulSoup

## read config
CONFIG = configparser.RawConfigParser()
CONFIG.read('./config.cfg')

# get values from config file
db_section = "testdb"

# get values from config file
dbname = CONFIG.get(db_section, 'dbname')
dbuser = CONFIG.get(db_section, 'dbuser')
dbpassword = CONFIG.get(db_section, 'dbpassword')
dbhost = CONFIG.get(db_section, 'dbhost')

# Mock the html response and test the soup production
class ApiTests(unittest.TestCase):

    conn = None
    cur = None
    crawler_client =  None

    def setUp(self):
        self.crawler_client = CrawlerClient()
        self.conn = psycopg2.connect(dbname=dbname, user=dbuser, host=dbhost, password=dbpassword)
        self.cur = self.conn.cursor()
        i = 0;
        while i < 4:
            username = "testuser1"
            post_id = "testpost" + str(i)
            comment_id = "testcomment" + str(i)
            votes = i
            i = i + 1
            self.cur.execute('INSERT INTO "reddit-user" (username) VALUES (%s) ON CONFLICT (username) DO NOTHING',(username, ))
            self.cur.execute('INSERT INTO "reddit-post" (post_id, username, score) \
                         VALUES (%s, %s, %s) ON CONFLICT (post_id) DO NOTHING', (post_id, username, votes,))
            self.cur.execute('INSERT INTO "reddit-comment" (comment_id, username, votes, post_id) \
                                     VALUES (%s, %s, %s, %s) ON CONFLICT (comment_id) DO NOTHING ', \
                                     (comment_id, username, votes, post_id,))
        self.conn.commit()
        while i < 7:
            username = "testuser2"
            post_id = "testpost" + str(i)
            comment_id = "testcomment" + str(i)
            votes = i
            i = i + 1
            self.cur.execute('INSERT INTO "reddit-user" (username) VALUES (%s) ON CONFLICT (username) DO NOTHING',(username, ))
            self.cur.execute('INSERT INTO "reddit-post" (post_id, username, score) \
                         VALUES (%s, %s, %s) ON CONFLICT (post_id) DO NOTHING', (post_id, username, votes,))
            self.cur.execute('INSERT INTO "reddit-comment" (comment_id, username, votes, post_id) \
                                     VALUES (%s, %s, %s, %s) ON CONFLICT (comment_id) DO NOTHING ', \
                                     (comment_id, username, votes, post_id,))
        self.conn.commit()

        while i < 9:
            username = "testuser3"
            post_id = "testpost" + str(i)
            comment_id = "testcomment" + str(i)
            votes = i
            i = i + 1
            self.cur.execute('INSERT INTO "reddit-user" (username) VALUES (%s) ON CONFLICT (username) DO NOTHING',(username, ))
            self.cur.execute('INSERT INTO "reddit-post" (post_id, username, score) \
                         VALUES (%s, %s, %s) ON CONFLICT (post_id) DO NOTHING', (post_id, username, votes,))
            self.cur.execute('INSERT INTO "reddit-comment" (comment_id, username, votes, post_id) \
                                     VALUES (%s, %s, %s, %s) ON CONFLICT (comment_id) DO NOTHING ', \
                                     (comment_id, username, votes, post_id,))
        self.conn.commit()

        while i < 10:
            username = "testuser4"
            post_id = "testpost" + str(i)
            comment_id = "testcomment" + str(i)
            votes = i
            i = i + 1
            self.cur.execute('INSERT INTO "reddit-user" (username) VALUES (%s) ON CONFLICT (username) DO NOTHING',(username, ))
            self.cur.execute('INSERT INTO "reddit-post" (post_id, username, score) \
                         VALUES (%s, %s, %s) ON CONFLICT (post_id) DO NOTHING', (post_id, username, votes,))
            self.cur.execute('INSERT INTO "reddit-comment" (comment_id, username, votes, post_id) \
                                     VALUES (%s, %s, %s, %s) ON CONFLICT (comment_id) DO NOTHING ', \
                                     (comment_id, username, votes, post_id,))
        self.conn.commit()

    #add stuff to the testdb and test output
    def test_posts_by_user(self):
        res = self.crawler_client.get_posts_by_user("testuser1")
        self.assertEqual(res,[({'posted': None, 'score': 0, 'url': None, 'title': None, 'domain': None, 'comments_count': None, 'post_id': 'testpost0', 'username': 'testuser1'},), ({'posted': None, 'score': 1, 'url': None, 'title': None, 'domain': None, 'comments_count': None, 'post_id': 'testpost1', 'username': 'testuser1'},), ({'posted': None, 'score': 2, 'url': None, 'title': None, 'domain': None, 'comments_count': None, 'post_id': 'testpost2', 'username': 'testuser1'},), ({'posted': None, 'score': 3, 'url': None, 'title': None, 'domain': None, 'comments_count': None, 'post_id': 'testpost3', 'username': 'testuser1'},)])

    def test_top_submitter(self):
        res = self.crawler_client.get_top_submitter()
        self.assertEqual(res, [('testuser1', 4)])

    def test_top_commenter(self):
        res = self.crawler_client.get_top_commenter()
        self.assertEqual(res, [('testuser1', 4)])

    def test_top_posts_by_poins(self):
        res = self.crawler_client.get_top_posts_by_poins("all")
        self.assertEqual(res, [({'post_id': 'testpost9', 'posted': None, 'comments_count': None, 'score': 9, 'title': None, 'domain': None, 'username': 'testuser4', 'url': None},), ({'post_id': 'testpost8', 'posted': None, 'comments_count': None, 'score': 8, 'title': None, 'domain': None, 'username': 'testuser3', 'url': None},), ({'post_id': 'testpost7', 'posted': None, 'comments_count': None, 'score': 7, 'title': None, 'domain': None, 'username': 'testuser3', 'url': None},), ({'post_id': 'testpost6', 'posted': None, 'comments_count': None, 'score': 6, 'title': None, 'domain': None, 'username': 'testuser2', 'url': None},), ({'post_id': 'testpost5', 'posted': None, 'comments_count': None, 'score': 5, 'title': None, 'domain': None, 'username': 'testuser2', 'url': None},), ({'post_id': 'testpost4', 'posted': None, 'comments_count': None, 'score': 4, 'title': None, 'domain': None, 'username': 'testuser2', 'url': None},), ({'post_id': 'testpost3', 'posted': None, 'comments_count': None, 'score': 3, 'title': None, 'domain': None, 'username': 'testuser1', 'url': None},), ({'post_id': 'testpost2', 'posted': None, 'comments_count': None, 'score': 2, 'title': None, 'domain': None, 'username': 'testuser1', 'url': None},), ({'post_id': 'thing_t3_6ka9lv', 'posted': '2017-06-29T18:24:00', 'comments_count': 1, 'score': 1, 'title': 'Help With Programming Around APFS', 'domain': 'self.Python', 'username': 'pinkysooperfly', 'url': '/r/Python/comments/6ka9lv/help_with_programming_around_apfs/'},), ({'post_id': 'testpost1', 'posted': None, 'comments_count': None, 'score': 1, 'title': None, 'domain': None, 'username': 'testuser1', 'url': None},)])

    def tearDown(self):
        self.cur.close()
        self.conn.close()
