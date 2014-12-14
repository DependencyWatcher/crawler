from datetime import datetime
from lxml import etree, html
import urllib2, logging, _strptime, re
from dependencywatcher.crawler.detectors import Detector

logger = logging.getLogger(__name__)

class XPathDetector(Detector):
	""" XPath-based information detector """

	def __init__(self, manifest):
		self.page_cache = {}
		super(XPathDetector, self).__init__(manifest)

	def resolve(self, options, result):
		url = options["url"]
		try:
			page = self.page_cache[url]
		except KeyError:
			logger.debug("Opening URL: %s" % url)
			request = urllib2.Request(url, headers={"User-Agent": "Mozilla/5.0"})
			response = urllib2.urlopen(request)
			if url.endswith(".xml") or url.endswith(".pom"):
				it = etree.iterparse(response, resolve_entities=False)
				for _, el in it:
					try:
						el.tag = el.tag.split("}", 1)[1]  # strip all namespaces
					except IndexError:
						pass
				page = it.root
			else:
				page = etree.parse(response, etree.HTMLParser())
			self.page_cache[url] = page

		xpath = options["xpath"]
		element = page.xpath(xpath)
		logger.debug("Resolved XPath '%s': %s" % (xpath, element))
		return element

	def get_node_text(self, node):
		if type(node) in [etree._ElementStringResult, etree._ElementUnicodeResult]:
			return node
		return "".join([x for x in node.itertext()])

	def get_node_html(self, node):
		return "".join([etree.tostring(child) for child in node.iterdescendants()])

	def resolve_text(self, options, result):
		try:
			r = self.resolve(options, result)
			if r:
				text = self.get_node_text(r[0])
				try:
					regex = re.compile(options["regex"])
					m = regex.search(text)
					if m:
						text = m.group(1)
				except KeyError:
					pass
				return text.strip()
		except IndexError:
			return None

	def detect(self, what, options, result):
		if what == "updatetime":
			date_text = self.normalize(what, self.resolve_text(options, result))
			try:
				date_format = options["dateFormat"]
			except KeyError:
				date_format = "%Y%m%d%H%M%S"
			logger.debug("Converting date '%s' using format '%s'" % (date_text, date_format))
			result[what] = long(datetime.strptime(date_text, date_format).strftime("%s")) * 1000
		elif what == "changelist":
			try:
				changelist = []
				for node in self.resolve(options, result):
					changelist.append(self.normalize(what, self.get_node_html(node)))
				result[what] = changelist
			except urllib2.HTTPError:
				logger.warning("Couldn't resolve changelist")
		else:
			result[what] = self.normalize(what, self.resolve_text(options, result))

