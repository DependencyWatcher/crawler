from dependencywatcher.crawler.detectors import Detector
import urllib2, json, logging

logger = logging.getLogger(__name__)

class JSDelivrDetector(Detector):
	""" jsdelivr.com API based information detector """
	url = "http://api.jsdelivr.com/v1/jsdelivr/libraries/%s"

	def __init__(self, manifest):
		self.json = None
		super(JSDelivrDetector, self).__init__(manifest) 

	def detect(self, what, options, result):
		if self.json is None:
			url = JSDelivrDetector.url % self.manifest["name"]
			logger.debug("Opening URL: %s" % url)
			r = json.load(urllib2.urlopen(url))
			self.json = r[0] if len(r) > 0 else {}

		try:
			if what == "url":
				result[what] = self.json["homepage"]
			elif what == "description":
				result[what] = self.json["description"]
			elif what == "version":
				result[what] = self.json["lastversion"]
		except KeyError:
			pass

