#!/usr/bin/env python2.7

import sys
# Disable creating .pyc files:
sys.dont_write_bytecode = True

from crawler.updates import *
from crawler.manifest import *

import logging
logging.basicConfig(level=logging.INFO)

# Test: iterate on all manifests, resolve updates and print them:
import pprint
for m in FileManifestLoader().load_all():
	try:
		update = UpdateFinder().find_update(m)
		print "\n"
		pprint.pprint(update)
	except Exception as e:
		logging.exception("Couldn't find update for: %s" % m["name"])

