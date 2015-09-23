from tests.updates import UpdatesTest

class JSTest(UpdatesTest):

    def test_dot_dash(self):
        check_fields = ["name", "description", "version", "stable_version", "updatetime", "url"]
        self.assertHasInfo(self.updateFinder.find_update("jquery.tagsinput", "js"), check_fields)
        self.assertHasInfo(self.updateFinder.find_update("jquery-tagsinput", "js"), check_fields)

    def test_jsdelivr(self):
        check_fields = ["name", "description", "version", "stable_version", "updatetime", "url"]
        self.assertHasInfo(self.updateFinder.find_update("momentjs", "js"), check_fields)

    def test_cdnjs(self):
        check_fields = ["name", "description", "version", "stable_version", "url"]
        self.assertHasInfo(self.updateFinder.find_update("bootbox", "js"), check_fields)

