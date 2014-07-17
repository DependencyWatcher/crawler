from datetime import datetime

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
		result["lastUpdate"] = datetime.strptime(date_text, options["format"]).strftime("%s")


class ChangeListDetector(Detector):
	""" Detects changelist of the current version """
	def detect(self, options, result):
		pass


class LicenseDetector(Detector):
	""" Detects dependency license name """
	def detect(self, options, result):
		result["license"] = self.extractor.get_text(options)

