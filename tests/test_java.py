from tests.updates import UpdatesTest

class JavaTest(UpdatesTest):
    def test_maven(self):
        self.assertHasAllInfo(self.updateFinder.find_update("joda-time:joda-time", "java"))

    def test_clojure(self):
        self.assertHasInfo(self.updateFinder.find_update("aleph", "java"),
                ["name", "description", "version", "stable_version", "updatetime", "url"])
        
