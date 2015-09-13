import logging, dateutil.parser, datetime, time

logger = logging.getLogger(__name__)

class Detector(object):
    """ Abstract detector that retrieves latest information about dependency """

    def __init__(self, manifest):
        self.manifest = manifest

    def normalize(self, what, text):
        if text:
            text = text.strip()
            if what == "description" and not text.endswith("."):
                text = "%s." % text
        return text

    def parse_date(self, text, format=None):
        timestamp = None
        parsed = None
        if format:
            try:
                parsed = datetime.datetime.strptime(text, format)
            except:
                pass
        if not parsed:
            try:
                parsed = dateutil.parser.parse(text)
            except:
                pass
        if parsed is not None:
            timestamp = int(parsed.strftime("%s"))
        if timestamp is None:
            if isinstance(text, int):
                timestamp = text
            elif text.isdigit():
                timestamp = int(text)
        if timestamp is not None:
            if timestamp <= time.time():
                timestamp = timestamp * 1000
        return timestamp

    def detect(self, what, options, result):
        raise NotImplementedError

    @staticmethod
    def create(type, manifest):
        """ Creates detector for the given type """

        if type == "xpath":
            from dependencywatcher.crawler.xpath import XPathDetector
            return XPathDetector(manifest)
        if type == "maven":
            from dependencywatcher.crawler.maven import MavenDetector
            return MavenDetector(manifest)
        if type == "jsdelivr":
            from dependencywatcher.crawler.jsdelivr import JSDelivrDetector
            return JSDelivrDetector(manifest)
        if type == "cdnjs":
            from dependencywatcher.crawler.cdnjs import CDNJSDetector
            return CDNJSDetector(manifest)
        if type == "npmjs":
            from dependencywatcher.crawler.npmjs import NPMJSDetector
            return NPMJSDetector(manifest)
        if type == "rubygems":
            from dependencywatcher.crawler.rubygems import RubyGemsDetector
            return RubyGemsDetector(manifest)
        if type == "pypi":
            from dependencywatcher.crawler.pypi import PyPiDetector
            return PyPiDetector(manifest)
        if type == "clojars":
            from dependencywatcher.crawler.clojars import ClojarsDetector
            return ClojarsDetector(manifest)

        raise NotImplementedError("Detector of type '%s' is not supported" % type)

