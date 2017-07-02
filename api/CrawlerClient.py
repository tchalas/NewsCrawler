import configparser
import psycopg2

## read config
CONFIG = configparser.RawConfigParser()
CONFIG.read('./config.cfg')

# get values from config file
dbname = CONFIG.get('db', 'dbname')
dbuser = CONFIG.get('db', 'dbuser')
dbpassword = CONFIG.get('db', 'dbpassword')
dbhost = CONFIG.get('db', 'dbhost')

class CrawlerClient(object):
    conn = None
    cur = None

    def __init__(self):
        self.conn = psycopg2.connect(dbname=dbname, user=dbuser, host=dbhost, password=dbpassword)
        self.cur = self.conn.cursor()

    #def query(self, query, params):
    #    return self._db_cur.execute(query, params)

    def __del__(self):
        self.conn.close()


    def get_top_posts_by_poins(self, post_type):
        if(post_type == "all"):
            res = self.cur.execute('select row_to_json("reddit-post") FROM "reddit-post" order by score desc limit 10;') # order by score desc limit 10',)
        elif(post_type == "discussion"):
            res = self.cur.execute('select row_to_json("reddit-post") FROM "reddit-post" where domain = %s OR domain = %s order by score desc limit 10;', ("self.Python","i.redd.it",)) # order by score desc limit 10',)
        else:
            res = self.cur.execute('select row_to_json("reddit-post") FROM "reddit-post" where domain != %s AND domain != %s order by score desc limit 10;', ("self.Python","i.redd.it",)) # order by score desc limit 10',)
        res = self.cur.fetchall()
        #print(res)
        return res

    def test(self):
        return "lele"
