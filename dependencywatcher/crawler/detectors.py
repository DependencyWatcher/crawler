import logging, dateutil.parser, datetime, time

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

	def parse_date(self, text, format=None):
		parsed = None
		if format:
			try:
				parsed = datetime.datetime.strptime(text, format)
			except:
				pass
		if not parsed:
			try:
				parsed = dateutil.parser.parse(text)
			except:
				pass
		if parsed:
			parsed = int(parsed.strftime("%s"))
			if parsed <= time.time():
				parsed = parsed * 1000
		return parsed

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
		if type == "rubygems":
			from dependencywatcher.crawler.rubygems import RubyGemsDetector
			return RubyGemsDetector(manifest)
		if type == "pypi":
			from dependencywatcher.crawler.pypi import PyPiDetector
			return PyPiDetector(manifest)

		raise NotImplementedError("Detector of type '%s' is not supported" % type)

