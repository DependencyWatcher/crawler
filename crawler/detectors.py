from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class Detector():
	def __init__(self, extractor):
		self.extractor = extractor

	""" Abstract detector that retrieves latest information about dependency """
	def detect(self, options, result):
		raise NotImplementedError


class VersionDetector(Detector):
	""" Detects latest version """
	def detect(self, options, result):
		result["version"] = self.extractor.get_text(options)


class UpdateTimeDetector(Detector):
	""" Detects latest version update date """
	def detect(self, options, result):
		date_text = self.extractor.get_text(options)
		date_format = options["format"]
		logger.debug("Converting date '%s' using format '%s'" % (date_text, date_format))
		result["lastUpdate"] = datetime.strptime(date_text, date_format).strftime("%s")


class ChangeListDetector(Detector):
	""" Detects changelist of the current version """
	def detect(self, options, result):
		pass


class LicenseDetector(Detector):
	""" Detects dependency license name """
	def detect(self, options, result):
		result["license"] = self.extractor.get_text(options)

