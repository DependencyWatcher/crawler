import logging

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
			from dependencywatcher.crawler.xpath import XPathDetector
			return XPathDetector(manifest)
		if type == "maven":
			from dependencywatcher.crawler.maven import MavenDetector
			return MavenDetector(manifest)
		raise NotImplementedError("Detector of type '%s' is not supported" % type)

