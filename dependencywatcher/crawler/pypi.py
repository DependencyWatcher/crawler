from dependencywatcher.crawler.detectors import Detector
import urllib2, json, logging

logger = logging.getLogger(__name__)

class PyPiDetector(Detector):
	""" pypi.com API based information detector """
	url = "https://pypi.python.org/pypi/%s/json"

	def __init__(self, manifest):
		self.json = None
		super(PyPiDetector, self).__init__(manifest) 

	def get(self, library_name):
		url = PyPiDetector.url % library_name
		logger.debug("Opening URL: %s" % url)
		try:
			return json.load(urllib2.urlopen(url))
		except urllib2.HTTPError:
			return None

	def detect(self, what, options, result):
		if self.json is None:
			self.json = self.get(self.manifest["name"])
		try:
			if what == "url":
				result[what] = self.normalize(what, self.json["info"]["home_page"])
			elif what in ["license", "version"]:
				result[what] = self.normalize(what, self.json["info"][what])
			elif what == "description":
				result[what] = self.normalize(what, self.json["info"]["summary"])
			elif what == "updatetime":
				result[what] = self.parse_date(self.json["releases"][result["version"]][0]["upload_time"])
		except KeyError:
			pass

