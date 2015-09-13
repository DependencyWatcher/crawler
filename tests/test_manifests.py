import sys, unittest
from dependencywatcher.crawler.updates import *
from dependencywatcher.crawler.manifest import *
from multiprocessing.pool import ThreadPool

class TestManifests(unittest.TestCase):
    def test_all_manifests(self):
        results = {}
        def collect_result(update):
            if update is not None:
                results[update["name"]] = update

        manifests = []
        pool = ThreadPool(processes=10)
        for m in FileManifestLoader().load_all():
            manifests.append(m)
            pool.apply_async(UpdateFinder().find_update, args = (m,), callback = collect_result)
        pool.close()
        pool.join()

        for m in manifests:
            self.assertIsNotNone(results[m["name"]], "Can't find update for %s" % m["name"])

