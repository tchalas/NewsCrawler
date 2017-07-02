import crawler.crawler_tasks as crawler_tasks

def crawl(max):
    crawler_tasks.craw_reddit.delay("https://www.reddit.com/r/Python", 1, max)
