import crawler_tasks

crawler_tasks.craw_reddit.delay("https://www.reddit.com/r/Python", 1)
