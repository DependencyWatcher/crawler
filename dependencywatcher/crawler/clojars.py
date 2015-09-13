from dependencywatcher.crawler.detectors import Detector
import urllib2, json, logging

logger = logging.getLogger(__name__)

class ClojarsDetector(Detector):
    """ clojars.org registry API based information detector """
    api_url = "https://clojars.org/api/artifacts/%s"

    def __init__(self, manifest):
        self.json = None
        self.web_detector = Detector.create("xpath", {
            "name": manifest["name"],
            "detectors": {
                "updatetime": {
                    "xpath": {
                        "url": "https://clojars.org/%s" % manifest["name"].replace(":", "/"),
                        "xpath": "//span[@title != '']/@title",
                        "dateFormat": "%a %b %d %H:%M:%S %Z %Y"
                    }
                }
            }
        })
        super(ClojarsDetector, self).__init__(manifest) 

    def detect(self, what, options, result):
        if self.json is None:
            url = ClojarsDetector.api_url % self.manifest["name"].replace(":", "/")
            logger.debug("Opening URL: %s" % url)
            self.json = json.load(urllib2.urlopen(url))

        try:
            if what == "url":
                result[what] = self.normalize(what, self.json["homepage"])
            elif what in ["description", "license", "updatetime"]:
                if what in self.json:
                    result[what] = self.normalize(what, self.json[what])
                else:
                    self.web_detector.detect(what, self.web_detector.manifest["detectors"][what]["xpath"], result)
            elif what == "version":
                result[what] = self.normalize(what, self.json["latest_version"])
        except KeyError:
            pass

