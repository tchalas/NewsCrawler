import sys
import unittest
import os
from tests.crawler_test import CrawlerTests
from tests.api_test import ApiTests


def run():
    #run tests
    dir_path = os.path.dirname(os.path.realpath(__file__))
    craw_tests = unittest.defaultTestLoader.loadTestsFromTestCase(CrawlerTests)
    ok = unittest.TextTestRunner().run(craw_tests).wasSuccessful()
    api_tests = unittest.defaultTestLoader.loadTestsFromTestCase(ApiTests)
    ok = unittest.TextTestRunner().run(api_tests).wasSuccessful()
