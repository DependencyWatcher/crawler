from dependencywatcher.crawler.detectors import Detector
from dependencywatcher.crawler.utils import VersionUtil
import urllib2, json, logging

logger = logging.getLogger(__name__)

class NPMJSDetector(Detector):
    """ npmjs.org registry API based information detector """
    url = "http://registry.npmjs.org/%s"

    def __init__(self, manifest):
        self.json = None
        super(NPMJSDetector, self).__init__(manifest) 

    def detect(self, what, options, result):
        if self.json is None:
            url = NPMJSDetector.url % self.manifest["name"]
            logger.debug("Opening URL: %s" % url)
            self.json = json.load(urllib2.urlopen(url))

        if not "error" in self.json:
            try:
                if what == "url":
                    result[what] = self.normalize(what, self.json["homepage"])
                elif what in ["description", "license"]:
                    result[what] = self.normalize(what, self.json[what])
                elif what == "version" or what == "stable_version":
                    versions = [v["version"] for v in self.json["versions"].values()]
                    result[what] = VersionUtil.find_latest(versions) if what == "version" else VersionUtil.find_stable(versions)
                elif what == "updatetime":
                    result[what] = self.parse_date(self.json["time"][result["version"]])
            except KeyError:
                pass

