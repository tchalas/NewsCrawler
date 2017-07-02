from celery import Celery
from bs4 import BeautifulSoup
import requests
import configparser
import psycopg2

## read config
CONFIG = configparser.RawConfigParser()
CONFIG.read('./config.cfg')
section = "db"
env = CONFIG.get('default', 'env')

if env == "test":
    section = "testdb"

# get values from config file
dbname = CONFIG.get(section, 'dbname')
dbuser = CONFIG.get(section, 'dbuser')
dbpassword = CONFIG.get(section, 'dbpassword')
dbhost = CONFIG.get(section, 'dbhost')
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
def craw_odd(s):
    posts_soup = BeautifulSoup(s, "html.parser")
    posts_odd = posts_soup.find_all("div", class_ = "odd")
    for post in posts_odd:
        craw_post.delay(post.decode())

@app.task
def craw_even(s):
    posts_soup = BeautifulSoup(s, "html.parser")
    posts_odd = posts_soup.find_all("div", class_ = "even")
    for post in posts_odd:
        craw_post.delay(post.decode())


@app.task
def craw_post(post_html):
    print(dbname)
    conn = psycopg2.connect(dbname=dbname, user=dbuser, host=dbhost, password=dbpassword)
    cur = conn.cursor()
    post_soup = BeautifulSoup(post_html, "html.parser")
    post = post_soup.find("div", class_ = "thing")
    post_id = post['id']
    author = post['data-author']
    domain = post['data-domain']
    comments_count = int(post['data-comments-count'])
    score = int(post['data-score'])
    title_object = post.find("p", class_="title")
    title = title_object.a.get_text()
    href = title_object.a['href']
    time = post.find("p", class_="tagline").time['datetime']
    print("ISERTING")
    print(domain)
    cur.execute('INSERT INTO "reddit-user" (username) VALUES (%s) ON CONFLICT DO NOTHING',(author, ))
    cur.execute('INSERT INTO "reddit-post" (post_id, username, title, domain, score, url, posted, comments_count) \
                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (post_id) DO UPDATE SET score = %s, comments_count = %s ', \
                         (post_id, author, title, domain, score, href, time, comments_count, score, comments_count,))
    conn.commit()
    #if comments_count > 0:
    #    comments = post.find("li", class_="first")
    #    craw_comments.delay(comments.a['href'], post_id)
    cur.close()
    conn.close()

@app.task
def craw_reddit(url, page):
    r  = requests.get(url, headers=HEADERS)
    s = r.text
    posts_soup = BeautifulSoup(s, "html.parser")
    next_url = posts_soup.find("span", class_ = "next-button")
    if next_url == None:
        print(url)
        return
    craw_reddit.delay(next_url.a['href'], page + 1)
    craw_odd.delay(posts_soup.decode())
    craw_even.delay(posts_soup.decode())
    return "page:" + str(page)
