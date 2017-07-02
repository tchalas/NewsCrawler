import sys
import unittest
import os
from tests.crawler_test import CrawlerTests

def run():
    #run tests
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print(dir_path)
    tests = unittest.defaultTestLoader.loadTestsFromTestCase(CrawlerTests)
    #tests = unittest.defaultTestLoader.loadTestsFromTestCase
    #tests = unittest.TestLoader().discover('.')
    #crawler_test = CrawlerTests()
    #tests.addTest(crawler_test)
    print(tests)
    ok = unittest.TextTestRunner().run(tests).wasSuccessful()
    sys.exit(0 if ok else 1)
