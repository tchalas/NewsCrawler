from celery import Celery
from bs4 import BeautifulSoup
import requests

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0"}

app = Celery('celery_config', broker='redis://localhost:6379/0')

@app.task
def craw_reddit(url, page):
    #add.delay(1, 1)
    r  = requests.get(url, headers=HEADERS)
    s = r.text
    posts_soup = BeautifulSoup(s, "html.parser")
    next_url = posts_soup.find("span", class_ = "next-button")
    if next_url == None:
        print(url)
        return
    craw_reddit.delay(next_url.a['href'], page + 1)
    posts = posts_soup.find_all("div", class_ = "thing")
    # soup every post
    for post in posts:
        post = posts[8]
        title_object = post.find("p", class_="title")
        title = title_object.a.get_text()
        return "page:" + str(page) + title
