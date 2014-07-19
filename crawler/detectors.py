from datetime import datetime
from lxml import etree, html
import urllib2, logging, os

logger = logging.getLogger(__name__)

class Detector(object):
	""" Abstract detector that retrieves latest information about dependency """

	def __init__(self, manifest):
		self.manifest = manifest

	def detect_last_version(self, options, result):
		""" Detects last available version of the dependency """
		raise NotImplementedError

	def detect_update_time(self, options, result):
		""" Detects the last version update time """
		raise NotImplementedError

	def detect_change_list(self, options, result):
		""" Detects change list of the latest version """
		raise NotImplementedError

	def detect_license(self, options, result):
		""" Detects license name of the depdendency """
		raise NotImplementedError

	def detect(self, what, options, result):
		self.what = what
		if what == "version":
			return self.detect_last_version(options, result)
		if what == "updatetime":
			return self.detect_update_time(options, result)
		if what == "changelist":
			return self.detect_change_list(options, result)
		if what == "license":
			return self.detect_license(options, result)
		raise NotImplementedError("Detecting '%s' is not supported" % what)

	@staticmethod
	def create(type, manifest):
		""" Creates detector for the given type """
		if type == "xpath":
			return XPathDetector(manifest)
		if type == "maven":
			return MavenDetector(manifest)
		raise NotImplementedError("Detector of type '%s' is not supported" % type)


class XPathDetector(Detector):
	""" XPath-based information detector """
	page_cache = {}

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
		changelist = []
		for node in self.resolve(options):
			changelist.append(self.get_node_html(node))
		result[self.what] = changelist

	def detect_license(self, options, result):
		result[self.what] = self.resolve_text(options)


class MavenDetector(XPathDetector):
	""" This detector gets newest information from a Maven repository """

	def get_repositories(self, options):
		try:
			return [options["repository"]]
		except KeyError:
			return ["http://central.maven.org/maven2/"]

	def get_urls(self, options):
		try:
			# Search for Maven alias (such an alias will have a ':' separator):
			for alias in self.manifest["aliases"]:
				try:
					url_path = "/".join(alias.replace(".", "/").split(":"))
					break
				except ValueError:
					pass
		except KeyError:
			pass

		if url_path is None:
			raise Exception("No Maven alias was found!")

		urls = []
		for repo in self.get_repositories(options):
			urls.append(os.path.join(repo, url_path, "maven-metadata.xml"))
		return urls

	def resolve(self, options):
		for url in self.get_urls(options):
			new_options = dict(options.items() + [("url", url)])
			result = super(MavenDetector, self).resolve(new_options)
			if not result is None:
				return result

	def detect_last_version(self, options, result):
		new_options = dict(options.items() + [("xpath", "/metadata/versioning/release/text()|/metadata/version/text()")])
		return super(MavenDetector, self).detect_last_version(new_options, result)

	def detect_update_time(self, options, result):
		new_options = dict(options.items() + [("xpath", "/metadata/versioning/lastUpdated/text()")])
		return super(MavenDetector, self).detect_update_time(new_options, result)

