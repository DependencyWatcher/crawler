from datetime import datetime
from lxml import etree, html
import urllib2, logging
from dependencywatcher.crawler.detectors import Detector

logger = logging.getLogger(__name__)

class XPathDetector(Detector):
	""" XPath-based information detector """

	def __init__(self, manifest):
		self.page_cache = {}
		super(XPathDetector, self).__init__(manifest)

	def resolve(self, options):
		url = options["url"]
		try:
			page = self.page_cache[url]
		except KeyError:
			logger.debug("Opening URL: %s" % url)
			response = urllib2.urlopen(url)
			if url.endswith(".xml"):
				parser = etree.XMLParser()
			else:
				parser = etree.HTMLParser()
			page = etree.parse(response, parser)
			self.page_cache[url] = page

		xpath = options["xpath"]
		element = page.xpath(xpath)
		logger.debug("Resolved XPath '%s': %s" % (xpath, element))
		return element

	def get_node_text(self, node):
		if type(node) is etree._ElementStringResult:
			return node
		return "".join([x for x in node.itertext()])

	def get_node_html(self, node):
		return "".join([etree.tostring(child) for child in node.iterdescendants()])

	def resolve_text(self, options):
		try:
			return self.get_node_text(self.resolve(options)[0])
		except KeyError:
			return None

	def detect_last_version(self, options, result):
		result[self.what] = self.resolve_text(options)

	def detect_update_time(self, options, result):
		date_text = self.resolve_text(options)

		try:
			date_format = options["dateFormat"]
		except KeyError:
			date_format = "%Y%m%d%H%M%S"

		logger.debug("Converting date '%s' using format '%s'" % (date_text, date_format))
		result[self.what] = datetime.strptime(date_text, date_format).strftime("%s")

	def detect_change_list(self, options, result):
		try:
			changelist = []
			for node in self.resolve(options):
				changelist.append(self.get_node_html(node))
			result[self.what] = changelist
		except urllib2.HTTPError:
			logger.warning("Couldn't resolve changelist")

	def detect_license(self, options, result):
		result[self.what] = self.resolve_text(options)

