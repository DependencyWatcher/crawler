crawler
=======

Retrieves latest information on dependencies.

[![Build Status](https://travis-ci.org/DependencyWatcher/crawler.png)](https://travis-ci.org/DependencyWatcher/crawler)

### How it operates ###

Crawler fetches newest information on a dependency based on its manifest file. If newer version is found, an update object will be generated and stored into the database. Latest JSON schema for such an update object can be found [here](https://github.com/DependencyWatcher/manifests/blob/master/update.json).


