#!/usr/bin/env python2.7

import sys
# Disable creating .pyc files:
sys.dont_write_bytecode = True

from crawler.updates import *
from crawler.manifest import *

# Test: iterate on all manifests, resolve updates and print them:
import pprint
for m in FileManifestLoader().load_all():
	update = UpdateFinder().find_update(m)
	pprint.pprint(update)

