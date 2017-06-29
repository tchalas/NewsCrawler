from celery import Celery
from bs4 import BeautifulSoup
import requests
import configparser
import psycopg2

## read config
CONFIG = configparser.RawConfigParser()
CONFIG.read('../config.cfg')

# get values from config file
dbname = CONFIG.get('db', 'dbname')
dbuser = CONFIG.get('db', 'dbuser')
dbpassword = CONFIG.get('db', 'dbpassword')
dbhost = CONFIG.get('db', 'dbhost')
#conn = psycopg2.connect(dbname=dbname, user=dbuser, host=dbhost, password=dbpassword)


HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0"}

app = Celery('celery_config', broker='redis://localhost:6379/0')

@app.task
def craw_comments(url, post_id):
    print(post_id)
    """r  = requests.get(url, headers=HEADERS)
    comments_soup = BeautifulSoup(r.text, "html.parser")
    comments = comments_soup.find_all("div", class_ = "thing")
    for comment in comments[1:]:
        entry = comment.find("div", class_="entry unvoted")"""

@app.task
def craw_reddit(url, page):
    conn = psycopg2.connect(dbname=dbname, user=dbuser, host=dbhost, password=dbpassword)
    cur = conn.cursor()
    r  = requests.get(url, headers=HEADERS)
    s = r.text
    posts_soup = BeautifulSoup(s, "html.parser")
    next_url = posts_soup.find("span", class_ = "next-button")
    if next_url == None:
        print(url)
        conn.close()
        return
    craw_reddit.delay(next_url.a['href'], page + 1)
    posts = posts_soup.find_all("div", class_ = "thing")
    # soup every post
    for post in posts:
        post_id = post['id']
        author = post['data-author']
        comments_count = int(post['data-comments-count'])
        score = int(post['data-score'])
        title_object = post.find("p", class_="title")
        title = title_object.a.get_text()
        href = title_object.a['href']
        time = post.find("p", class_="tagline").time['datetime']
        cur.execute('INSERT INTO "user" (username) VALUES (%s) ON CONFLICT DO NOTHING',(author, ))
        cur.execute('INSERT INTO "post" (post_id, username, title, score, url, posted, comments_count) \
                     VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (post_id) DO UPDATE SET score = %s, comments_count = %s ', \
                     (post_id, author, title, score, href, time, comments_count, score, comments_count,))
        conn.commit()
        #if comments_count > 0:
        #    comments = post.find("li", class_="first")
        #    craw_comments.delay(comments.a['href'], post_id)
    cur.close()
    conn.close()
    return "page:" + str(page)
