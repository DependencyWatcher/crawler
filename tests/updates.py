import unittest
from dependencywatcher.crawler.updates import *

class UpdatesTest(unittest.TestCase):
    """ Abstract unit test that validates that update that was found contains all the info """

    def setUp(self):
        self.updateFinder = UpdateFinder()

    def assertHasInfo(self, update, keys):
        for k in keys:
            self.assertIsNotNone(update[k])

    def assertHasAllInfo(self, update):
        self.assertHasInfo(update, ["name", "description", "license", "version", "updatetime"])

