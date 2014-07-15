import urllib2
from lxml import etree, html

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
			response = urllib2.urlopen(url)
			htmlparser = etree.HTMLParser()
			page = etree.parse(response, etree.HTMLParser())
			self.page_cache[url] = page

		return page.xpath(options["xpath"])

	def get_text(self, options):
		try:
			return self.retrieve(options)[0].text
		except KeyError:
			return None

