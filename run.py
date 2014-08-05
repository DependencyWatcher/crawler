#!/usr/bin/env python2.7

import sys
# Disable creating .pyc files:
sys.dont_write_bytecode = True

from dependencywatcher.crawler.updates import *
from dependencywatcher.crawler.manifest import *
from multiprocessing.pool import ThreadPool

import logging
logging.basicConfig(level=logging.DEBUG)

# Test: iterate on all manifests, resolve updates and print them:
import pprint
def print_result(update):
	pprint.pprint(update)

pool = ThreadPool(processes=10)

for m in FileManifestLoader().load_all():
	pool.apply_async(UpdateFinder().find_update, args = (m,), callback = print_result)

pool.close()
pool.join()

	#try:
	#except Exception as e:
	#	logging.exception("Couldn't find update for: %s" % m["name"])

