import logging

logger = logging.getLogger(__name__)

class Detector(object):
	""" Abstract detector that retrieves latest information about dependency """

	def __init__(self, manifest):
		self.manifest = manifest

	def normalize(self, what, text):
		if text:
			text = text.strip()
			if what == "description" and not text.endswith("."):
				text = "%s." % text
		return text

	def detect(self, what, options, result):
		raise NotImplementedError

	@staticmethod
	def create(type, manifest):
		""" Creates detector for the given type """

		if type == "xpath":
			from dependencywatcher.crawler.xpath import XPathDetector
			return XPathDetector(manifest)
		if type == "maven":
			from dependencywatcher.crawler.maven import MavenDetector
			return MavenDetector(manifest)
		if type == "jsdelivr":
			from dependencywatcher.crawler.jsdelivr import JSDelivrDetector
			return JSDelivrDetector(manifest)
		if type == "cdnjs":
			from dependencywatcher.crawler.cdnjs import CDNJSDetector
			return CDNJSDetector(manifest)
		if type == "npmjs":
			from dependencywatcher.crawler.npmjs import NPMJSDetector
			return NPMJSDetector(manifest)

		raise NotImplementedError("Detector of type '%s' is not supported" % type)

