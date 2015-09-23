from tests.updates import UpdatesTest

class JavaTest(UpdatesTest):
    def test_maven(self):
        self.assertHasAllInfo(self.updateFinder.find_update("joda-time:joda-time", "java"))

    def test_clojure(self):
        check_fields = ["name", "description", "version", "stable_version", "updatetime", "url"]
        self.assertHasInfo(self.updateFinder.find_update("aleph", "java"), check_fields)
        self.assertHasInfo(self.updateFinder.find_update("org.clojure/clojure", "java"), check_fields)
        
