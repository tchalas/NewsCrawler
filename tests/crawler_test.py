import unittest
import crawler.crawler_tasks as crawler_tasks


# Mock the html response and test the soup production
class CrawlerTests(unittest.TestCase):

    def test_craw_post_task(self):
        rst = abscrawler_tasks.craw_post("ytt")
