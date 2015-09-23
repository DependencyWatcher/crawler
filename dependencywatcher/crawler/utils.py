import re
from pkg_resources import parse_version

class VersionUtil():
    UNSTABLE_RE = re.compile("alpha|beta|rc\d|snapshot|dev", re.I)

    @staticmethod
    def is_stable(version):
        return not VersionUtil.UNSTABLE_RE.search(version)

    @staticmethod
    def sort(versions):
        return sorted(versions, cmp=lambda x,y: cmp(parse_version(y), parse_version(x)))

    @staticmethod
    def find_latest(versions):
        if len(versions) > 0:
            return VersionUtil.sort(versions)[0]
        return None

    @staticmethod
    def find_stable(versions):
        if len(versions) > 0:
            for v in VersionUtil.sort(versions):
                if VersionUtil.is_stable(v):
                    return v
        return None

