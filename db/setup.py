# Setup the database, create tables
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

def drop_db():
    # connect to db
    conn = psycopg2.connect(dbname=dbname, user=dbuser, host=dbhost, password=dbpassword)
    cur = conn.cursor()
    # drop tables
    cur.execute('DROP TABLE IF EXISTS "user" CASCADE;')
    cur.execute('DROP TABLE IF EXISTS "post" CASCADE;')
    cur.execute('DROP TABLE IF EXISTS "comment" CASCADE;')
    # commit changes
    conn.commit()
    cur.close()
    conn.close()

def create_db():
    # connect to db
    print("vrea")
    print(dbname)
    conn = psycopg2.connect(dbname=dbname, user=dbuser, host=dbhost, password=dbpassword)
    cur = conn.cursor()

    # add tables
    #cur.execute('DROP TABLE IF EXISTS "user" CASCADE;')
    cur.execute('CREATE TABLE "user" (username varchar PRIMARY KEY);')

    #cur.execute('DROP TABLE IF EXISTS "post" CASCADE;')
    cur.execute('CREATE TABLE "post" (post_id varchar PRIMARY KEY, username varchar NOT NULL, \
                 comments_count int, score int, title varchar, url varchar, posted timestamp, \
                 FOREIGN KEY (username) REFERENCES "user" (username) ON UPDATE CASCADE ON DELETE CASCADE);')

    #cur.execute('DROP TABLE IF EXISTS "comment" CASCADE;')
    cur.execute('CREATE TABLE "comment" (id serial PRIMARY KEY, username varchar NOT NULL, post_id varchar NOT NULL, \
                 FOREIGN KEY (username) REFERENCES "user" (username) ON UPDATE CASCADE ON DELETE CASCADE, \
                 FOREIGN KEY (post_id) REFERENCES "post" (post_id) ON UPDATE CASCADE ON DELETE CASCADE);')

    # commit changes
    conn.commit()
    cur.close()
    conn.close()
