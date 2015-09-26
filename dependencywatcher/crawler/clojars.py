from dependencywatcher.crawler.detectors import Detector
from dependencywatcher.crawler.utils import VersionUtil
import urllib2, json, logging

logger = logging.getLogger(__name__)

class ClojarsDetector(Detector):
    """ clojars.org registry API based information detector """
    api_url = "https://clojars.org/api/artifacts/%s"

    def __init__(self, manifest):
        self.json = None
        name = manifest["name"]
        self.clojars_url = "https://clojars.org/%s" % name.replace(":", "/")
        maven_alias = name.replace("/", ":")
        if not ":" in maven_alias:
            maven_alias = "%s:%s" % (maven_alias, maven_alias)
        self.maven_detector = Detector.create("xpath", {
            "name": name,
            "aliases": [maven_alias],
            "detectors": {
                "updatetime": {
                    "xpath": {
                        "url": self.clojars_url,
                        "xpath": "//span[@title != '']/@title",
                        "dateFormat": "%a %b %d %H:%M:%S %Z %Y"
                    }
                },
                "url": {
                    "xpath": {
                        "url": self.clojars_url,
                        "xpath": "//ul[@id='jar-info-bar']//a/@href"
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
                if what in self.json:
                    result[what] = self.normalize(what, self.json["homepage"])
                else:
                    self.maven_detector.detect(what, self.maven_detector.manifest["detectors"][what]["xpath"], result)
                if not result[what]:
                    result[what] = self.clojars_url
            elif what in ["description", "license", "updatetime"]:
                if what in self.json:
                    result[what] = self.normalize(what, self.json[what])
                else:
                    self.maven_detector.detect(what, self.maven_detector.manifest["detectors"][what]["xpath"], result)
            elif what == "version" or what == "stable_version":
                versions = [v["version"] for v in self.json["recent_versions"]]
                result[what] = VersionUtil.find_latest(versions) if what == "version" else VersionUtil.find_stable(versions)
        except KeyError:
            pass

