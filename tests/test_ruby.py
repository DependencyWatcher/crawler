from tests.updates import UpdatesTest

class RubyTest(UpdatesTest):

    def test_gems(self):
        check_fields = ["name", "description", "version", "stable_version", "url", "license"]
        self.assertHasInfo(self.updateFinder.find_update("rails", "ruby"), check_fields)

