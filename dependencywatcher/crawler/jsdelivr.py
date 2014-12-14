from dependencywatcher.crawler.detectors import Detector
import urllib2, json, logging

logger = logging.getLogger(__name__)

class JSDelivrDetector(Detector):
	""" jsdelivr.com API based information detector """
	url = "http://api.jsdelivr.com/v1/jsdelivr/libraries/%s"

	def __init__(self, manifest):
		self.json = None
		super(JSDelivrDetector, self).__init__(manifest) 

	def get(self, library_name):
		url = JSDelivrDetector.url % library_name
		logger.debug("Opening URL: %s" % url)
		r = json.load(urllib2.urlopen(url))
		return r[0] if len(r) > 0 else {}

	def detect(self, what, options, result):
		if self.json is None:
			library_name = self.manifest["name"]
			self.json = self.get(library_name)
			if len(self.json) == 0 and not library_name.endswith("js"):
				self.json = self.get(library_name + "js")
		try:
			if what == "url":
				result[what] = self.json["homepage"]
			elif what == "description":
				result[what] = self.json["description"]
			elif what == "version":
				result[what] = self.json["lastversion"]
		except KeyError:
			pass

