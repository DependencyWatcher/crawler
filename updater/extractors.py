import urllib2
from lxml import etree

class Extractor():
	""" Abstract information extractor """
	def retrieve(options):
		raise NotImplementedError


class XPathExtractor():
	""" XPath-based information extractor """

	page_cache = {}

	def retrieve(self, options):
		url = options["url"]
		try:
			page = self.page_cache[url]
		except KeyError:
			response = urllib2.urlopen(url)
			htmlparser = etree.HTMLParser()
			page = etree.parse(response, etree.HTMLParser())
			self.page_cache[url] = page

		return page.xpath(options["xpath"])

