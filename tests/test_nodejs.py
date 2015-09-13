from tests.updates import UpdatesTest

class NodeJSTest(UpdatesTest):
    def test_npmjs(self):
        self.assertHasAllInfo(self.updateFinder.find_update("npm", "nodejs"))
        
