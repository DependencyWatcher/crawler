import logging, os
from dependencywatcher.crawler.xpath import XPathDetector

logger = logging.getLogger(__name__)

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

