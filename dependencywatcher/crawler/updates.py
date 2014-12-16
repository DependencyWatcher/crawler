from dependencywatcher.crawler.detectors import *
from dependencywatcher.crawler.manifest import subst_vars

class UpdateFinder(object):

	def find_update(self, what, context=None, last_version=None):
		""" Finds update for the given dependency manifest or name """

		manifest = what if isinstance(what, dict) else self.create_manifest_by_name(str(what), context)
		if not manifest:
			return None

		update = {}

		# Copy static fields:
		for f in ["name", "license"]:
			try:
				update[f] = manifest[f]
			except KeyError:
				pass

		detectors_cache = {}
		detectors = manifest["detectors"]
		for what in ["version"] + [k for k in detectors.keys() if k != "version"]:
			for detector_type, detector_options in detectors[what].iteritems():
				try:
					detector = detectors_cache[detector_type]
				except KeyError:
					detector = Detector.create(detector_type, manifest)
					detectors_cache[detector_type] = detector

				detector.detect(what, detector_options, update)
				if what in update:
					break

			if what == "version":
				if not "version" in update:
					raise Exception("Can't detect version of %s" % manifest["name"])

				# Substitute version in all manifest properties:
				if last_version == update["version"]:
					raise AlreadyLatestVersion("%s is already at latest version" % manifest["name"])
				subst_vars(manifest, {"VERSION": update["version"]})

		return update

	def create_manifest_by_name(self, name, context=None):
		if context == "java":
			return {
				"detectors": {
					"version": { "maven": {} },
					"description": { "maven": {} },
					"updatetime": { "maven": {} },
					"url": { "maven": {} }
				},
				"name": name,
				"aliases": [ name ]
			}
		if context == "js":
			return {
				"detectors": {
					"version": { "jsdelivr": {}, "cdnjs": {} },
					"description": { "jsdelivr": {}, "cdnjs": {} },
					"url": { "jsdelivr": {}, "cdnjs": {} }
				},
				"name": name
			}
		if context == "nodejs":
			return {
				"detectors": {
					"version": { "npmjs": {} },
					"description": { "npmjs": {} },
					"license": { "npmjs": {} },
					"updatetime": { "npmjs": {} },
					"url": { "npmjs": {} }
				},
				"name": name
			}
		if context == "ruby":
			return {
				"detectors": {
					"version": { "rubygems": {} },
					"description": { "rubygems": {} },
					"license": { "rubygems": {} },
					"url": { "rubygems": {} }
				},
				"name": name
			}
		return None

class AlreadyLatestVersion(Exception):
	pass

