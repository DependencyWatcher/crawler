from dependencywatcher.crawler.detectors import Detector
import urllib2, json, logging

logger = logging.getLogger(__name__)

class RubyGemsDetector(Detector):
	""" jsdelivr.com API based information detector """
	url = "https://rubygems.org/api/v1/gems/%s.json"

	def __init__(self, manifest):
		self.json = None
		super(RubyGemsDetector, self).__init__(manifest) 

	def get(self, library_name):
		url = RubyGemsDetector.url % library_name
		logger.debug("Opening URL: %s" % url)
		return json.load(urllib2.urlopen(url))

	def detect(self, what, options, result):
		if self.json is None:
			self.json = self.get(self.manifest["name"])
		try:
			if what == "url":
				result[what] = self.normalize(what, self.json["homepage_uri"])
			elif what == "license":
				result[what] = self.normalize(what, ", ".join(self.json["licenses"]))
			elif what in ["description", "version"]:
				result[what] = self.normalize(what, self.json[what])
		except KeyError:
			pass

