from dependencywatcher.crawler.detectors import Detector
import urllib2, json, logging, os

logger = logging.getLogger(__name__)

class RubyGemsDetector(Detector):
    """ rubygems.org API based information detector """
    url = "https://rubygems.org/api/v1/gems/%s.json"
    auth = "af93e383246a774566bcf661f9c9f591"

    def __init__(self, manifest):
        self.json = None
        super(RubyGemsDetector, self).__init__(manifest) 

    def get(self, library_name):
        url = RubyGemsDetector.url % library_name
        logger.debug("Opening URL: %s" % url)
        request = urllib2.Request(url)
        request.add_header("Authorization", RubyGemsDetector.auth)
        return json.load(urllib2.urlopen(request))

    def detect(self, what, options, result):
        if self.json is None:
            self.json = self.get(self.manifest["name"])
        try:
            if what == "url":
                result[what] = self.normalize(what, self.json["homepage_uri"])
            elif what == "license":
                result[what] = self.normalize(what, ", ".join(self.json["licenses"]))
            elif what in ["version"]:
                result[what] = self.normalize(what, self.json[what])
            if what == "description":
                result[what] = self.normalize(what, self.json["info"])
        except KeyError:
            pass

