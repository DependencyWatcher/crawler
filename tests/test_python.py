from tests.updates import UpdatesTest

class PythonTest(UpdatesTest):
    def test_python(self):
        self.assertHasAllInfo(self.updateFinder.find_update("Flask-Login", "python"))
        
