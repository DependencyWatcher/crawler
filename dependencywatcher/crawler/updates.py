from dependencywatcher.crawler.detectors import *
from dependencywatcher.crawler.manifest import subst_vars

class UpdateFinder(object):

	def find_update_using_manifest(self, manifest, last_version=None):
		""" Finds update for the given dependency manifest """
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

				if what == "version":
					if not update["version"]:
						raise Exception("Can't detect version of %s" % manifest["name"])

					# Substitute version in all manifest properties:
					if last_version == update["version"]:
						raise AlreadyLatestVersion("%s is already at latest version" % manifest["name"])
					subst_vars(manifest, {"VERSION": update["version"]})

		return update

	def find_update_using_alias(self, alias, last_version=None):
		if ":" in alias:
			""" Tries to look for an update for the given dependency alias using Maven repository """
			manifest = {
				"detectors": {
					"version": { "maven": {} },
					"updatetime": { "maven": {} },
					"url": { "maven": {} }
				},
				"name": alias,
				"aliases": [ alias ]
			}
			return self.find_update_using_manifest(manifest, last_version)
		return None

	def find_update(self, what, last_version=None):
		if isinstance(what, dict):
			return self.find_update_using_manifest(what, last_version)
		return self.find_update_using_alias(str(what), last_version)

class AlreadyLatestVersion(Exception):
	pass
