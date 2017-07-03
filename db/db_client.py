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

class DBClient(object):
    conn = None
    cur = None

    def __init__(self):
        self.conn = psycopg2.connect(dbname=dbname, user=dbuser, host=dbhost, password=dbpassword)
        self.cur = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def query_all(self, query, params):
        res = self.cur.execute(query, params)
        return self.cur.fetchall()

    def query_all(self, query, params):
        res = self.cur.execute(query, params)
        return self.cur.fetchall()
