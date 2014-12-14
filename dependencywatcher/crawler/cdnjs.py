from dependencywatcher.crawler.detectors import Detector
import urllib2, json, logging

logger = logging.getLogger(__name__)

class CDNJSDetector(Detector):
	""" cdnjs.com repository based detector """
	url = "https://raw.githubusercontent.com/cdnjs/cdnjs/master/ajax/libs/%s/package.json"

	def __init__(self, manifest):
		self.json = None
		super(CDNJSDetector, self).__init__(manifest) 

	def get(self, library_name):
		url = CDNJSDetector.url % library_name
		logger.debug("Opening URL: %s" % url)
		try:
			return json.load(urllib2.urlopen(url))
		except urllib2.HTTPError:
			return None

	def detect(self, what, options, result):
		if self.json is None:
			library_name = self.manifest["name"]
			self.json = self.get(library_name)
			if not self.json and "-" in library_name:
				self.json = self.get(library_name.replace("-", ""))
			if not self.json and not library_name.endswith("js"):
				self.json = self.get(library_name + "js")
		try:
			result[what] = self.normalize(what, self.json[what])
		except KeyError:
			pass

