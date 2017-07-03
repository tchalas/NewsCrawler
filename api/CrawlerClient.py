import configparser
import psycopg2

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

    def __init__(self):
        self.conn = psycopg2.connect(dbname=dbname, user=dbuser, host=dbhost, password=dbpassword)
        self.cur = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def get_top_posts_by_poins(self, post_type):

        #SQL = 'select row_to_json("reddit-post") FROM "reddit-post" order by score desc limit 10;'
        #data = (, )
        if(post_type == "all"):
            res = self.cur.execute('select row_to_json("reddit-post") FROM "reddit-post" order by score desc limit 10;')
        elif(post_type == "discussion"):
            res = self.cur.execute('select row_to_json("reddit-post") FROM "reddit-post" where domain = %s OR domain = %s order by score desc limit 10;', ("self.Python","i.redd.it",))
        else:
            res = self.cur.execute('select row_to_json("reddit-post") FROM "reddit-post" where domain != %s AND domain != %s order by score desc limit 10;', ("self.Python","i.redd.it",))
        res = self.cur.fetchall()
        return res

    def get_top_posts_by_comments(self, post_type):
        if(post_type == "all"):
            res = self.cur.execute('select row_to_json("reddit-post") FROM "reddit-post" order by comments_count desc limit 10;')
        elif(post_type == "discussion"):
            res = self.cur.execute('select row_to_json("reddit-post") FROM "reddit-post" where domain = %s OR domain = %s order by comments_count desc limit 10;', ("self.Python","i.redd.it",))
        else:
            res = self.cur.execute('select row_to_json("reddit-post") FROM "reddit-post" where domain != %s AND domain != %s order by comments_count desc limit 10;', ("self.Python","i.redd.it",))
        res = self.cur.fetchall()
        #print(res)
        return res

    def test(self):
        return "lele"
