# Setup the database, create tables
import configparser
import psycopg2

## read config
CONFIG = configparser.RawConfigParser()
CONFIG.read('config.cfg')

# get values from config file
dbname = CONFIG.get('db', 'dbname')
dbuser = CONFIG.get('db', 'dbuser')
dbpassword = CONFIG.get('db', 'dbpassword')
dbhost = CONFIG.get('db', 'dbhost')

# connect to db
conn = psycopg2.connect(dbname=dbname, user=dbuser, host=dbhost, password=dbpassword)
cur = conn.cursor()

# add tables
cur.execute('DROP TABLE IF EXISTS "user" CASCADE;')
cur.execute('CREATE TABLE "user" (user_id varchar PRIMARY KEY NOT NULL, username varchar UNIQUE);')

cur.execute('DROP TABLE IF EXISTS "post" CASCADE;')
cur.execute('CREATE TABLE "post" (post_id varchar PRIMARY KEY  NOT NULL, username varchar NOT NULL, \
             FOREIGN KEY (username) REFERENCES "user" (username) ON UPDATE CASCADE ON DELETE CASCADE);')

cur.execute('DROP TABLE IF EXISTS "comment" CASCADE;')
cur.execute('CREATE TABLE "comment" (id serial PRIMARY KEY, username varchar NOT NULL, post_id varchar NOT NULL, \
             FOREIGN KEY (username) REFERENCES "user" (username) ON UPDATE CASCADE ON DELETE CASCADE, \
             FOREIGN KEY (post_id) REFERENCES "post" (post_id) ON UPDATE CASCADE ON DELETE CASCADE);')

# commit changes
conn.commit()
cur.close()
conn.close()
