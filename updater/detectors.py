class Detector():
	""" Abstract detector that retrieves latest information about dependency """
	def detect(options, result):
		raise NotImplementedError


class VersionDetector(Detector):
	""" Detects latest version """
	def detect(options, result):
		pass


class UpdateTimeDetector(Detector):
	""" Detects latest version update date """
	def detect(options, result):
		pass


class ChangeListDetector(Detector):
	""" Detects changelist of the current version """
	def detect(options, result):
		pass


class LicenseDetector(Detector):
	""" Detects dependency license name """
	def detect(options, result):
		pass

