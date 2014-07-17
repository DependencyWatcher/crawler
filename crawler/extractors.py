import urllib2
import logging
from lxml import etree, html

logger = logging.getLogger(__name__)

class Extractor():
	""" Abstract information extractor """
	def retrieve(self, options):
		raise NotImplementedError

	def get_text(self, options):
		raise NotImplementedError

class XPathExtractor():
	""" XPath-based information extractor """

	page_cache = {}

	def retrieve(self, options):
		url = options["url"]
		try:
			page = self.page_cache[url]
		except KeyError:
			logger.info("Opening URL: %s" % url)
			response = urllib2.urlopen(url)
			if url.endswith(".xml"):
				parser = etree.XMLParser()
			else:
				parser = etree.HTMLParser()
			page = etree.parse(response, parser)
			self.page_cache[url] = page

		return page.xpath(options["xpath"])

	def get_text(self, options):
		try:
			r = self.retrieve(options)[0]
			if type(r) is etree._ElementStringResult:
				return r
			return r.text
		except KeyError:
			return None

