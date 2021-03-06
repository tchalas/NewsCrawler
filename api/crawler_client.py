import configparser
import psycopg2
from db.db_client import DBClient

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

class CrawlerClient(object):
    conn = None
    cur = None
    db_client = None

    def __init__(self):
        self.db_client = DBClient()

    def get_top_posts_by_poins(self, post_type):
        query = None
        data = None
        if(post_type == "all"):
            query = 'select row_to_json("reddit-post") FROM "reddit-post" order by score desc limit 10;'
            params = ('', )
        elif(post_type == "discussion"):
            query = 'select row_to_json("reddit-post") FROM "reddit-post" where domain = %s OR domain = %s order by score desc limit 10;'
            params = ("self.Python", "i.redd.it", )
        else:
            query = 'select row_to_json("reddit-post") FROM "reddit-post" where domain != %s AND domain != %s order by score desc limit 10;'
            params = ("self.Python", "i.redd.it", )
        res = self.db_client.query_all(query, params)
        return res

    def get_top_posts_by_comments(self, post_type):
        print(dbname)
        query = None
        data = None
        if(post_type == "all"):
            query = 'select row_to_json("reddit-post") FROM "reddit-post" order by comments_count desc limit 10;;'
            params = ('', )
        elif(post_type == "discussion"):
            query = 'select row_to_json("reddit-post") FROM "reddit-post" where domain = %s OR domain = %s order by comments_count desc limit 10;'
            params = ("self.Python", "i.redd.it", )
        else:
            query = 'select row_to_json("reddit-post") FROM "reddit-post" where domain != %s AND domain != %s order by comments_count desc limit 10;'
            params = ("self.Python", "i.redd.it", )
        res = self.db_client.query_all(query, params)
        return res

    def get_top_submitter(self):
        query = 'SELECT "username", COUNT("username") AS "value_occurrence" FROM "reddit-post" GROUP BY "username" ORDER BY "value_occurrence" DESC LIMIT 1;'
        params = ('', )
        res = self.db_client.query_all(query, params)
        return res

    def get_top_commenter(self):
        query = 'SELECT "username", COUNT("username") AS "value_occurrence" FROM "reddit-comment" GROUP BY "username" ORDER BY "value_occurrence" DESC LIMIT 1;'
        params = ('', )
        res = self.db_client.query_all(query, params)
        return res

    def get_most_active_user(self):
        query = 'SELECT a.username, COUNT(*) AS "value_occurrence" FROM "reddit-comment" a LEFT JOIN "reddit-post" b  on a.username = b.username GROUP BY a.username ORDER BY "value_occurrence" DESC LIMIT 1;'
        params = ('', )
        res = self.db_client.query_all(query, params)
        return res

    def get_posts_by_user(self, username):
        query = 'select row_to_json("reddit-post") FROM "reddit-post" where username = %s;'
        params = (username, )
        res = self.db_client.query_all(query, params)
        return res

    def get_posts_user_commented(self, username):
        query = 'select row_to_json(a) FROM "reddit-post" a INNER JOIN "reddit-comment" b on a.post_id = b.post_id where b.username = %s GROUP BY a.post_id;'
        params = (username, )
        res = self.db_client.query_all(query, params)
        return res
