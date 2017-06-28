#crawling  python subreddit
from bs4 import BeautifulSoup
import requests

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0"}
r  = requests.get("https://www.reddit.com/r/Python", headers=HEADERS)
s = r.text
posts_soup = BeautifulSoup(s, "html.parser")
posts = posts_soup.find_all("div", class_ = "thing")

for post in posts:
    title_object = post.find("p", class_="title")
    print(title_object)
    tag_object = post.find("p", class_="tagline")
    comments_object = post.find("li", class_="first") 
    
    title = title_object.a.get_text()
    href = title_object.a['href']
    post_link = title_object.a['data-outbound-url']

    author = tag_object.a.get_text()
    time = tag_object.time['datetime']
 
    comments_number = comments_object.a.get_text()
    r  = requests.get(comments_object.a['href'], headers=HEADERS)
    comments_soup = BeautifulSoup(r.text, "html.parser")
    comments = comments_soup.find_all("div", class_ = "thing")
