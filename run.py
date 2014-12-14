#!/usr/bin/env python2.7

import sys
# Disable creating .pyc files:
sys.dont_write_bytecode = True

from dependencywatcher.crawler.updates import *
from dependencywatcher.crawler.manifest import *
from multiprocessing.pool import ThreadPool

import pprint
import logging
logging.basicConfig(level=logging.DEBUG)

#pprint.pprint(UpdateFinder().find_update(FileManifestLoader().read_manifest("fontawesome")))
pprint.pprint(UpdateFinder().find_update("backbone", "js"))
sys.exit()

# Test: iterate on all manifests, resolve updates and print them:
def print_result(update):
	pprint.pprint(update)

pool = ThreadPool(processes=10)

for m in FileManifestLoader().load_all():
	#print UpdateFinder().find_update(m)
	pool.apply_async(UpdateFinder().find_update, args = (m,), callback = print_result)

pool.close()
pool.join()

	#try:
	#except Exception as e:
	#	logging.exception("Couldn't find update for: %s" % m["name"])

