#!/usr/bin/env python2.7

from dependencywatcher.crawler.updates import *
import pprint, logging, sys
logging.basicConfig(level=logging.DEBUG)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print """
USAGE: %s <Dependency Name> <Context>

For exmaple: %s junit:junit java
""" % (sys.argv[0], sys.argv[0])

        sys.exit(2)

    pprint.pprint(UpdateFinder().find_update(sys.argv[1], sys.argv[2]))

