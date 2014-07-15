from crawler.extractors import *
from crawler.detectors import *
from crawler.manifest import subst_vars

class UpdateFinder():
	extractors = {}
	detectors = {}

	def get_extractor(self, type):
		try:
			extractor = self.extractors[type]
		except KeyError:
			if type == "xpath":
				extractor = XPathExtractor()
			else:
				raise Exception("Unknown extractor type: %s" % type)
			self.extractors[type] = extractor
		return extractor

	def get_detector(self, type, extractor):
		try:
			detector = self.detectors[type]
		except KeyError:
			if type == "version":
				detector = VersionDetector(extractor)
			elif type == "updateDate":
				detector = UpdateTimeDetector(extractor)
			elif type == "changelist":
				detector = ChangeListDetector(extractor)
			elif type == "license":
				detector = LicenseDetector(extractor)
			else:
				raise Exception("Unknown detector type: %s" % type)
			self.detectors[type] = detector
		return detector

	def find_update(self, manifest):
		update = {}

		# Copy static fields:
		for f in ["name", "license"]:
			try:
				update[f] = manifest[f]
			except KeyError:
				pass

		detectors = manifest["detectors"]
		for detector_type in ["version"] + [k for k in detectors.keys() if k != "version"]:
			for extractor_type, detector in detectors[detector_type].iteritems():
				self.get_detector(detector_type, self.get_extractor(extractor_type)).detect(detector, update)

				# Substitute version in all manifest properties:
				if detector_type == "version":
					vars = {"VERSION": update["version"]}
					subst_vars(manifest, vars)

		return update

