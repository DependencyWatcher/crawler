from dependencywatcher.crawler.detectors import *
from dependencywatcher.crawler.manifest import subst_vars

logger = logging.getLogger(__name__)

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
        detectors_blacklist = []
        for what in ["version"] + [k for k in detectors.keys() if k != "version"]:
            for detector_type, detector_options in detectors[what].iteritems():
                if not detector_type in detectors_blacklist:
                    try:
                        detector = detectors_cache[detector_type]
                    except KeyError:
                        detector = Detector.create(detector_type, manifest)
                        detectors_cache[detector_type] = detector

                    try:
                        detector.detect(what, detector_options, update)
                        if what in update:
                            break
                    except Exception as e:
                        logger.debug(e)
                        logger.debug("Adding %s detector to blacklist" % detector_type)
                        detectors_blacklist.append(detector_type)

            if what == "version":
                if not "version" in update:
                    raise Exception("Can't detect version of %s" % manifest["name"])

                # Substitute version in all manifest properties:
                if last_version == update["version"]:
                    raise AlreadyLatestVersion("%s is already at latest version" % manifest["name"])
                subst_vars(manifest, {"VERSION": update["version"]})

        return update

    def gen_basic_detectors(self, types):
        detectors = {}
        for f in ["version", "description", "license", "url", "updatetime"]:
            for t in types:
                if not f in detectors:
                    detectors[f] = {}
                detectors[f][t] = {}
        return detectors

    def create_manifest_by_name(self, name, context=None):
        if context == "java":
            return {
                "detectors": self.gen_basic_detectors(["maven", "clojars"]),
                "name": name,
                "aliases": [ name ]
            }
        if context == "js":
            return {
                "detectors": self.gen_basic_detectors(["jsdelivr", "cdnjs"]),
                "name": name
            }
        if context == "nodejs":
            return {
                "detectors": self.gen_basic_detectors(["npmjs"]),
                "name": name
            }
        if context == "ruby":
            return {
                "detectors": self.gen_basic_detectors(["rubygems"]),
                "name": name
            }
        if context == "python":
            return {
                "detectors": self.gen_basic_detectors(["pypi"]),
                "name": name
            }
        return None

class AlreadyLatestVersion(Exception):
    pass

