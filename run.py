#!/usr/bin/env python2.7

import sys
# Disable creating .pyc files:
sys.dont_write_bytecode = True

from crawler.updates import *
from crawler.manifest import *

m = FileManifestLoader().load("commons-math")
update = UpdateFinder().find_update(m)

import pprint
pprint.pprint(update)

